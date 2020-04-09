FROM python:3.6

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update -y
RUN apt-get install -y supervisor gunicorn

COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

RUN sed -i 's/\r$//g' entrypoint
RUN chmod +x entrypoint

EXPOSE 8000

ENTRYPOINT ["entrypoint"]
