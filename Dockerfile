FROM ubuntu:focal
MAINTAINER JGBMichalski

ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \ 
    python3 \
    python3-pip \ 
    wget \ 
    git \ 
    cron

# Install python dependencies
RUN pip install requests bs4 pyyaml

# Copy the setup python script to /usr/sbin
COPY docker.py /usr/sbin

# Setup Kijiji-Scraper if it is not already setup and execute Kijiji-Scraper once every minute
CMD python3 /usr/sbin/docker.py && python3 /Kijiji-Scraper/kijiji.py --interval 60