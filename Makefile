SHELL := /bin/bash  # Use bash syntax

# Settings
# ===

# Default port for the dev server - can be overridden e.g.: "PORT=1234 make run"
ifeq ($(PORT),)
	PORT=8004
endif

# Settings
# ===
PROJECT_NAME=ubuntu-china
APP_IMAGE=${PROJECT_NAME}
SASS_CONTAINER=${PROJECT_NAME}-sass

# Help text
# ===

define HELP_TEXT

${PROJECT_NAME} - A Django website by the Canonical web team
===

Basic usage
---

> make run         # Prepare Docker images and run the Django site

Now browse to http://127.0.0.1:${PORT} to run the site

All commands
---

> make help               # This message
> make run                # build, watch-sass and run-site
> make it so              # a fun alias for "make run"
> make build-app-image    # Build the docker image
> make run-site           # Use Docker to run the website
> make watch-sass         # Setup the sass watcher, to compile CSS
> make compile-sass       # Setup the sass watcher, to compile CSS
> make stop-sass-watcher  # If the watcher is running in the background, stop it
> make clean              # Delete all created images and containers

(To understand commands in more details, simply read the Makefile)

endef

##
# Print help text
##
help:
	$(info ${HELP_TEXT})

##
# Use docker to run the sass watcher and the website
##
run:
	${MAKE} build-app-image
	${MAKE} watch-sass &
	${MAKE} run-site

##
# Build the docker image
##
build-app-image:
	docker build -t ${APP_IMAGE} .

##
# Run the Django site using the docker image
##
run-site:
	@echo ""
	@echo "======================================="
	@echo "Running server on http://127.0.0.1:${PORT}"
	@echo "======================================="
	@echo ""
	docker run -p 0.0.0.0:${PORT}:8000 -v `pwd`:/app -w=/app ${APP_IMAGE} ./manage.py runserver 0.0.0.0:8000

##
# Create or start the sass container, to rebuild sass files when there are changes
##
watch-sass:
	docker attach ${SASS_CONTAINER} || docker start -a ${SASS_CONTAINER} || docker run --name ${SASS_CONTAINER} -v `pwd`:/app ubuntudesign/sass sass --debug-info --watch /app/static/css

##
# Force a rebuild of the sass files
##
compile-sass:
	docker run -v `pwd`:/app ubuntudesign/sass sass --debug-info --update /app/static/css --force

##
# If the watcher is running in the background, stop it
##
stop-sass-watcher:
	docker stop ${SASS_CONTAINER}

##
# Re-create the app image (e.g. to update dependencies)
##
rebuild-app-image:
	-docker rmi -f ${APP_IMAGE}
	${MAKE} build-app-image

##
# Delete all created images and containers
##
clean:
	-docker rm -f ${SASS_CONTAINER}
	-docker rmi -f ${APP_IMAGE}

# The below targets
# are just there to allow you to type "make it so"
# as a replacement for "make develop"
# - Thanks to https://directory.canonical.com/list/ircnick/deadlight/

it:
so: run

# Phone targets (don't correspond to files or directories)
.PHONY: help build run run-site watch-sass compile-sass stop-sass-watcher rebuild-app-image it so
