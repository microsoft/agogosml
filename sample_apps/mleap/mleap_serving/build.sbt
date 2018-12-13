scalaVersion := "2.11.0"

libraryDependencies ++= Seq(
  "com.github.finagle" %% "finch-core" % "0.22.0",
  "com.github.finagle" %% "finch-circe" % "0.22.0",
  "io.circe" %% "circe-generic" % "0.9.0",
  "com.google.code.gson" % "gson" % "2.8.0",
  "org.scalaj" %% "scalaj-http" % "2.4.1",
  "ml.combust.mleap" %% "mleap-runtime" % "0.12.0",
  "org.scalatest" %% "scalatest" % "3.0.5" % "test"
)

assemblyJarName in assembly := s"app-assembly.jar"

assemblyMergeStrategy in assembly := {
  case PathList("META-INF", xs @ _*) => MergeStrategy.discard
  case x => MergeStrategy.first
}

fork in Test := true

envVars in Test := Map("MODEL_PATH" -> sys.env.get("MODEL_PATH"))
envVars in Test := Map("PORT" -> sys.env.get("PORT"))
envVars in Test := Map("OUTPUT_URL" -> sys.env.get("OUTPUT_URL"))