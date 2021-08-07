FULLBRANCH= $(shell git branch --show-current)
BRANCH=$(shell echo $(FULLBRANCH) | cut -d '/' -f2)

clean:
	rm -rf .pytest_cache .coverage

install:
	pipenv install --dev --ignore-pipfile

update:
	pipenv update --dev
	pipenv check
	pipenv graph

test: clean
	pipenv run flake8
	pipenv run pytest --cov app --cov-report term-missing

makemigrations:
	cd src && pipenv run python manage.py makemigrations

migrate:
	cd src && pipenv run python manage.py migrate

createsuperuser:
	cd src && pipenv run python manage.py createsuperuser

run:
	DOCKER_BUILDKIT=0 docker-compose up --build

deploy-infra:
	cd deployment && terraform init -var branch=$(BRANCH) && terraform apply -var branch=$(BRANCH) -input=false -auto-approve -target=module.infrastructure

deploy-rds:
	cd deployment && terraform init -var branch=$(BRANCH) && terraform apply -var branch=$(BRANCH) -input=false -auto-approve -target=module.rds

deploy-app:
	docker build -t cookiehook/titancraft:$(BRANCH) .
	docker push cookiehook/titancraft:$(BRANCH)
	cd deployment && terraform init -var branch=$(BRANCH) && terraform apply -var branch=$(BRANCH) -input=false -auto-approve -target=module.app

destroy-app:
	cd deployment && terraform init -var branch=$(BRANCH) && terraform destroy -var branch=$(BRANCH) -target=module.app
