###############################################
#
# Installs necessary files for project
#
###############################################
import os
import secrets
cwd = os.getcwd()


# Create secret key for QuizTake configuration
config_dir = os.path.join(cwd, 'QuizTake', 'config')
flask_ini = os.path.join(config_dir, 'flask.ini')
flask_ini_example = os.path.join(config_dir, 'flask.ini.example')

lines = []
with open(flask_ini_example, 'r', encoding='utf-8') as infile:
    lines = infile.readlines()

secret_key = secrets.token_hex(32)
lines[-1] = lines[-1].replace('ChangeMe', secret_key)

with open(flask_ini, 'w', encoding='utf-8') as outfile:
    outfile.writelines(lines)
