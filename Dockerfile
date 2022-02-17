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
COPY kijiji_scraper/* /Kijiji-Scraper/kijiji_scraper/
COPY docker.py /Kijiji-Scraper
COPY kijiji.py /Kijiji-Scraper
COPY config.yaml /Kijiji-Scraper
COPY ads.json /Kijiji-Scraper
COPY VERSION /Kijiji-Scraper

# Change the directory to /Kijiji-Scraper
WORKDIR /Kijiji-Scraper

# Setup Kijiji-Scraper if it is not already setup and execute Kijiji-Scraper once every 2 minutes using the docker config.yaml
CMD python3 docker.py && python3 kijiji.py --conf /config/config.yaml --ads /config/ads.json --interval 120