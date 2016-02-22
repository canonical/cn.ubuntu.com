FROM ubuntudesign/python-auth

# System dependencies
RUN apt-get update && apt-get install -y graphviz-dev gettext netcat

# Pip requirements files
ADD requirements /requirements

# Install pip requirements
RUN pip install -r /requirements/dev.txt

ADD . /srv
WORKDIR /srv

ENV DJANGO_SETTINGS_MODULE website.dev_settings
CMD ["./provision-and-run.sh"]
