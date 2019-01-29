package ml.combust.mleap.core.feature

import ml.combust.mleap.core.Model
import ml.combust.mleap.core.types.{ScalarType, StructType}


case class LengthCounterModel() extends Model {
  def apply(word: String): Int = {
    word.length
  }

  override def inputSchema: StructType = StructType("input" -> ScalarType.String).get

  override def outputSchema: StructType = StructType("output" -> ScalarType.Int.nonNullable).get
}