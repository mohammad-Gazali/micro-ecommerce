FROM python:3.11.1-slim

COPY . /app

WORKDIR /app

# os-level installs (which is usually linux)
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    python3-dev \
    python3-setuptools \
    libpq-dev \ 
    gcc \
    make

# venv and python install packages
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/python -m pip install pip --upgrade && \
    /opt/venv/bin/python -m pip install -r ./requirements.txt

# purge unused
RUN apt-get remove -y --purge make gcc build-essential && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# running the entrypoint.sh file which is in "config" folder
RUN chmod +x ./config/entrypoint.sh

CMD ["./config/entrypoint.sh"]