import logging
import os
import random

main_path = __file__.replace(os.path.basename(__file__), '')

formatter = "[%(asctime)s] %(message)s"
logFormatter = logging.Formatter(formatter)
logging.basicConfig(format=formatter)
logging.basicConfig(level=logging.INFO)
global rootLogger


fileHandler = logging.FileHandler("{0}/{1}.txt".format(f'{main_path}/logs', 'DISCORD_LOG'))
fileHandler.setFormatter(logFormatter)

if os.path.getsize(f'{main_path}/logs/DISCORD_LOG.txt') >= 52428800:
    fileHandler.close()
    a = random.random()
    os.rename(f'{main_path}/logs/DISCORD_LOG.txt', f'DISCORD_LOG_{a}.txt')
    with open(f'{main_path}/logs/DISCORD_LOG.txt', 'w+') as file:
        file.write('Cleaning up logs!')
        file.close()

logging.basicConfig(level=logging.WARNING)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger = logging.getLogger()
rootLogger.addHandler(fileHandler)
# rootLogger.addHandler(consoleHandler)

