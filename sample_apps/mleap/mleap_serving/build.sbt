scalaVersion := "2.11.0"

libraryDependencies ++= Seq(
  "com.github.finagle" %% "finch-core" % "0.22.0",
  "com.github.finagle" %% "finch-circe" % "0.22.0",
  "io.circe" %% "circe-generic" % "0.9.0",
  "com.google.code.gson" % "gson" % "2.8.0",
  "org.scalaj" %% "scalaj-http" % "2.4.1",
  "ml.combust.mleap" %% "mleap-runtime" % "0.12.0"
)