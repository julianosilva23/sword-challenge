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

assert df.count() > 0, 'Database is empty'
df.printSchema()

df.createOrReplaceTempView("patient_scores")

result_df = spark.sql("""
    WITH most_recent_score_by_month AS (
        SELECT
            id,
            scores.satisfaction satisfaction,
            patient_id,
            date_trunc('MM', date) month_date,
            ROW_NUMBER() OVER(PARTITION BY patient_id, date_trunc('MM', date) ORDER BY date DESC) row_number
        FROM patient_scores
    ), filter_most_recent_score_and_classify AS (
        SELECT
            id,
            patient_id,
            satisfaction,
            CASE
                WHEN satisfaction > 8 THEN 'promoter'
                WHEN satisfaction < 7 THEN 'detractor'
                ELSE 'ignore'
            END satisfaction_label,
            month_date
        FROM most_recent_score_by_month
        WHERE row_number = 1
    ), count_classification AS (
        SELECT
            month_date,
            COUNT(1) number_of_patients,
            COUNT(1) FILTER(WHERE satisfaction_label = 'promoter') number_of_promoters,
            COUNT(1) FILTER(WHERE satisfaction_label = 'detractor') number_of_detractors
        FROM filter_most_recent_score_and_classify
        GROUP BY month_date
    )
    SELECT
        *,
        ROUND(
            (
                (number_of_promoters - number_of_detractors) / number_of_patients
            ) * 100
        , 0) nps
    FROM count_classification
""")


result_df.show(truncate=False, vertical=True)

spark.stop()
