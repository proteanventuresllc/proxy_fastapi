FROM python:3.10-alpine

ENV APP_HOME /app

WORKDIR $APP_HOME

COPY . ./

RUN pip install --no-cache-dir -r requirements.txt

CMD exec uvicorn proxy_src:app --host 0.0.0.0 --port 8080 --workers 1

