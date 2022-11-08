FROM ubuntu:latest
RUN apt update && apt install python3-pip -y
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
CMD ["python3", "APP.py"]