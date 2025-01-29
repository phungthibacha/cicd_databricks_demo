from cicd_project.cleandf import clean_name
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DateType, DoubleType
from pandas.testing import assert_frame_equal
import pytest

@pytest.fixture(scope="session")
def spark_session():
    global spark
    try:
        spark
    except NameError:
        from databricks.connect import DatabricksSession
        spark = DatabricksSession.builder.getOrCreate()
    yield spark

@pytest.fixture(scope="session")
def create_customerdf(spark_session):
    schema = StructType([ \
        StructField("c_custkey", StringType(),True), \
        StructField("c_name", StringType(),True), \
        StructField("c_address", StringType(),True), \
        StructField("c_nationkey", IntegerType(),True), \
        StructField("c_phone", StringType(),True), \
        StructField("c_acctbal", DoubleType(),True), \
        StructField("c_mktsegment", StringType(),True), \
        StructField("c_comment", StringType(),True) \
    ])
    df = spark_session.createDataFrame([
        ("cust1", 'a', 'sydney', 1, '2123', 423523.4, 'priority', 'no comment'),
        ("cust2", 'b', 'brisbane', 5, '2312', 5244323.5, 'vip', 'no comment'),
        ("cust3", 'c', 'melbourne', 6, '53453', 24332.4, 'starter', 'comment'),
        ("cust4", 'd', 'melbourne', 2, '631224', 2343242.3, 'starter', 'no comment'),
        ("cust5", 'e', 'adelaide', 2, '63443', 5221.2, 'starter', ''),
        ("cust6", 'f', 'sydney', 3, '75695', 5231423.3, 'vip', 'comment'),
    ], schema)
    yield df

def test_clean_name(spark_session, create_customerdf):
    result = clean_name(create_customerdf)
    schema = StructType([ \
        StructField("customer_id", StringType(),True), \
        StructField("customer_name", StringType(),True), \
        StructField("customer_address", StringType(),True), \
        StructField("nation_id", IntegerType(),True), \
        StructField("customer_phone", StringType(),True), \
        StructField("customer_balance", DoubleType(),True), \
        StructField("customer_segment", StringType(),True), \
        StructField("customer_comment", StringType(),True) \
    ])
    expected = spark_session.createDataFrame([
        ("cust1", 'a', 'sydney', 1, '2123', 423523.4, 'priority', 'no comment'),
        ("cust2", 'b', 'brisbane', 5, '2312', 5244323.5, 'vip', 'no comment'),
        ("cust3", 'c', 'melbourne', 6, '53453', 24332.4, 'starter', 'comment'),
        ("cust4", 'd', 'melbourne', 2, '631224', 2343242.3, 'starter', 'no comment'),
        ("cust5", 'e', 'adelaide', 2, '63443', 5221.2, 'starter', ''),
        ("cust6", 'f', 'sydney', 3, '75695', 5231423.3, 'vip', 'comment'),
    ], schema)
    assert_frame_equal(result.toPandas(), expected.toPandas())