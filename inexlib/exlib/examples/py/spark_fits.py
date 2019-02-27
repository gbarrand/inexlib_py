# Copyright (C) 2010, Guy Barrand. All rights reserved.
# See the file exlib.license for terms.

# Read first hdu of spark_test_data.fits.
# The first hdu contains a table of coords of all points of a 3D grid cube of size 27.
# First point is (0,0,0) and last one is (26,26,26). We have them 27*27*27 = 19683 points.

# First version provided by J.Peloton.

#///////////////////////////////////////////////////////////////////////////////////////
#/// main : ////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////////////
import pyspark.sql
import argparse

if __name__ == "__main__":

  #///////////////////////////////////////////////////////////////////////////////////////
  #/// args : ////////////////////////////////////////////////////////////////////////////
  #///////////////////////////////////////////////////////////////////////////////////////
  parser = argparse.ArgumentParser()
  parser.add_argument('-verbose', dest='verbose',required=False,help='verbosity')
  parser.add_argument('-file', dest='file_name',required=True,help='Path to a data file')
  parser.add_argument('-hdu', dest='hdu',required=True,help='HDU index to load.')
  parser.add_argument('-vis_mode', dest='vis_mode',required=False,help='Visualization mode')
    
  args = parser.parse_args(None)
  
  #///////////////////////////////////////////////////////////////////////////////////////
  #/// Spark : ///////////////////////////////////////////////////////////////////////////
  #///////////////////////////////////////////////////////////////////////////////////////

  # Initialize the Spark Session :
  spark = pyspark.sql.SparkSession.builder.getOrCreate()

  # Set logs to be quiet :
  logger = spark._jvm.org.apache.log4j
  log_level = "OFF"                                   # INFO, WARN, ERROR, OFF.
  level = getattr(logger.Level, log_level, "INFO")    # level__class__ is 'py4j.java_gateway.JavaObject'
  logger.LogManager.getLogger("org"). setLevel(level)
  logger.LogManager.getLogger("akka").setLevel(level)

  # Attach the data file to a DataFrame :
  df = spark.read.format("fits").option("hdu", args.hdu).load(args.file_name)
 #print("df.count() : "+str(df.count())+". Should be 19683.")
  df_count_ref = 19683
  if df.count() != df_count_ref :
    print("df.count() "+str(df.count())+", expected "+str(df_count_ref))
    exit()

  # Gather result into the driver :
  data = df.collect()                  # at the return of .collect(), we are in the Python world.
 #print(data.__class__.__name__)       # list
 #print(data[0].__class__.__name__)    # Row
 #print(data[0][0].__class__.__name__) # float
  
  row = data[0]
 #print("len(row) : "+str(len(row))+". Should be 3.")

  x = [row[0] for row in data if row is not None]
  y = [row[1] for row in data if row is not None]
  z = [row[2] for row in data if row is not None]

  #for i in range(len(x)): print(str(x[i])+" "+str(y[i])+" "+str(z[i]))
  
 #print('//////////////////////////////////////')
 #print(x.__class__.__name__)
 #print(len(x))

 #print(str(x[0])+" "+str(y[0])+" "+str(z[0]))
 #last = len(x)-1
 #print(str(x[last])+" "+str(y[last])+" "+str(z[last]))
