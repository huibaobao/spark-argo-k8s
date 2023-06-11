from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql.functions import corr, lit

spark = SparkSession.builder.getOrCreate()
inputs = spark.sparkContext.parallelize(range(50))
print("-----inputs are created------")
def generate_rows(input_val):
    rows = []
    for i in range(1000):
        rows.append(Row(value=float(input_val * 1000 + i)))
    return rows

# Calculate the correlation between columns
df = inputs.flatMap(generate_rows).toDF()
print("=========data frame is created==========")
# Create new columns based on the `value` column
df = df.withColumn('double_value', df['value'] * 2)
df = df.withColumn('triple_value', df['value'] * 3)
df = df.withColumn('squared_value', df['value'] ** 2)


print("*****************number of rows****************", df.count())
# Show the updated DataFrame
df.show()
