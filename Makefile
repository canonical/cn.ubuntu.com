SHELL := /bin/bash  # Use bash syntax

export COMPOSE_PROJECT_NAME ?= $(shell echo $(subst .,,$(subst _,,$(subst -,,$(shell basename `pwd`)))) | tr A-Z a-z)
export COMPOSE_FILE ?= docker-compose.makefile.yml
export PORT ?= 8010

DOCKER_IP := 127.0.0.1
ifdef DOCKER_HOST
	DOCKER_IP := $(shell echo ${DOCKER_HOST} | perl -nle'print $$& if m{(\d+\.){3}\d+}')
endif

# Help text
# ===

define HELP_TEXT

cn.ubuntu.com - A Django website by the Canonical web team
===

Basic usage
---

> make run  # Prepare and run all services, to serve the site locally

Now browse to http://127.0.0.1:${PORT} to run the site

All commands
---

> make help               # This message
> make run                # Build, watch-sass and run-site (in background)
> make stop               # Stop all running images
> make logs               # Watch the logs for the site
> make db-update          # Migrate database to latest app code
> make clean-images       # Delete all created images and containers
> make clean-css          # Delete compiled css
> make clean-npm          # Delete node_modules
> make clean-all          # Run all clean commands
> make export-page        # Export JSON data for a local CMS page and create a DB migration to import/overwrite that page
> make it so              # A fun alias for "make run"

(To understand commands in more details, simply read the Makefile)

endef

# Print help text
help:
	$(info ${HELP_TEXT})

run:
	docker-compose up -d
	@echo -e "==\nServer running at: http://${DOCKER_IP}:${PORT}\n=="

stop:
	docker-compose stop -t 3

logs:
	docker-compose logs

db-update:
	docker-compose run web python manage.py migrate --noinput

clean-css:
	docker-compose run sass rm -f static/css/*.css

clean-images:
	docker-compose kill
	docker-compose rm -f
	docker rmi -f ${COMPOSE_PROJECT_NAME}_web || true

clean-npm:
	docker-compose run npm rm -rf node_modules

clean-all:
	${MAKE} clean-css
	${MAKE} clean-npm
	${MAKE} clean-images

# Given a URL, export the page data for that URL as JSON
export-page:
	@read -p "Enter page URL path (without preceding slash): " url; \
	if [[ -n "$${url}" ]]; then \
		echo "Exporting to website/page-data/$${url}.json"; \
		data=$$(docker-compose run web ./manage.py export-page-json $${url}); \
		if [[ $$? > 0 ]]; then echo -e "ERROR:\n$${data}"; exit 1; \
		else echo "$${data}" > website/page-data/$${url}.json; fi; \
		echo "Creating migration for $${url}"; \
		docker-compose run web ./manage.py create-page-migration $${url} website/page-data/$${url}.json; \
	fi

it:
so: run
