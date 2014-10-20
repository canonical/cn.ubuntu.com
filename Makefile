SHELL := /bin/bash

define HELP_TEXT
Ubuntu-china.cn website project
===

Usage:

> make setup    # Install dependencies
> make develop  # Auto-compile sass files and run the dev server

endef

# Variables
##

ENVPATH=${VIRTUAL_ENV}
DEPENDENCIES_REPOSITORY="bzr branch lp:~webteam-backend/ubuntu-chinese-website/dependencies pip-cache"
VEX=vex --path ${ENVPATH}

ifeq ($(ENVPATH),)
	ENVPATH=env
endif

ifeq ($(PORT),)
	PORT=8004
endif

# Phone targets (don't correspond to files or directories)
.PHONY: help develop setup dev-server watch-sass sass update-env create-env
.PHONY: install-requirements install-dependencies apt-dependencies brew-dependencies
.PHONY: clean clean-all rebuild-dependencies-cache 

help:
	$(info ${HELP_TEXT})

##
# Start the development server
##
develop:
	$(MAKE) watch-sass &
	$(MAKE) dev-server

##
# Prepare the project
##
setup: install-dependencies update-env

##
# Run server
##
dev-server:
	${VEX} ./manage.py runserver_plus 0.0.0.0:${PORT}

##
# Run SASS watcher
##
watch-sass:
	sass --debug-info --watch static/css/

##
# Build SASS
##
sass:
	sass --force --style compressed --update static/css

##
# Get virtualenv ready
##
update-env:
	${MAKE} create-env

	${VEX} ${MAKE} install-requirements

##
# Make virtualenv directory if it doesn't exist and we're not in an env
##
create-env:
	if [ ! -d ${ENVPATH} ]; then virtualenv ${ENVPATH}; fi

##
# Install pip requirements
# Only if inside a virtualenv
##
install-requirements:
	if [ "${VIRTUAL_ENV}" ]; then pip install --exists-action=w -r requirements/dev.txt; fi

##
# Install required system dependencies
##
install-dependencies:
	if [ $$(command -v apt-get) ]; then ${MAKE} apt-dependencies; fi
	if [ $$(command -v brew) ]; then ${MAKE} brew-dependencies; fi

	if [ ! $$(command -v virtualenv) ]; then sudo pip install virtualenv; fi
	if [ ! $$(command -v vex) ]; then sudo pip install vex; fi

## Install dependencies with apt
apt-dependencies:
	if [ ! $$(command -v pip) ]; then sudo apt-get install python-pip; fi
	if [ ! $$(command -v sass) ]; then sudo apt-get install ruby-sass; fi

## Install dependencies with brew
brew-dependencies:
	if [ ! $$(command -v pip) ]; then sudo easy_install pip; fi
	if [ ! $$(command -v sass) ]; then sudo gem install sass; fi

##
# Clean mojo
##
pip-cache:
	if bzr info pip-cache > /dev/null 2>&1; then \
		bzr branch ${DEPENDENCIES_REPOSITORY} pip-cache; \
	else \
		bzr pull --directory pip-cache; \
	fi

##
# Rebuild the pip requirements cache, for non-internet-visible builds
##
rebuild-dependencies-cache:
	$(MAKE) pip-cache
	pip install --exists-action=w --download pip-cache/ -r requirements/standard.txt
	bzr commit pip-cache/ -m 'automatically updated ubuntu-china requirements'
	bzr push --directory pip-cache lp:~webteam-backend/ubuntu-chinese-website/dependencies
	$(MAKE) clean-pip-cache

##
# For dokku - build sass and run gunicorn
##
dokku-start: sass gunicorn

##
# Run the gunicorn app
##
gunicorn:
	gunicorn webapp.wsgi

##
# Delete any generated files that effect the site
##
clean:
	rm -rf env .sass-cache
	find static/css -name '*.css*' -exec rm {} +  # Remove any .css files - should only be .sass files

##
# Also delete pip-cache
##
clean-all: clean clean-pip-cache

##
# Clean pip-cache
##
clean-pip-cache:
	rm -rf pip-cache src/

# The below targets
# are just there to allow you to type "make it so"
# as a replacement for "make develop"
# - Thanks to https://directory.canonical.com/list/ircnick/deadlight/

it:
	$(MAKE) watch-sass &

so: dev-server
