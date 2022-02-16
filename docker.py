import os

cloneURL = 'https://github.com/JGBMichalski/Kijiji-Scraper.git'
filesRequired = ['/Kijiji-Scraper/kijiji.py', '/Kijiji-Scraper/config.yaml', '/Kijiji-Scraper/ads.json', '/Kijiji-Scraper/kijiji_scraper']

# Check if Kijiji-Scraper main file exists
if os.path.exists(filesRequired[0]):
    print('Repository exists locally.\nSkipping setup.\n\n')
else:
    print('Repository does not exist locally.\nCloning repository into the root directory...')
    
    # Clone the repo
    os.system('git clone {} /Kijiji-Scraper'.format(cloneURL))
    
    # Verify that core files exist after the clone
    print('Verifying that files exist...')
    for file in filesRequired:
        if not os.path.exists(file):
            print(' - ERROR: {} not found.'.format(file))
            exit(1)
    
    print('All files exist.\nSetup Complete!\n\n')
