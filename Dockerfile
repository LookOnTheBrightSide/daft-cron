FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
ENV HOME=/app
RUN pip install -r requirements.txt
ENV FLASK_APP=run.py
EXPOSE 5000
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:5000", "-w", "4", "wsgi:app"]
