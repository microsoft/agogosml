# Agogosml Test Generator 

This package generates end-to-end tests for Agogosml's CI/CD pipeline to be able to test your custom data pipeline.
The package also provides a method to allow you to load your own unit tests and integration tests directly into Agogosml's CI/CD pipeline.

To use this test generator, you would need to provide a valid JSON file describing the tests and plugins for Agogosml to load and run.

### Validating your Test JSON File

To validate your Test JSON file, you can clone this repository, run `npm install` and execute `npm run validate-schema JSONFILE.JSON`

