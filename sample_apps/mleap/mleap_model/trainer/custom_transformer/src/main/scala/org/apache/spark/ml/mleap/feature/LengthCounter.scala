package org.apache.spark.ml.mleap.feature

import ml.combust.mleap.core.feature.LengthCounterModel
import org.apache.spark.annotation.DeveloperApi
import org.apache.spark.ml.Transformer
import org.apache.spark.ml.param.ParamMap
import org.apache.spark.ml.param.shared.{HasInputCol, HasOutputCol}
import org.apache.spark.ml.util.Identifiable
import org.apache.spark.sql.functions._
import org.apache.spark.sql.{DataFrame, Dataset}
import org.apache.spark.sql.types._


class LengthCounter(override val uid: String,
                val model: LengthCounterModel) extends Transformer
  with HasInputCol
  with HasOutputCol {
  def this(model: LengthCounterModel) = this(uid = Identifiable.randomUID("length_counter"), model = model)
  def this() = this(uid = Identifiable.randomUID("length_counter"), model = new LengthCounterModel())
  def this(uid: String) = this(model = new LengthCounterModel())

  def setInputCol(value: String): this.type = set(inputCol, value)
  def setOutputCol(value: String): this.type = set(outputCol, value)

  @org.apache.spark.annotation.Since("2.0.0")
  override def transform(dataset: Dataset[_]): DataFrame = {
    val lengthCounterUdf = udf {
      (word: String) => model(word)
    }

    dataset.withColumn($(outputCol), lengthCounterUdf(dataset($(inputCol))))
  }

  override def copy(extra: ParamMap): Transformer =
    copyValues(new LengthCounter(uid, model), extra)

  @DeveloperApi
  override def transformSchema(schema: StructType): StructType = {
    require(schema($(inputCol)).dataType.isInstanceOf[StringType],
      s"Input column must be of type StringType but got ${schema($(inputCol)).dataType}")
    val inputFields = schema.fields
    require(!inputFields.exists(_.name == $(outputCol)),
      s"Output column ${$(outputCol)} already exists.")

    StructType(schema.fields :+ StructField($(outputCol), DoubleType))
  }
}
