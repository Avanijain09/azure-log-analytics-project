from pyspark.sql import SparkSession
from pyspark.sql.functions import count, col

# Initialize a local Spark Session
spark = SparkSession.builder \
    .appName("AppLogAnalytics_Gold") \
    .getOrCreate()

# Define local file paths
silver_path = "Silver/cleaned_logs"
gold_event_metrics_path = "Gold/event_metrics"
gold_device_metrics_path = "Gold/device_metrics"

print("Reading cleaned Parquet data from Silver layer...")
silver_df = spark.read.parquet(silver_path)

print("Calculating Business Metrics for Gold Layer...")

# KPI 1: Count of each event type (Find out how many logins, crashes, etc.)
event_counts_df = silver_df.groupBy("event_type") \
    .agg(count("event_id").alias("total_events")) \
    .orderBy(col("total_events").desc())

print("--- Event Metrics (KPI 1) ---")
event_counts_df.show()

# KPI 2: Device usage distribution (Which platform is most popular)
device_counts_df = silver_df.groupBy("device") \
    .agg(count("event_id").alias("total_interactions")) \
    .orderBy(col("total_interactions").desc())

print("--- Device Metrics (KPI 2) ---")
device_counts_df.show()

print("Saving final aggregated data to Gold layer...")
# Write the highly aggregated data to the Gold folder
event_counts_df.write.mode("overwrite").parquet(gold_event_metrics_path)
device_counts_df.write.mode("overwrite").parquet(gold_device_metrics_path)

print("✅ Gold layer business aggregation complete!")