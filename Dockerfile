FROM python:slim

WORKDIR /app
COPY . . 
RUN pip install Flask haversine pytest
EXPOSE 5000

ENV FLASK_ENV=development

ENTRYPOINT python3 api.py