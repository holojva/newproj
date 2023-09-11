# Берем образ пайтон 
FROM python:3.9.5-alpine

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Устанавливаем необходимые модули
RUN pip install --upgrade pip
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Входная точка в контейнер
COPY ./entrypoint.sh /app/entrypoint.sh
COPY . /app/
ENTRYPOINT [ "/app/entrypoint.sh" ]