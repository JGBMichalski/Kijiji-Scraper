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

# Download and setup Kijiji-Scraper
RUN git clone https://github.com/JGBMichalski/Kijiji-Scraper.git

# Execute Kijiji-Scraper once every minute
CMD python3 /Kijiji-Scraper/kijiji.py --interval 60