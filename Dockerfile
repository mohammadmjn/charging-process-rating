FROM python:3.9-alpine

ENV PYTHONUNBUFFERED True

ENV RUNTIME_LOG=runtime.log
ENV MAX_CONTENT_LENGTH=2

RUN python -m pip install --upgrade pip
COPY requirements.txt /
RUN pip install -r requirements.txt

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

EXPOSE 5000
ENV PORT 5000

CMD exec gunicorn --bind :$PORT --workers 3 --timeout 0 --preload server:app
