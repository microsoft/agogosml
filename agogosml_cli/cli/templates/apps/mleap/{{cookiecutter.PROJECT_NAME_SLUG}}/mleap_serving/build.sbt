scalaVersion := "2.11.0"

resolvers += "Typesafe repository" at "http://repo.typesafe.com/typesafe/releases/"

libraryDependencies ++= Seq(
    "com.github.finagle" %% "finch-core" % "0.22.0",
    "com.github.finagle" %% "finch-circe" % "0.22.0",
    "io.circe" %% "circe-generic" % "0.9.0",
    "com.google.code.gson" % "gson" % "2.8.0",
    "org.scalaj" %% "scalaj-http" % "2.4.1",
    "ml.combust.mleap" %% "mleap-runtime" % "0.12.0",
    "org.scalatest" %% "scalatest" % "3.0.5" % "test",
    "org.slf4j" % "slf4j-jdk14" % "1.7.25",
    "com.typesafe.play" % "play-json_2.11" % "2.4.6"
)

envVars in test / assembly := Map(
  "MODEL_PATH" -> sys.env.get("MODEL_PATH").get,
  "PORT" -> sys.env.get("PORT").get,
  "OUTPUT_URL" -> sys.env.get("OUTPUT_URL").get
)

fork in test := true

assemblyJarName in assembly := "app-assembly.jar"

assemblyMergeStrategy in assembly := {
  case PathList("META-INF", xs @ _*) => MergeStrategy.discard
  case x => MergeStrategy.first
}