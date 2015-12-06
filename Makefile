SHELL := /bin/bash  # Use bash syntax

# Settings
# ===

# Default port for the dev server - can be overridden e.g.: "PORT=1234 make run"
ifeq ($(PORT),)
	PORT=8010
endif

# Settings
# ===
PROJECT_NAME=ubuntu-china
PROJECT_DIR=$(shell basename `pwd`)
DOCKER_PROJECT_NAME := $(subst _,,$(subst -,,$(PROJECT_DIR)))
APP_IMAGE=${DOCKER_PROJECT_NAME}_web
DB_CONTAINER=${DOCKER_PROJECT_NAME}_db_1
SASS_CONTAINER=${DOCKER_PROJECT_NAME}_sass_1

# Help text
# ===

define HELP_TEXT

${PROJECT_NAME} - A Django website by the Canonical web team
===

Basic usage
---

> make run  # Prepare and run all services, to serve the site locally

Now browse to http://127.0.0.1:${PORT} to run the site

All commands
---

> make help                      # Print help text (this message)
> make run                       # Prepare and run all services, to serve the site locally
> make stop                      # Stop all running services
> make logs                      # Watch the logs from all running services
> make sass-watch                # Start the sass-watch container
> make sass-compile              # Use the sass container to compile all sass files
> make app-build                 # (Re-)build the application image, in which the web container is based
> make app-update-requirements   # Update pip requirements in the app image
> make db-start                  # Start the database service
> make db-stop                   # Stop the database service
> make db-reset                  # Re-create the database from scratch (discards existing data)
> make db-update                 # Update the database from local fixtures
> make db-connect                # Connect to the database to hack around with it
> make export-page               # Given a URL, export the page data for that URL as JSON
> make import-new-pages          # Import pages from the existing JSON data
> make clean-css                 # Delete any compiled CSS files
> make clean-db                  # Remove the database and web containers (discards existing data)
> make clean-web                 # Remove the web container (doesn't remove the application image)
> make clean-app                 # Remove the application image and the web container
> make clean-containers          # Remove all containers (but not the application image)
> make clean-all                 # Remove everything - containers (incl. database), images, CSS
> make it so                     # a fun alias for "make run" (Karl)

(To understand commands in more details, simply read the Makefile)

endef

# Print help text
help:
	$(info ${HELP_TEXT})

# Prepare and run web, sass and database
run:
	# Make sure IP is correct for mac etc.
	$(eval docker_ip := `hash boot2docker 2> /dev/null && echo "\`boot2docker ip\`" || echo "127.0.0.1"`)
	if [[ -z "`docker images -q ubuntudesign/python-auth`" ]]; then docker pull ubuntudesign/python-auth; fi
	@docker-compose up -d db

	@echo ""
	@echo "== Updating DB =="
	@echo ""
	${MAKE} db-update
	@echo ""
	@echo "== DB Ready =="
	@echo ""

	@docker-compose up -d web     # Run Django
	@echo ""
	@echo "== Running server on http://${docker_ip}:${PORT} =="
	@echo ""

	@echo "== Building SCSS =="
	@echo ""
	@docker-compose up sass           # Build CSS into `static/css`
	@docker-compose up -t 1 -d sass-watch  # Watch SCSS files for changes
	@echo ""
	@echo "== Built SCSS =="
	@echo ""

	@echo ""
	@echo "======================================="
	@echo "Running server on http://${docker_ip}:${PORT}"
	@echo "To stop the server, run 'make stop'"
	@echo "To get server logs, run 'make logs'"
	@echo "======================================="
	@echo ""

# Stop all running services
stop:
	@docker-compose stop -t 5

# Watch the logs from all running services
logs:
	@docker-compose logs

# Start the sass-watch container
sass-watch:
	docker-compose up -d sass-watch

# Use the sass container to compile all sass files
sass-compile:
	docker-compose up sass

# (Re-)build the application image, in which the web container is based
app-build:
	rm -rf .sass-cache
	docker-compose build web

# Update the database from local fixtures
app-update-requirements:
	docker exec $$(docker-compose ps -q web) pip install --upgrade --requirement requirements/dev.txt

# Start the database service
db-start:
	docker-compose up -d db

# Stop the database service
db-stop:
	docker-compose stop -t 5 db

# Re-create the database from scratch (discards existing data)
db-reset:
	${MAKE} clean-db
	${MAKE} db-start
	${MAKE} db-update

# Update the database from local fixtures
db-update:
	# Wait for DB to be ready
	docker run --link $$(docker-compose ps -q db):db aanand/wait
	docker-compose run web python manage.py migrate --noinput
	docker-compose run web python manage.py loaddata cms.json

# Connect to the database to hack around with it
db-connect:
	docker run -it --link ${DB_CONTAINER}:postgres --rm postgres sh -c 'exec psql -h "$$POSTGRES_PORT_5432_TCP_ADDR" -p "$$POSTGRES_PORT_5432_TCP_PORT" -U postgres'

# Given a URL, export the page data for that URL as JSON
export-page:
	@read -p "Enter page URL path (without preceding slash): " url; \
	if [[ -n "$${url}" ]]; then \
		docker-compose run web ./manage.py export-page $${url}; \
	fi

# Delete any compiled CSS files
clean-css:
	rm -rf .sass-cache
	find . -name 'statis/css/*.css' | xargs rm -f

# Remove the database container (discards existing data, and deletes web as well)
clean-db:
	docker-compose kill db web
	docker-compose rm -f db
	docker-compose rm -f web

# Remove the web container (doesn't remove the application image)
clean-web:
	docker-compose kill web
	docker-compose rm -f web

# Remove the application image and the web container
clean-app:
	${MAKE} clean-web
	# If image exists, delete it
	if [[ -n $$(docker images -q ${APP_IMAGE}) ]]; then docker rmi -f ${APP_IMAGE}; fi

# Remove all containers (discards existing data, but not the application image)
clean-containers:
	docker-compose kill
	docker-compose rm -f

# Remove everything - containers (incl. database), images, CSS
clean-all:
	${MAKE} clean-css
	${MAKE} clean-containers
	${MAKE} clean-app

##
# "make it so" alias for "make run" (thanks @karlwilliams)
##
it:
so: run

# Phone targets (don't correspond to files or directories)
.PHONY: help run stop logs sass-watch sass-compile app-build app-update-requirements db-start db-stop db-reset db-update db-connect clean-css clean-db clean-web clean-app clean-containers clean-all it so run
