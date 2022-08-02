<h1 align="center">Kijiji Scraper</h1>
<p align="center">
  <a href="https://github.com/JGBMichalski/Kijiji-Scraper"><img alt="Build Status" src="https://github.com/JGBMichalski/Kijiji-Scraper/actions/workflows/docker-image.yml/badge.svg?branch=master" height="20"/></a>
  <a href="https://github.com/JGBMichalski/Kijiji-Scraper/issues"><img alt="Issues open" src="https://img.shields.io/github/issues/jgbmichalski/Kijiji-Scraper?label=Issues" height="20"/></a>
  <a href="https://github.com/JGBMichalski/Kijiji-Scraper"><img alt="Last commit" src="https://img.shields.io/github/last-commit/jgbmichalski/kijiji-scraper?label=Last%20Commit" height="20"/></a>
  <a href="https://github.com/JGBMichalski/Kijiji-Scraper/releases"><img alt="Latest version" src="https://img.shields.io/github/v/release/jgbmichalski/kijiji-scraper?label=Latest%20Release" height="20"/></a>
  <a href="https://github.com/JGBMichalski/Kijiji-Scraper"><img alt="Github Hits" src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FJGBMichalski%2FKijiji-Scraper&count_bg=%2379C83D&title_bg=%23555555&icon=github.svg&icon_color=%23E7E7E7&title=Hits&edge_flat=false" height="20"/></a>
  <a href="https://hub.docker.com/r/jgbmichalski/kijiji-scraper"><img alt="Docker Pulls" src="https://img.shields.io/docker/pulls/jgbmichalski/kijiji-scraper?label=Docker%20Pulls" height="20"/></a>
</p>
<p align="center">
  <b>Kijiji-Scraper is used to track Kijiji ad information and will send out emails when a new ads are found. This project was originally developed by <a href="https://github.com/CRutkowski">CRutkowski</a>, but due to inactivity and the program breaking, it has since undergone some serious changes.</b>
  
<p align="center">
	<a href="https://github.com/JGBMichalski/Kijiji-Scraper/releases">Download & Release Notes</a>
</p>
<br />

---

## Dependencies

`Kijiji-Scraper` requires the following `python` dependencies: 

* [requests](https://docs.python-requests.org/en/latest/)
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [PyYaml](https://pyyaml.org/wiki/PyYAMLDocumentation)

---

## Installation

### Manually

To install `Kijiji-Scraper` manually:

1. Clone the repository by running the following code:

```bash
git clone https://github.com/JGBMichalski/Kijiji-Scraper.git
```

2. Install the dependencies:

```bash
pip install requests bs4 pyyaml
```

3. Add all the required  the `config.yaml` file (*see the **Configuration** section.*).

4. Run the program:

```bash
python3 kijiji.py
```

### Docker

`Kijiji-Scraper` can be run in Docker, which will allow you to have things up and running fairly quickly with vary little configuration.

1. Pull the docker image from `jgbmichalski/kijiji-scraper`:

```bash
docker pull jgbmichalski/kijiji-scraper
```

2. Run the docker container:

```bash
docker run -d --name kijiji-scraper -v /path/to/your/config:/config jgbmichalski/kijiji-scraper:latest
```
> *Note: If this is your first time running the container and you have not set functional email settings in the `config.yaml` file, an error will occur.*

3. Configure the `config.yaml` file (*see the **Configuration** section.*).

4. Try to run the container again.

> By default, the Docker implementation will automatically check for new ads every two minutes. If you wish to change this, simply update or remove the `--interval` parameter in the dockerfile.

---

## Configuration

The script **must read a configuration file to set mail server settings**. Default config file `config.yaml` is located in the root directory.
 - In the `config.yaml` file, set the `from`, `username`, `password` and `receiver` fields in config file.
 - You can specify the Kijji URLs you wish to scrape at the bottom of the config file. There are a few examples in the config to show the syntax.  
 - Alternatively you can use `--url URLs` to configure URLs to scrape and `--email` to set receivers addresses.

### Using Outlook

If you are using Outlook, simply enter the username and password of the Outlook account you wish to use into the configuration settings. If you are getting an errors, take a look at the recommended SMTP settings inside of your account settings and make sure the configuration matches them.

### Using Gmail

It is important to note that **GMail is no longer supported** due to them removing access to SMTP with just a username and password.

---

## Usage
 
 To run the program, simply execute `python3 kijiji.py` from the root directory.

```
% python3 kijiji.py --help
usage: kijiji.py [-h] [--conf File path] [--url URL [URL ...]] 
                  [--email Email [Email ...]] [--skipmail] [--all] 
                  [--ads File path] [--interval N [N ...]] [--version]

Kijiji scraper: Track ad information and send out emails when a new ads are found

optional arguments:
  -h, --help            show this help message and exit
  --conf File path, -c File path
                        The script * must read a configuration file to set 
                        mail server settings *. Default config file config.yaml
                         is located in the root directly.
  --url URL [URL ...], -u URL [URL ...]
                        Kijiji seacrh URLs to scrape
  --email Email [Email ...], -e Email [Email ...]
                        Email recepients
  --skipmail, -s        Do not send emails. This is useful for the first time 
                        you scrape a Kijiji as the current ads will be indexed 
                        and after removing the flag you will only be sent new ads.
  --all, -a             Consider all ads as new, do not load ads.json file
  --ads File path       Load specific ads JSON file. Default file will be store 
                        in the config folder
  --interval N [N ...], -i N [N ...]
                        Time to wait between each loop
  --version, -V         Print Kijiji-Scraper version
```


### Ad Storage
The script stores current ads in `ads.json` file located by default in the config folder. If an `./ads.json` file exist, it will automatically be loaded.
