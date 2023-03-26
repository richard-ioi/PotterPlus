FROM python:3.8-slim-buster

WORKDIR /app
RUN apt-get update && apt-get install msmtp -y && \
    rm -rf /var/lib/apt/lists/*

COPY msmtprc /etc/msmtprc
RUN chmod 600 /etc/msmtprc

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY app.py /app/app.py
COPY mailer.sh /app/mailer.sh

EXPOSE 5000
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]