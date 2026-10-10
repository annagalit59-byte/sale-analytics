import os
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import DoubleType

spark = SparkSession.builder.appName("SaleAnalytics").getOrCreate()

print("--- Cleaning Data (Part C) ---")
df = spark.read.csv("data/orders.csv", header=True, inferSchema=True)
print(f"Initial row count: {df.count()}")

df = df.dropDuplicates(["order_id"])
print(f"Row count after removing duplicates: {df.count()}")

cleaned_price_expr = F.regexp_replace(F.regexp_replace(F.col("unit_price").cast("string"), "₱", ""), ",", "").cast(DoubleType())
df = df.withColumn("unit_price", cleaned_price_expr)

df = df.filter(F.col("quantity") > 0)
print(f"Row count after filtering negative quantities: {df.count()}")

df = df.withColumn("region", F.initcap(F.coalesce(F.col("region"), F.lit("Unknown"))))
print(f"Row count after standardizing regions: {df.count()}")

os.makedirs("results", exist_ok=True)

print("--- Analyzing at Scale (Part D) ---")
rev_cat = df.filter(F.col("status") == "Delivered") \
    .withColumn("revenue", F.col("unit_price") * F.col("quantity")) \
    .groupBy("category").agg(F.sum("revenue").alias("total_revenue"))
rev_cat.toPandas().to_csv("results/revenue_by_category.csv", index=False)

df = df.withColumn("hour", F.hour(F.col("timestamp")))
orders_hour = df.groupBy("hour").agg(F.count("order_id").alias("order_count")).orderBy("hour")
orders_hour.toPandas().to_csv("results/orders_per_hour.csv", index=False)

rev_region = df.filter(F.col("status") == "Delivered") \
    .withColumn("revenue", F.col("unit_price") * F.col("quantity")) \
    .groupBy("region").agg(F.sum("revenue").alias("revenue"), F.count("order_id").alias("order_count"))
rev_region.toPandas().to_csv("results/region_summary.csv", index=False)

canc_pm = df.groupBy("payment_method") \
    .agg(
        F.count("order_id").alias("total_orders"),
        F.sum(F.when(F.col("status") == "Cancelled", 1).otherwise(0)).alias("cancelled_orders")
    ) \
    .withColumn("cancellation_rate", F.col("cancelled_orders") / F.col("total_orders"))
canc_pm.toPandas().to_csv("results/cancellation_by_payment.csv", index=False)

aov = df.filter(F.col("status") == "Delivered") \
    .withColumn("revenue", F.col("unit_price") * F.col("quantity")) \
    .agg(F.avg("revenue").alias("avg_order_value"))
aov.toPandas().to_csv("results/aov.csv", index=False)

print("Analysis complete. Results exported to results/")
