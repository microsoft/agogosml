Quick Links
-----------

-  `Intro <#Intro>`__
-  `Contributing <./CONTRIBUTING.md>`__
-  `License <./LICENSE>`__
-  `Microsoft Open Source Code of
   Conduct <https://opensource.microsoft.com/codeofconduct/>`__
-  `Backlog <https://waffle.io/Microsoft/agogosml>`__
-  `Design and Architecture <./docs/assets/design/README.md>`__

Intro
-----

agogosml is a data processing pipeline project that addresses the common
need for operationalizing ML models. This covers the complete workflow
of training, deploying, scoring and monitoring the models in production
at scale. The key focus will be on production ready re-training and
scoring. The taken approach will be agnostic to the data science
workflow of building the models, but the initial project will be scoped
towards traditional ML techniques (non deep-learning) but might be
extended when required/requested through additional customer
engagements. Key functionality split into four milestones:

Milestone 0: Automated data processing pipeline
-----------------------------------------------

-  Re-usable/canonical data processing pipeline supporting multiple data
   streaming technologies (Kafka, Spark Structured Streaming,
   EventHub,…. ) as well as different choices for deploying the backend
   services (K8s, Serverless, …)
-  CI/CD pipeline to deploy versioned and immutable pipeline
-  Blue/Green deployments, automatic role-backs or redeployment of a
   specific version

Milestone 1: Automated ML pipeline
----------------------------------

-  Automated model training, testing, deploying and scoring
-  Model scoring at scale leveraging micro services/containers
-  Green/Blue testing and deployment role-backs

Milestone 2: Model logging and monitoring
-----------------------------------------

-  Dashboard to explore real-time and historical model input,
   predictions and performance
-  Model monitoring to detect unexpected changes in input data and
   predictions
-  Triggers to take actions if input or predictions diverge from
   expected ranges

Milestone 3: GDPR compliant ML pipeline
---------------------------------------

-  Anonymize/remove PII data and keep track of PII data used for model
   training
-  Revoke and retrain models if certain records need to be removed due
   to customers that want their data revoked

Related projects and useful resources
-------------------------------------

-  https://github.com/jakkaj/ravenswood
-  https://github.com/jakkaj/ml-train-deploy-vsts-k8s
-  https://github.com/Microsoft/presidio
-  https://github.com/timfpark/topological
-  https://github.com/lawrencegripper/ion
-  https://github.com/Azure/AI-predictivemaintenance and `this
   page <https://na01.safelinks.protection.outlook.com/?url=https%3A%2F%2Fgithub.com%2FAzure%2FAI-PredictiveMaintenance%2Ftree%2Fmaster%2Fdocs&data=02%7C01%7C%7C0bc38fbfbe0e45b9364e08d60ecfc936%7C72f988bf86f141af91ab2d7cd011db47%7C1%7C0%7C636712682921627767&sdata=CXvxvfzl%2FnoLlIZV7p7LBQTyzJdrL8rvwYlDxB5CsQE%3D&reserved=0>`__
   shows the modeling pipeline and the operationalized pipeline.
-  `Case Study on fraud
   detection <https://azure.microsoft.com/en-us/blog/two-seconds-to-take-a-bite-out-of-mobile-bank-fraud-with-artificial-intelligence/>`__

## Steps to run

### Making tests run

```
cd agogosml
# install dependencies in the virtual environment
pipenv install && pipenv install --dev
# installs agogosml locally
pipenv run python setup.py install
# run the tests
pipenv run make test
```

