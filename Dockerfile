FROM ubuntudesign/python-auth

# Pip requirements files
ADD requirements /requirements

# Install pip requirements
RUN pip install -r /requirements/dev.txt
