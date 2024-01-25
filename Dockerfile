FROM python:3.11

RUN mv .env_ .env

COPY ./requirements.txt /src/requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r /src/requirements.txt
COPY . /src

EXPOSE 8080

WORKDIR /src

CMD ["python", "server.py"]

