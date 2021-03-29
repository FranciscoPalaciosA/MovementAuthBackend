FROM continuumio/miniconda3 AS build

# Create environment as normal
ADD environment.yml /tmp/environment.yml
RUN conda env create -f /tmp/environment.yml

# Install conda-pack:
RUN conda install -c conda-forge conda-pack

# Use conda-pack to create a standalone enviornment
# in /venv:
RUN conda-pack -n MovementAuthBackend -o /tmp/env.tar && \
  mkdir /venv && cd /venv && tar xf /tmp/env.tar && \
  rm /tmp/env.tar

# We've put venv in same path it'll be in final image,
# so now fix up paths:
RUN /venv/bin/conda-unpack

FROM debian:buster AS runtime

# Copy /venv from the previous stage:
COPY --from=build /venv /venv

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy data from current repo
COPY . /
SHELL ["/bin/bash", "-c"]

# The code to run when container is started:

# Change server timezone
RUN cp /usr/share/zoneinfo/America/Los_Angeles /etc/localtime
# Create directories
RUN mkdir soilGrib && mkdir temp && mkdir data

# ENTRYPOINT ["conda", "run", "-n", "apienv", "gunicorn", "-c", "./gunicorn.config.py","--timeout","60", "run:app"]
ENTRYPOINT source /venv/bin/activate && gunicorn --bind :$PORT -c ./gunicorn.config.py --timeout 60 app:app