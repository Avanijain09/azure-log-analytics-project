from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp

# Initialize a local Spark Session
spark = SparkSession.builder \
    .appName("AppLogAnalytics_Silver") \
    .getOrCreate()

# Define local file paths matching your exact folder names
bronze_path = "Bronze/*.json"
silver_path = "Silver/cleaned_logs"

print("Reading raw JSON data from Bronze layer...")
raw_df = spark.read.json(bronze_path)

print("Cleaning and transforming data...")
# Drop rows where critical fields are null
cleaned_df = raw_df.dropna(subset=["user_id", "event_id"])

# Convert string timestamp to an actual timestamp datatype
transformed_df = cleaned_df.withColumn(
    "event_timestamp", 
    to_timestamp(col("event_timestamp"))
)

# Show the new schema and a sample of the cleaned data in the terminal
transformed_df.printSchema()
transformed_df.show(5, truncate=False)

print(f"Saving cleaned data to Silver layer in Parquet format at: {silver_path}")
# Write the cleaned data to the Silver folder in Parquet format
transformed_df.write.mode("overwrite").parquet(silver_path)

print("✅ Silver layer transformation complete!")