FROM ubuntu:latest

RUN apt update
RUN apt install python3 -y

COPY proof.py /home

CMD ["python3", "/home/proof.py"]
