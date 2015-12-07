FROM ubuntudesign/python-auth

# System dependencies
RUN apt-get update && apt-get install -y graphviz-dev gettext

# Pip requirements files
ADD requirements /requirements

# Install pip requirements
RUN pip install -r /requirements/dev.txt

ADD . /srv
WORKDIR /srv

ENV DJANGO_SETTINGS_MODULE website.dev_settings
CMD ["python", "manage.py", "runserver_plus", "0.0.0.0:5000"]

