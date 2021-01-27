import sys, os, shutil, glob, requests

name = sys.argv[1]
udid = sys.argv[2]
command = ' '.join(sys.argv[3:])

url = "%s/ping/%s" % (os.environ['HEALTHCHECKS_DOMAIN'], udid)
original_config = glob.glob('/app/config/' + name + '*')[0]
filename, file_extension = os.path.splitext(original_config)
new_config = '/app/repos/' + name + '/config' + file_extension

requests.get(url + "/start")
shutil.copy(original_config, new_config)
full_command = 'python3 /app/repos/' + name + '/' + name + '.py' + command
os.system(full_command)
requests.get(url)
