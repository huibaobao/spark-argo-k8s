from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql.functions import corr, lit

spark = SparkSession.builder.getOrCreate()
inputs = spark.sparkContext.parallelize(range(50))

def generate_rows(input_val):
    rows = []
    for i in range(10000):
        rows.append(Row(value=float(input_val * 10000 + i)))
    return rows

df = inputs.flatMap(generate_rows).toDF()

# Create new columns based on the `value` column
df = df.withColumn('double_value', df['value'] * 2)
df = df.withColumn('triple_value', df['value'] * 3)
df = df.withColumn('squared_value', df['value'] ** 2)

# Calculate the correlation between columns
corr_value_double = df.select(corr('value', 'double_value')).first()[0]
corr_value_triple = df.select(corr('value', 'triple_value')).first()[0]
corr_value_squared = df.select(corr('value', 'squared_value')).first()[0]

# Add correlation values as new columns
df = df.withColumn('corr_value_double', lit(corr_value_double))
df = df.withColumn('corr_value_triple', lit(corr_value_triple))
df = df.withColumn('corr_value_squared', lit(corr_value_squared))

print("*****************number of rows****************", df.count())
# Show the updated DataFrame
df.show()
