
val sparkCore = "org.apache.spark" %% "spark-core" % "2.3.1"
val sparkSql = "org.apache.spark" %% "spark-sql" % "2.3.1"
val sparkMllib = "org.apache.spark" %% "spark-mllib" % "2.3.1"
val scalaTest = "org.scalatest" %% "scalatest" % "3.0.1"
val scalaCheck = "org.scalacheck" %% "scalacheck" % "1.13.4"
val sparkTest = "com.holdenkarau" %% "spark-testing-base" % "2.3.1_0.10.0"

lazy val assemblySettings = Seq(
  assemblyJarName in assembly := name.value + ".jar",
  assemblyMergeStrategy in assembly := {
    case PathList("javax", "servlet", xs @ _*) => MergeStrategy.first
    case PathList(ps @ _*) if ps.last endsWith ".html" => MergeStrategy.first
    case n if n.startsWith("reference.conf") => MergeStrategy.concat
    case n if n.endsWith(".conf") => MergeStrategy.concat
    case PathList("META-INF", xs @ _*)  => MergeStrategy.discard
    case x => MergeStrategy.first
  }
)

lazy val commonSettings = Seq(
  sparkVersion := "2.3.1",
  sparkComponents := Seq(),
  scalacOptions ++= Seq("-deprecation", "-unchecked"),
  pomIncludeRepository := { x => false },
  resolvers ++= Seq(
    "sonatype-releases" at "https://oss.sonatype.org/content/repositories/releases/",
    "Typesafe repository" at "http://repo.typesafe.com/typesafe/releases/",
    "Second Typesafe repo" at "http://repo.typesafe.com/typesafe/maven-releases/",
    Resolver.sonatypeRepo("public")
  )
)

lazy val root = (project in file("."))
  .aggregate(customTransformer)
  .dependsOn(customTransformer)
  .settings(
    commonSettings,
    assemblySettings,
    inThisBuild(List(
      organization := "com.Microsoft.agogosml",
      scalaVersion := "2.11.8"
    )),
    name := "mleap_model_trainer",
    version := "0.0.1",

    javacOptions ++= Seq("-source", "1.8", "-target", "1.8"),
    javaOptions ++= Seq("-Xms512M", "-Xmx2048M", "-XX:MaxPermSize=2048M", "-XX:+CMSClassUnloadingEnabled"),
    scalacOptions ++= Seq("-deprecation", "-unchecked"),
    parallelExecution in Test := false,
    fork := true,
    coverageHighlighting := true,
    libraryDependencies ++= Seq(
      sparkCore % "provided",
      sparkSql % "provided",
      sparkMllib % "provided",
      scalaTest % "test",
      scalaCheck % "test",
      sparkTest % "test"
    ),

    // uses compile classpath for the run task, including "provided" jar (cf http://stackoverflow.com/a/21803413/3827)
    run in Compile := Defaults.runTask(fullClasspath in Compile, mainClass in (Compile, run), runner in (Compile, run)).evaluated,

    // publish settings
    publishTo := {
      val nexus = "https://oss.sonatype.org/"
      if (isSnapshot.value)
        Some("snapshots" at nexus + "content/repositories/snapshots")
      else
        Some("releases"  at nexus + "service/local/staging/deploy/maven2")
    }
  )

lazy val customTransformer = (project in file("custom_transformer"))
  .settings(
    commonSettings,
    assemblySettings,
    name := "mleap_custom_transformer",
    version := "0.0.1",
    libraryDependencies ++= Seq(
      sparkCore % "provided",
      sparkMllib % "provided",
      scalaTest % "test",
      scalaCheck % "test",
      sparkTest % "test",
      "ml.combust.mleap" %% "mleap-runtime" % "0.12.0",
      "ml.combust.mleap" %% "mleap-core" % "0.12.0",
      "ml.combust.mleap" %% "mleap-spark" % "0.12.0"
    )
  )

