import os, shutil, git, schedule, logging, sys, time, threading, glob
from logging.handlers import RotatingFileHandler

file = "/app/config/apps.csv"

extra = {'folder_name': os.path.dirname(os.path.abspath(__file__)).split("/")[-1]}
formatter = logging.Formatter('%(asctime)s - %(levelname)10s - %(folder_name)15s:%(module)15s:%(funcName)30s:%(lineno)5s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(formatter)
logger.addHandler(consoleHandler)
fileHandler = RotatingFileHandler(os.environ['LOG_FOLDER'] + '/python-cron.log', maxBytes=1024 * 1024 * 1, backupCount=1)
logger.setLevel(os.environ['LOG_LEVEL'])
logging.getLogger("requests").setLevel(logging.WARNING)
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)
logger = logging.LoggerAdapter(logger, extra)

def run_command(command, original_config, new_config):
	try:
		shutil.copy(original_config, new_config)
	except FileNotFoundError:
		logger.info("No Config File Found")
		pass
	os.system(command)

def run_threaded(job_func, *args, **kwargs):
	job_thread = threading.Thread(target=job_func, args=args, kwargs=kwargs)
	job_thread.start()
	
logger.info("Gathering Repos")
with open(file) as f:
	for x in list(f):
		try:
			if x[0] != "#":
				(description, url, cron, param, autostart)= x.split(',')
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
				
				original_config = glob.glob("/app/config/"+name +".*")[0]
				new_config = folder + "/config" + os.path.splitext(original_config)[1]

				if ":" in cron:
					if "/" in cron:
						hour = cron.split(":")[0].split("/")[0]
						minute = cron.split(":")[1]
						type = "Every %s hours at minute %s" % (hour, minute)
						# schedule.every().day.at(cron).do(run_command, 'python3 /app/repos/' + name + '/run.py', original_config, new_config)
					else:
						hour = cron.split(":")[0]
						minute = cron.split(":")[1]
						
						schedule.every().day.at(("00"+hour)[-2:]+":"+("00"+minute)[-2:]).do(run_threaded, run_command, 'python3 /app/repos/' + name + '/run.py ' + param, original_config, new_config)
						type = "Every Day at %s" % cron
				else:
					if cron[0] == "*":
						hour = cron.split("/")[0]
						minute = cron.split("/")[1]
						schedule.every(int(minute)).minutes.do(run_threaded, run_command, 'python3 /app/repos/' + name + '/run.py ' + param, original_config, new_config)
						type = "Every %s minutes" % minute
					else:
						hour = cron.split("/")[1]
						minute = cron.split("/")[0]
						schedule.every().minute.at(":" + minute).do(run_threaded, run_command, 'python3 /app/repos/' + name + '/run.py ' + param, original_config, new_config)
						type = "Every Hour at minute %s" % minute
						
				logger.info("Setting %s to run %s" % (description, type))
		except ValueError:
			pass
		except Exception as e:
			logger.error("Row Incorrectly Configured, %s" % x)
			
			
logger.info("Repos Gathered and Scheduler Created")
while True:
	try:
		logger.info("Starting Scheduler")
		schedule.run_all()
		while True:
			schedule.run_pending()
			time.sleep(1)
	except Exception as e:
		logger.error("Scheduler Errored")
		pass