package ml.combust.mleap.runtime.transformer.feature

import ml.combust.mleap.core.types.{NodeShape, ScalarType, StructField, StructType}
import ml.combust.mleap.runtime.frame.{DefaultLeapFrame, Row}
import ml.combust.mleap.core.feature.LengthCounterModel
import org.scalatest.FunSuite

class LengthCounterTest extends FunSuite {

  test("Mleap custom transformer (LengthCounter) functions properly") {
    // Create leapFrame
    val schema: StructType = StructType(
      StructField("text", ScalarType.String)).get
    val dataset = Seq(
      Row("Don't stop me now"),
      Row("cause I'm having a good time"))
    val leapFrame = DefaultLeapFrame(schema, dataset)

    // Instantiate LengthCounter model
    val lc = new LengthCounter(shape = NodeShape()
        .withStandardInput("text")
        .withStandardOutput("string_length"),
      model = LengthCounterModel())

    // Transform our leap frame using the LengthCounter transformer
    val lengths = (for(lf <- lc.transform(leapFrame);
                       lf2 <- lf.select("string_length")) yield {
      lf2.dataset.map(_.getInt(0))
    }).get

    assert(lengths == List(17, 28))
  }

}
