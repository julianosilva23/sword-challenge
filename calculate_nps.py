from pyspark.sql import SparkSession
import pyspark.sql.types as T

spark = (SparkSession.builder
    .appName("ReadJSON")
    .getOrCreate()
)

schema = T.StructType([
    T.StructField("id", T.IntegerType(), True),
    T.StructField("patient_id", T.IntegerType(), True),
    T.StructField("scores", T.MapType(T.StringType(), T.IntegerType()), True),
    T.StructField("date", T.DateType(), True)
])

json_file_path = 'database/patient_scores.json'

df = spark.read.option("multiline", True).schema(schema).json(json_file_path)

df.printSchema()

df.show(truncate=False, vertical=True)

spark.stop()
