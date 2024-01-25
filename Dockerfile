FROM python:3.11

RUN apt-get update && \
    apt-get install -y python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# RUN echo "PG_HOST=localhost\nPG_PORT=5432\nPG_USER=ads\nPG_PASSWORD=adsads123\nPG_DATABASE=ads" > .env

COPY ./requirements.txt /src/requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r /src/requirements.txt
COPY . /src

EXPOSE 8080

WORKDIR /src

CMD ["python", "server.py"]

