import sys, os, shutil, glob

name = sys.argv[1]
command = ' '.join(sys.argv[2:])

original_config = glob.glob('/app/config/' + name + '*')[0]
filename, file_extension = os.path.splitext(original_config)
new_config = '/app/repos/' + name + '/config' + file_extension

shutil.copy(original_config, new_config)
full_command = 'python3 /app/repos/' + name + '/' + name + '.py' + command
os.system(full_command)