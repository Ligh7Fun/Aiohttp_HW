FROM python:3.11

RUN apt-get update && \
    apt-get install -y python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN if [ -e .env_ ]; then mv .env_ .env; fi

COPY ./requirements.txt /src/requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r /src/requirements.txt
COPY . /src

EXPOSE 8080

WORKDIR /src

CMD ["python", "server.py"]

