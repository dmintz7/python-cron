import os, shutil, git, schedule, logging, sys, time, threading, glob, requests
from logging.handlers import RotatingFileHandler

file = "/app/config/apps.csv"

filename, file_extension = os.path.splitext(os.path.basename(__file__))
formatter = logging.Formatter('%(asctime)s - %(levelname)10s - %(module)15s:%(funcName)30s:%(lineno)5s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(formatter)
logger.addHandler(consoleHandler)
logging.getLogger("requests").setLevel(logging.WARNING)
logger.setLevel(os.environ['LOG_LEVEL'])

logger.info("Gathering Repos")
with open(file) as f:
	for x in list(f):
		try:
			if x[0] != "#":
				(description, url)= x.split(',')
				url = url.strip()
				name = url.split("/")[-1].split(".")[0]
				folder =  "/app/repos/" + name
				
				try:
					git.Git("/app/repos/").clone(url)
					logger.info("Repo: %s - Cloned" % name)
				except:
					g = git.cmd.Git("/app/repos/" + name)
					g.pull()
					logger.info("Repo: %s - Upgraded" % name)
					
				os.system("pip3 install -r " + folder + "/requirements.txt")
		except ValueError:
			pass
		except Exception as e:
			logger.error("Row Incorrectly Configured, %s" % x)
			
logger.info("Repos Gathered")