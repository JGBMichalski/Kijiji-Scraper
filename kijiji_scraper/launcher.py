import yaml
import time
import sys
import os
import argparse
from shutil import which

from kijiji_scraper.kijiji_scraper import KijijiScraper
from kijiji_scraper.email_client import EmailClient
from . import VERSION

def parse_args():
    parser = argparse.ArgumentParser(description="""Kijiji scraper: Track ad informations and sends out an email when a new ads are found""")
    parser.add_argument('--conf', '-c', metavar='File path', help="""The script * must read a configuration file to set mail server settings *. Default config file config.yaml is located in the root directly.""")
    parser.add_argument('--url', '-u', metavar="URL", help="Kijiji seacrh URLs to scrape", nargs='+', default=None)
    parser.add_argument('--email','-e', metavar="Email", help="Email recepients", nargs='+',  default=None)
    parser.add_argument('--skipmail', '-s', help="Do not send emails. This is useful for the first time you scrape a Kijiji as the current ads will be indexed and after removing the flag you will only be sent new ads.", action='store_true')
    parser.add_argument('--all', '-a', help="Consider all ads as new, do not load ads.json file", action='store_true')
    parser.add_argument('--ads' , metavar="File path", help="Load specific ads JSON file. Default file will be store in the config folder")
    parser.add_argument('--interval', '-i', metavar='N', type=int, help="Time to wait between each loop", nargs='+',  default=None)
    parser.add_argument('--version', '-V', help="Print Kijiji-Scraper version", action='store_true')
    args = parser.parse_args()
    return(args)

def main():
    # parse the arguments 
    args = parse_args()

    if args.version:
        print("Version:\t\t%s" %VERSION)
        exit(0)

    if args.interval:
        loop = True # We will want to do multiple iterations
    else: 
        loop = False

    while (loop):
        # Get configuration path
        filepath = config_path(args.conf)
        
        # Get config values
        if filepath:
            # Read from configuration file
            with open(filepath, "r") as config_file:
                email_config, urls_to_scrape = yaml.safe_load_all(config_file)
            print("Loaded config file: %s"%filepath)
        else:
            print("No config file loaded")
            email_config, urls_to_scrape = ({},{})
            # Do not try to send mail if no config file is loaded
            args.skipmail=True

        # Initialize the KijijiScraper and email client
        ads_filepath=None
        if not args.all:
            if args.ads: 
                ads_filepath=args.ads
            else:
                # Find default ads.json file in PWD directory
                print(os.path.abspath(os.getcwd()))
                if os.path.exists(os.path.abspath(os.getcwd()) + "/ads.json"): 
                    ads_filepath="ads.json"
            print("Ads file: %s"%ads_filepath)
        kijiji_scraper = KijijiScraper(ads_filepath)
    
        # Overwrite search URLs if specified
        if args.url: urls_to_scrape = [{'url':u} for u in args.url]

        # Nice quit if no URLs
        if not urls_to_scrape :
            print("You must supply at least one URL to scrape. Use --url or configure URLs in the config file.")
            exit(-1)

        # Scrape each url given in config file
        for url_dict in urls_to_scrape:
            url = url_dict.get("url")
            exclude_words = url_dict.get("exclude", [])

            print("Scraping: %s"%url)
            if len(exclude_words):
                print("Excluding: " + ", ".join(exclude_words))

            kijiji_scraper.set_exclude_list(exclude_words)
            ads, email_title = kijiji_scraper.scrape_kijiji_for_ads(url)

            info_string = "Found %s new ads"%len(ads) \
                if len(ads) != 1 else "Found 1 new ad"
            print(info_string)

            # Print ads summary list 
            sys.stdout.buffer.write(get_ads_summary(ads).encode('utf-8'))
            # Send email
            if not args.skipmail and len(ads):
                email_client = EmailClient(email_config)
                # Overwrite email recepeients if specified
                if args.email: email_client.receiver=','.join(args.email)
                email_client.mail_ads(ads, email_title)
                print("Email sent to %s"%email_client.receiver)
            else: print("No email sent")

        if ads_filepath: kijiji_scraper.save_ads()

        if (loop):
            print('Waiting {} seconds until next check...'.format(args.interval[0]))
            time.sleep(args.interval[0])

def config_path(conf):
    # Handle custom config file
    if conf:
        filepath=conf
    else:
        # Find the default config file in the install directory
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(os.path.dirname(abspath))
        filepath=os.path.join(dname, "config.yaml")
        if not os.path.exists(filepath):
            filepath=None
    return filepath

def get_ads_summary(ads):
    string=''
    if not ads: return string
    header = ("Title", "Url")
    title_w=20
    # Determine the longest width for Title column
    for ad_id in ads:
        title_w=len(ads[ad_id]['Title'])+4 if ads[ad_id] and len(ads[ad_id]['Title'])>title_w else title_w
    frow="{:<%d} {}"%title_w
    string+=frow.format(*header)

    for ad_id in ads:
        string+='\n'
        string+=frow.format(str(ads[ad_id]['Title']), str(ads[ad_id]['Url']))

    return string+'\n'

def find_file(env_location, potential_files, default_content="", create=False):
    potential_paths=[]
    existent_file=None
    # build potential_paths of config file
    for env_var in env_location:
        if env_var in os.environ:
            for file_path in potential_files:
                potential_paths.append(os.path.join(os.environ[env_var],file_path))
    # If file exist, add to list
    for p in potential_paths:
        if os.path.isfile(p):
            existent_file=p
            break
    # If no file foud and create=True, init new template config
    if existent_file==None and create:
        os.makedirs(os.path.dirname(potential_paths[0]), exist_ok=True)
        with open(potential_paths[0],'w') as config_file:
            config_file.write(default_content)
        print("Init new file: %s"%(p))
        existent_file=potential_paths[0]

    return(existent_file)
