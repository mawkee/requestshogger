# requestshogger.Dockerfile
FROM debian:11-slim AS build

RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes python3-venv && \
    python3 -m venv /venv && \
    /venv/bin/pip3 install --upgrade pip

# Build the virtualenv as a separate step
# It will only re-execute this step when requirements.txt changes
FROM build AS build-venv

COPY requirements.txt /requirements.txt
RUN /venv/bin/pip3 install --disable-pip-version-check -U -r /requirements.txt

# Copy the virtualenv into a distroless image
FROM gcr.io/distroless/python3-debian11
COPY --from=build-venv /venv /venv
COPY hogger /app/hogger
WORKDIR /app

# Don't bind to a specific address
ENV HOGGER_HOST="0.0.0.0"

# Executing Hogger
ENTRYPOINT ["/venv/bin/python", "/app/hogger/reqhogger.py"]

EXPOSE 8910
