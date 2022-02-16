# Kijiji-Scraper 1.0.0

## Summary
`Kijiji-Scraper` is used to track Kijiji ad information and sends out emails when a new ads are found. This project was originally developed by [@CRutkowski](https://github.com/CRutkowski), but due to inactivity and the program breaking, it has since undergone some serious changes.

## Dependencies

`Kijiji-Scraper` requires the following `python` dependencies: 

* requests
* BeautifulSoup
* PyYaml

## Installation

### Manually

You can install `Kijiji-Scraper` manually by running the following code:

```bash
git clone https://github.com/JGBMichalski/Kijiji-Scraper.git
```

To install the dependencies, execute:

```bash
pip install requests bs4 pyyaml
```

### Docker

*Documentation coming soon.*

## Configuration

The script **must read a configuration file to set mail server settings**. Default config file `config.yaml` is located in the root directory.
 - Ub the `config.yaml` file, set the `from`, `username`, `password` and `receiver` fields in config file.
 - You can specify the Kijji URLs you wish to scrape at the bottom of the config file. There are a few examples in the config to show the syntax.  
 - Alternatively you can use `--url URLs` to configure URLs to scrape and `--email` to set receivers addresses.

### Using Gmail

If you are using Gmail, you will have to enable less secure apps on your account. To do this, simply:

1. In your Google account, go to `My Account -> Sign in & security -> Connected apps & sites`.
2. Turn `Allow less secure apps` to `On`.

## Usage
 
 To run the program, simply execute `python3 main.py` from the root directory.

<!-- ```
% kijiji --help           
usage: kijiji [-h] [--conf File path] [--url URL [URL ...]]
               [--email Email [Email ...]] [--skipmail] [--all]
               [--ads File path] [--version]

Kijiji scraper: Track ad informations and sends out an email when a new ads
are found

optional arguments:
  -h, --help            show this help message and exit
  --conf File path, -c File path
                        The script * must read a configuration file to set
                        mail server settings *. Default config file
                        config.yalm is located in ~/.kijiji_scraper/
                        (MacOS/Linux), APPDATA/.kijiji_scraper (Windows) or
                        directly in the install folder.
  --url URL [URL ...], -u URL [URL ...]
                        Kijiji seacrh URLs to scrape
  --email Email [Email ...], -e Email [Email ...]
                        Email recepients
  --skipmail, -s        Do not send emails. This is useful for the first time
                        you scrape a Kijiji as the current ads will be indexed
                        and after removing the flag you will only be sent new
                        ads.
  --all, -a             Consider all ads as new, do not load ads.json file
  --ads File path       Load specific ads JSON file. Default file will be
                        store in the config folder
  --version, -V         Print Kijiji-Scraper version
``` -->


### Ad Storage
The script stores current ads in `ads.json` file located by default in the config folder. If an `./ads.json` file exist, it will automatically be loaded.
