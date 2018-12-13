.PHONY: requirements build_model deploy_resources deploy deploy_w_docker
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT


#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROFILE = default
PROJECT_NAME = microsoft-agogosml
PYTHON_INTERPRETER = python3
MODEL_TRAINER_JAR=trainer/target/scala-2.11/mleap_model_trainer.jar
DOCKER_DEPLOY_CONTAINER = devlace/agogos-mleapmodel
DATABRICKS_NOTEBOOKS_FOLDER = agogos

#################################################################################
# COMMANDS                                                                      #
#################################################################################

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

requirements: ## Install Python Dependencies
	pip install -U pip setuptools wheel
	pip install -r requirements.txt

$(MODEL_TRAINER_JAR): ## Builds scala jar with model
	(cd model/ && sbt clean assembly)

deploy_resources: $(MODEL_TRAINER_JAR) ## Deploy Azure infrastructure 
	databricks/deploy_resources.sh

deploy: deploy_resources ## Deploys entire solution 
	databricks/create_secrets.sh
	databricks/configure_databricks.sh

deploy_w_docker: ## Deploys entire solutions using Docker
	docker build -t $(DOCKER_DEPLOY_CONTAINER) -f Dockerfile .
	docker run -it $(DOCKER_DEPLOY_CONTAINER)
