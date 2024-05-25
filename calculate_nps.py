from pyspark.sql import SparkSession
import pyspark.sql.types as T

# Inicializar a sessão Spark
spark = SparkSession.builder \
    .appName("ReadJSON") \
    .getOrCreate()

# Definir o esquema para o arquivo JSON
schema = T.StructType([
    T.StructField("id", T.IntegerType(), True),
    T.StructField("patient_id", T.IntegerType(), True),
    T.StructField("scores", T.MapType(T.StringType(), T.IntegerType()), True),
    T.StructField("date", T.DateType(), True)
])

json_file_path = 'database/patient_scores.json'

df = spark.read.option("multiline", True).schema(schema).json(json_file_path)

df.printSchema()

# Exibir os dados
df.show(truncate=False, vertical=True)


# Fechar a sessão Spark
spark.stop()
