from pyspark.sql.dataframe import DataFrame
def clean_name(df:DataFrame):
    df = df.withColumnRenamed("c_custkey", "customer_id") \
            .withColumnRenamed("c_name", "customer_name") \
            .withColumnRenamed("c_address", "customer_address") \
            .withColumnRenamed("c_nationkey", "nation_id") \
            .withColumnRenamed("c_phone", "customer_phone") \
            .withColumnRenamed("c_acctbal", "customer_balance") \
            .withColumnRenamed("c_mktsegment", "customer_segment") \
            .withColumnRenamed("c_comment", "customer_comment")
    return df