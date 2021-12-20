.PHONY: build

SHELL := /bin/bash
IMAGENAME=deepurbanism-cms
VERSION=0.1.4
GH_ORG=cividi
APPLIED_VERSION=0.1.3

build: ## Build the Docker images
	docker buildx build --platform linux/amd64,linux/arm64 -t ghcr.io/$(GH_ORG)/$(IMAGENAME):latest -t ghcr.io/$(GH_ORG)/$(IMAGENAME):$(VERSION) --push ./django
	# docker-compose -p wagtail_grapple build

build-staging:
	docker buildx build --platform linux/amd64,linux/arm64 -t ghcr.io/$(GH_ORG)/$(IMAGENAME):latest --push ./django

build-dev:
	docker buildx build --platform linux/amd64,linux/arm64 -t ghcr.io/$(GH_ORG)/$(IMAGENAME):dev --push --build-arg ENVIRONMENT=dev ./django
	# docker-compose -p wagtail_grapple build

build-dev-local:
	docker buildx build --platform linux/arm64 -t ghcr.io/$(GH_ORG)/$(IMAGENAME):dev --load --build-arg ENVIRONMENT=dev ./django

up: ## Bring the  Docker containers up
	docker-compose -p wagtail_grapple up -d --no-build || echo 'Already up!'

upwin:  ## Bring the Docker container up for bash on ubuntu folk
	export WINDIR="$(subst /mnt/c,//c,$(CURDIR))/" && make up

lint: build ## Lint the python code.
	docker run -v $(CURDIR)/django:/app $(IMAGENAME) /bin/bash -c 'flake8 website'

down: ## Stop the backend Docker container
	docker-compose -p wagtail_grapple stop

enter: ## Enter backend container
	docker exec -it wagtail_grapple_backend_1 /bin/bash

clean: ## Stop and remove all Docker containers
	docker-compose down

destroy: ## Remove all our Docker images
	docker rmi -f ghcr.io/cividi/wagtail_grapple:dev

refresh: clean up enter
	## Let's start again

migrate:
	docker run --rm --env-file ${ENV} ghcr.io/$(GH_ORG)/$(IMAGENAME):$(APPLIED_VERSION) sh -c "cd wagtail_vue && python manage.py makemigrations && python manage.py migrate"

createsuperuser:
	docker run -it --rm --env-file ${ENV} ghcr.io/$(GH_ORG)/$(IMAGENAME):$(APPLIED_VERSION) sh -c "cd wagtail_vue && python manage.py createsuperuser"

init:
	docker run --rm --env-file ${ENV} ghcr.io/$(GH_ORG)/$(IMAGENAME):$(APPLIED_VERSION) sh -c "cd wagtail_vue && python manage.py collectstatic --noinput"