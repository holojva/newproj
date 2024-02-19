FROM python:3.9.5
# set work directory
WORKDIR /usr/src/app/
# copy project
COPY . /usr/src/app/
# install dependencies
RUN pip install --user pyTelegramBotAPI
# run app
CMD ["python", "bot.py"]