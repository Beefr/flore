
FROM cren0/nginxflask:latest

WORKDIR /app
COPY ./app /app

EXPOSE 8080

CMD ["python", "/app/main.py"]

