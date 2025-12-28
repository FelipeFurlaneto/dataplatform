# %%
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("EnterpriseLocal") \
    .master("k8s://https://192.168.65.3:6443") \
    .config("spark.kubernetes.namespace", "spark") \
    .config("spark.kubernetes.container.image", "apache/spark:3.5.1") \
    .getOrCreate()

# %%
# Agora cada célula executa no cluster
df = spark.range(0, 1000).toDF("number")
df.show()
