FROM ubuntu:40.07


RUN mkdir ./app
RUN chmod 774 ./app
WORKDIR ./app

RUN apt -qq update

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Kolkata

RUN apt -qq install -y git python3 ffmpeg python3-pip

COPY requirements.txt .
RUN pip2 install --no-cache-dir -r requirements.txt
COPY . .
CMD ["start.sh"]
