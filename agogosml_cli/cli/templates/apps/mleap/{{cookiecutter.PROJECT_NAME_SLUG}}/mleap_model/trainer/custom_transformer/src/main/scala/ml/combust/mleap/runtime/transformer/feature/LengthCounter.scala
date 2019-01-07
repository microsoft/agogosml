package ml.combust.mleap.runtime.transformer.feature

import ml.combust.mleap.core.feature.LengthCounterModel
import ml.combust.mleap.core.types.NodeShape
import ml.combust.mleap.runtime.function.UserDefinedFunction
import ml.combust.mleap.runtime.frame.{SimpleTransformer, Transformer}


case class LengthCounter(override val uid: String = Transformer.uniqueName("length_counter"),
                     override val shape: NodeShape,
                     override val model: LengthCounterModel) extends SimpleTransformer {
  override val exec: UserDefinedFunction = (word: String) => model(word)
}