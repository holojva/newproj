FROM python:3.9.5-alpine

WORKDIR /app

RUN pip install --upgrade pip
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

#entry point
COPY ./entrypoint.sh /app/entrypoint.sh
COPY . /app/
ENTRYPOINT ["/app/entrypoint.sh"]
