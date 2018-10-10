
from pyspark.sql import SparkSession

import argparse

def quiet_logs(sc, log_level="ERROR"):
  # log_level : INFO, WARN, ERROR, OFF.
    
  logger = sc._jvm.org.apache.log4j
  level = getattr(logger.Level, log_level, "INFO")

  logger.LogManager.getLogger("org"). setLevel(level)
  logger.LogManager.getLogger("akka").setLevel(level)

if __name__ == "__main__":
    
  parser = argparse.ArgumentParser(description="Visualise the elements of a spatial RDD")
  parser.add_argument('-fits', dest='file_name',required=True,help='Path to a FITS file')
  parser.add_argument('-hdu', dest='hdu',required=True,help='HDU index to load.')
    
  args = parser.parse_args(None)

  # Initialize the Spark Session
  spark = SparkSession.builder.getOrCreate()

  # Set logs to be quiet
  quiet_logs(spark.sparkContext, log_level="OFF")

  # Load the data inside a DataFrame
  df = spark.read.format("fits").option("hdu", args.hdu).load(args.file_name)

  # Apply a collapse function
  # Before, repartition our DataFrame to mimick a large data set.
  #data = df.repartition(256).rdd.mapPartitions(lambda partition: mean(partition)).collect()
  data = df.repartition(256).rdd.collect()

  # Re-organise the data into lists of x, y, z coordinates
  x = [p[0] for p in data if p is not None]
  y = [p[1] for p in data if p is not None]
  z = [p[2] for p in data if p is not None]

  #print(x)
  print(x.__class__.__name__)
  print(len(x))
  print(x[0])
  print(x[len(x)-1])

  import inlib
  print(inlib.spark_greet())

  # boost wrapping :
  #import hello_spark
  #print(hello_spark.greet())
  #hello_spark.read_list(x)
    
