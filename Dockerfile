FROM python:3.11

WORKDIR /usr/src/app

COPY . .

# RUN pip install -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

ENV SERVER_HOST "0.0.0.0"
ENV SERVER_PORT 8080
ENV PYTHONUNBUFFERED 1

CMD ["python", "-u", "./src/main.py"]