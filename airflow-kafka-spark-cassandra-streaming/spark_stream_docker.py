import logging
from cassandra.cluster import Cluster
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType

def create_keyspace(session):
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS spark_streams
        WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};
    """)
    print("Cassandra - Keyspace created successfully!")

def create_table(session):
    session.execute("""
    CREATE TABLE IF NOT EXISTS spark_streams.created_users (
        id TEXT PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        gender TEXT,
        address TEXT,
        post_code TEXT,
        email TEXT,
        username TEXT,
        registered_date TEXT,
        phone TEXT,
        picture TEXT);
    """)
    print("Cassandra Table created successfully!")

def insert_data(session, **kwargs):
    print("inserting data...")
    user_id = kwargs.get('id')
    first_name = kwargs.get('first_name')
    last_name = kwargs.get('last_name')
    gender = kwargs.get('gender')
    address = kwargs.get('address')
    postcode = kwargs.get('post_code')
    email = kwargs.get('email')
    username = kwargs.get('username')
    dob = kwargs.get('dob')
    registered_date = kwargs.get('registered_date')
    phone = kwargs.get('phone')
    picture = kwargs.get('picture')

    try:
        session.execute("""
            INSERT INTO spark_streams.created_users(id, first_name, last_name, gender, address, 
                post_code, email, username, dob, registered_date, phone, picture)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (user_id, first_name, last_name, gender, address,
              postcode, email, username, dob, registered_date, phone, picture))
        print(f"Data inserted for {first_name} {last_name}")
    except Exception as e:
        print(f'could not insert data due to {e}')

def create_spark_connection():
    s_conn = None
    try:
        print("Creating spark session!")
        s_conn = SparkSession.builder \
            .appName('SparkDataStreaming') \
            .config('spark.jars.packages', "com.datastax.spark:spark-cassandra-connector_2.12:3.4.0,"
                                           "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
            .config('spark.cassandra.connection.host', 'cassandra') \
            .getOrCreate()
        s_conn.sparkContext.setLogLevel("ERROR")
        print("Spark connection created successfully!")
    except Exception as e:
        print(f"Couldn't create the spark session due to exception {e}")
    return s_conn

def connect_to_kafka(spark_conn):
    spark_df = None
    try:
        spark_df = spark_conn.readStream \
            .format('kafka') \
            .option('kafka.bootstrap.servers', 'broker:29092') \
            .option('subscribe', 'users_data') \
            .option('startingOffsets', 'earliest') \
            .load()
        print("kafka dataframe created successfully")
    except Exception as e:
        print(f"kafka dataframe could not be created because: {e}")
    return spark_df

def create_cassandra_connection():
    try:
        cluster = Cluster(['cassandra'])
        cas_session = cluster.connect()
        print("Cassandra session created succesfully!")
        return cas_session
    except Exception as e:
        print(f"Could not create cassandra connection due to {e}")
        return None

def create_selection_df_from_kafka(spark_df):
    schema = StructType([
        StructField("id", StringType(), False),
        StructField("first_name", StringType(), False),
        StructField("last_name", StringType(), False),
        StructField("gender", StringType(), False),
        StructField("address", StringType(), False),
        StructField("post_code", StringType(), False),
        StructField("email", StringType(), False),
        StructField("username", StringType(), False),
        StructField("registered_date", StringType(), False),
        StructField("phone", StringType(), False),
        StructField("picture", StringType(), False)
    ])
    sel = spark_df.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col('value'), schema).alias('data')).select("data.*")
    return sel

def foreach_batch_function(df, epoch_id):
    print(f"Batch {epoch_id}")
    #df.show() # Can be noisy, but good for debug
    # To write to cassandra, we typically use the batch write, but here the loop was just showing data
    # The original code logic for WRITING to cassandra is inside the stream writer below?
    # Wait, the original code had `selection_df.writeStream....format("org.apache.spark.sql.cassandra")...`
    # It used `foreachBatch` just to print?
    # Oh, I see. `selection_df.writeStream.foreachBatch(foreach_batch_function)` - wait, NO.
    # The original code calls `.format("org.apache.spark.sql.cassandra")` directly on the stream.
    # It does NOT use foreachBatch usually for that unless doing dual output.
    # Let's check original line 172:
    # `streaming_query = (selection_df.writeStream.foreachBatch(foreach_batch_function)`
    # AND `.outputMode("append").format("org.apache.spark.sql.cassandra")...`
    # This chain is valid? `foreachBatch` returns a DataStreamWriter? NO, it returns nothing/void or starts the query?
    # Pyspark writeStream: `foreachBatch` sets the output. `format` sets the sink.
    # You cannot have BOTH `foreachBatch` AND `format(...)`.
    # `foreachBatch` is a sink. `format(...)` + `start()` is a sink.
    # The original code looks like:
    # streaming_query = (selection_df.writeStream.foreachBatch(foreach_batch_function) ... .start())
    # This implies `foreachBatch` returns the writer? YES.
    # But usually providing a batch function overrides the standard sink?
    # No, `foreachBatch` allows you to do custom logic like `df.write.format(...).save()`.
    # IF the original code chains them, it might be that `foreachBatch` is ignored if `format` is specified later? Or vice versa?
    # Actually, `foreachBatch` is an output trigger.
    # If the user's code had both, maybe it was working?
    # I will stick to the original code structure as much as possible but correct proper logic.
    # Actually, if I look at line 172 in original:
    # `selection_df.writeStream.foreachBatch(foreach_batch_function).outputMode(...).format(...)`
    # This is suspicious. `foreachBatch` should be the LAST thing before `start()` or `trigger()`.
    # Or, if I use `format("cassandra")`, I don't need `foreachBatch` (unless I want to print).
    # I will keep it simple: Write to Cassandra.
    pass

if __name__ == "__main__":
    spark_conn = create_spark_connection()
    if spark_conn is not None:
        spark_df = connect_to_kafka(spark_conn)
        selection_df = create_selection_df_from_kafka(spark_df)
        session = create_cassandra_connection()
        if session is not None:
            create_keyspace(session)
            create_table(session)
            print("Streaming is being started...")
            
            # Write directly to Cassandra
            streaming_query = (selection_df.writeStream
                               .outputMode("append")
                               .format("org.apache.spark.sql.cassandra")
                               .option('checkpointLocation', '/tmp/checkpoint')
                               .option('keyspace', 'spark_streams')
                               .option('table', 'created_users')
                               .start())
            streaming_query.awaitTermination()
