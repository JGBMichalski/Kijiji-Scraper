import yaml
import time
import sys
import os
import argparse
import shutil

from kijiji_scraper.kijiji_scraper import KijijiScraper
from kijiji_scraper.email_client import EmailClient
from kijiji_scraper.version import VERSION

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
        print('Version: {}'.format(VERSION))
        exit(0)
    else:
        print('Runnining Kijiji-Scraper v{}\n\n'.format(VERSION))

    if args.interval:
        loop = True # We will want to do multiple iterations
    else: 
        loop = False

    while (loop):
        # Get configuration path
        filepath = config_path(args.conf)
        
        # Get config values
        print(' - Loading configuration file...')
        if filepath:
            # Read from configuration file
            with open(filepath, "r") as config_file:
                email_config, urls_to_scrape = yaml.safe_load_all(config_file)
            print("   - Loaded config file: %s"%filepath)
        else:
            print("   - ERROR: No config file loaded.")
            sys.exit('No config file loaded.')

        # Initialize the KijijiScraper and email client
        ads_filepath=None
        if not args.all:
            print(' - Loading ads.json file...')
            if args.ads: 
                ads_filepath=args.ads
            else:
                # Find default ads.json file in PWD directory
                if os.path.exists(os.path.abspath(os.getcwd()) + "/ads.json"): 
                    ads_filepath="ads.json"
                    print('   - Using ads.json in the current directory.')
            print("   - Ads file: %s"%ads_filepath)
        kijiji_scraper = KijijiScraper(ads_filepath)
    
        # Overwrite search URLs if specified
        if args.url: 
            print(' - Overwriting URLs with URLs specified from CLI...')
            urls_to_scrape = [{'url':u} for u in args.url]

        # Nice quit if no URLs
        print(' - Verifying that there are URLs to scrape...')
        if not urls_to_scrape:
            print('   - No URLs specified. Add URLs in the config.yaml file or use --url or configure URLs in the config file.')
            sys.exit('No URLs specified. Add URLs in the config.yaml file or use --url or configure URLs in the config file.')

        # Scrape each url given in config file
        print(' - Scraping URLs...')
        for url_dict in urls_to_scrape:
            url = url_dict.get("url")
            exclude_words = url_dict.get("exclude", [])

            print('   - Scraping: {}'.format(url))
            if len(exclude_words):
                print("     - Excluding: " + ", ".join(exclude_words))

            kijiji_scraper.set_exclude_list(exclude_words)
            ads, email_title = kijiji_scraper.scrape_kijiji_for_ads(url)

            if len(ads) == 1:
                print('     - Found 1 new ad:')
            else:
                print('     - Found {} new ads:'.format(len(ads)))

           

            # Print ads summary list
            for ad_id in ads:
                print('       - {} | {}'.format(str(ads[ad_id]['Title']), str(ads[ad_id]['Url'])))

            # Send email
            if not args.skipmail and len(ads):
                email_client = EmailClient(email_config)
                # Overwrite email recepeients if specified
                if args.email: 
                    email_client.receiver=','.join(args.email)
                email_client.mail_ads(ads, email_title)
                print('     - Email sent to {}'.format(email_client.receiver))
            else: 
                print("     - No email sent.")

        if ads_filepath: 
            print(' - Updating ad list...')
            kijiji_scraper.save_ads()

        if (loop):
            print(' - Waiting {} seconds until next check...'.format(args.interval[0]))
            time.sleep(args.interval[0])

def config_path(conf):
    # Handle custom config file
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(os.path.dirname(abspath))
    
    if conf:
        filepath=conf
        if not os.path.exists(filepath):
            print(' - Configuration file at {} does not exist. Creating it using the default template...'.format(filepath))
            shutil.copyfile(os.path.join(dname, "config.yaml"), filepath)
    else:
        # Find the default config file in the install directory
        filepath=os.path.join(dname, "config.yaml")
        if not os.path.exists(filepath):
            filepath=None
    return filepath

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
