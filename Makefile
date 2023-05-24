build:
	docker-compose build

build-no-cache:
	@echo "--> Building Docker Base Image"
	DOCKER_BUILDKIT=0 docker build -f Docker/dev/Dockerfile . --no-cache
	@echo "--> Building Compose"
	DOCKER_BUILDKIT=0 COMPOSE_DOCKER_CLI_BUILD=1 docker-compose build

bash:
	@echo "--> Bash."
	docker-compose run bocuse-app bash

up:
	@echo "--> Up."
	docker-compose up

down:
	@echo "--> Down."
	docker-compose down --remove-orphans

test:
	docker-compose run bocuse-app pytest

lint:
	@echo "--> Lint"
	docker-compose run bocuse-app bash -c "./scripts/start-lint.sh"
