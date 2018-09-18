

## Quick Links

- [Intro](#Intro)
- [Contributing](./CONTRIBUTING.md)
- [License](./LICENSE.md)
- [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/)
  
## Intro
agogosml is a data processing pipeline project that addresses the common need for operationalizing ML models. This covers the complete workflow of training, deploying, scoring and monitoring the models in production at scale. The key focus will be on production ready re-training and scoring. The taken approach will be agnostic to the data science workflow of building the models, but the initial project will be scoped towards traditional ML techniques (non deep-learning) but might be extended when required/requested through additional customer engagements.
Key functionality split into four milestones:

## Milestone 0: Automated data processing pipeline
-	Re-usable/canonical data processing pipeline supporting multiple data streaming technologies (Kafka, Spark Structured Streaming, EventHub,…. ) as well as different choices for deploying the backend services (K8s, Serverless, …)
-	CI/CD pipeline to deploy versioned and immutable pipeline 
-	Blue/Green deployments, automatic role-backs or redeployment of a specific version

## Milestone 1: Automated ML pipeline
-	Automated model training, testing, deploying and scoring 
-	Model scoring at scale leveraging micro services/containers
-	Green/Blue testing and deployment role-backs

## Milestone 2: Model logging and monitoring
-	Dashboard to explore real-time and historical model input, predictions and performance 
-	Model monitoring to detect unexpected changes in input data and predictions
-	Triggers to take actions if input or predictions diverge from expected ranges

## Milestone 3: GDPR compliant ML pipeline
-	Anonymize/remove PII data and keep track of PII data used for model training
-	Revoke and retrain models if certain records need to be removed due to customers that want their data revoked 

