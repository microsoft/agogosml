package org.apache.spark.ml.mleap.feature

import com.holdenkarau.spark.testing.{DataFrameSuiteBase, SharedSparkContext, SparkSessionProvider}
import org.apache.spark.sql.types.{StringType, StructField, StructType}
import org.apache.spark.sql.{Row, SparkSession}
import org.scalatest.FunSuite

class LengthCounterTest extends FunSuite with DataFrameSuiteBase with SharedSparkContext {

  override implicit def reuseContextIfPossible: Boolean = true

  // Need to retrieve access to SparkSesssion from SparkContext
  // but DataFrameSuiteBase has unneeded dependency on Spark-hive
  // See github issue: https://github.com/holdenk/spark-testing-base/issues/148#issuecomment-437859541
  override def beforeAll(): Unit = {
    super[SharedSparkContext].beforeAll()
    SparkSessionProvider._sparkSession = SparkSession
      .builder()
      .appName("test-app")
      .master("local[2]")
      .getOrCreate()
  }

  test("Spark custom transformer (LengthCounter) functions properly") {

    // Setup dataframe
    val schema = List(StructField("text", StringType, true))
    val data = Seq(
      Row("Scaramouche, Scaramouche, will you do the Fandango"),
      Row("Thunderbolt and lightning, very, very fright'ning me")
    )
    val df = spark.createDataFrame(
      spark.sparkContext.parallelize(data),
      StructType(schema)
    )

    // Initialize custom spark transformer
    val lc = new LengthCounter()
      .setInputCol("text")
      .setOutputCol("string_length")

    // Use transformer and extract length column
    val transformedDf = lc.transform(df)
    val lengths = transformedDf
      .select("string_length")
      .rdd.map(r => r.getInt(0))
      .collect.toList

    assert(lengths == List(50, 52))

  }

}
