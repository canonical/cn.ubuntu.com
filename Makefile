SHELL := /bin/bash

define HELP_TEXT
Ubuntu-china.cn website project
===

Usage:

> make run         # Prepare Docker images and run the Django site

# or, if you want more control
> make build       # Build the ubuntu-china docker image
> make watch-sass  # Setup the sass watcher, to compile CSS
> make run-site    # Use Docker to run the website

endef

# Variables
##

dependency_repo="lp:~webteam-backend/ubuntu-chinese-website/dependencies"

ifeq ($(PORT),)
	PORT=8004
endif

# Phone targets (don't correspond to files or directories)
.PHONY: help build run run-site watch-sass pip-cache rebuild-dependencies-cache
.PHONY: clean clean-all clean-pip-cache it so

help:
	$(info ${HELP_TEXT})

# Use docker to run the sass watcher and the website
run:
	${MAKE} build
	${MAKE} watch-sass &
	${MAKE} run-site

# Build the ubuntu-china docker image
build:
	docker build -t ubuntu-china .

# Run the Django site using the docker image
run-site:
	docker run -p 0.0.0.0:${PORT}:8000 -v `pwd`:/app -w=/app ubuntu-china ./manage.py runserver 0.0.0.0:8000

# Watch sass using our sass docker image
watch-sass:
	docker run -v `pwd`:/app ubuntudesign/sass sass --debug-info --watch /app/static/css

##
# Targets for deployment
##

# Update the pip cache
pip-cache:
	if [ -d pip-cache ]; then \
	    bzr pull --directory pip-cache --overwrite ${dependency_repo}; \
	else \
	    bzr branch ${dependency_repo} pip-cache; \
	fi

# Rebuild the pip requirements cache, for non-internet-visible builds
rebuild-dependencies-cache:
	${MAKE} pip-cache
	pip install --exists-action=w --download pip-cache/ -r requirements/standard.txt
	bzr commit pip-cache/ -m 'automatically updated ubuntu-china requirements'
	bzr push --directory pip-cache ${dependency_repo}
	$(MAKE) clean-pip-cache

# Delete any generated files that effect the site
clean:
	rm -rf env .sass-cache
	find static/css -name '*.css*' -exec rm {} +  # Remove any .css files - should only be .sass files

# Also delete pip-cache
clean-all: clean clean-pip-cache

# Clean pip-cache
clean-pip-cache:
	rm -rf pip-cache src/

# The below targets
# are just there to allow you to type "make it so"
# as a replacement for "make develop"
# - Thanks to https://directory.canonical.com/list/ircnick/deadlight/

it:	
	${MAKE} watch-sass &

so: run-site
