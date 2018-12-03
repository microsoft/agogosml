name := "mleaplengthcounter"

version := "0.1"

scalaVersion := "2.11.8"


libraryDependencies += "ml.combust.mleap" %% "mleap-runtime" % "0.12.0"
libraryDependencies += "ml.combust.mleap" %% "mleap-core" % "0.12.0"
libraryDependencies += "ml.combust.mleap" %% "mleap-spark" % "0.12.0"

libraryDependencies ++= Seq(
  "org.apache.spark" %% "spark-core" % "2.3.0" % "provided",
  "org.apache.spark" %% "spark-mllib" % "2.3.0" % "provided"
)

assemblyJarName := "mleaplengthcounter.jar"

val meta = """META.INF(.)*""".r
assemblyMergeStrategy in assembly := {
  case PathList("javax", "servlet", xs @ _*) => MergeStrategy.first
  case PathList(ps @ _*) if ps.last endsWith ".html" => MergeStrategy.first
  case n if n.startsWith("reference.conf") => MergeStrategy.concat
  case n if n.endsWith(".conf") => MergeStrategy.concat
  case meta(_) => MergeStrategy.discard
  case x => MergeStrategy.first
}