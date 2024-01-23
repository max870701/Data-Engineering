FROM python:3.9

RUN pip install pandas sqlalchemy psycopg2 psycopg psycopg2-binary psycopg-binary 

WORKDIR /app
COPY ingest_data.py ingest_data.py

ENTRYPOINT [ "python", "ingest_data.py" ]