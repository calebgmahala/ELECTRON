import os


def mockdb(username, password = ''):
	if (password == ''):
		subprocess.run('mysqladmin -u' + username + ' create temp', shell=True)
		subprocess.run('mysqldump -u' + username + ' csx | mysql -u' + username + ' -D temp', shell=True)
		subprocess.run('mysqladmin -u' + username + ' drop csx', shell=True)
		subprocess.run('mysqladmin -u' + username + ' create csx', shell=True)
		subprocess.run('mysqldump -u' + username + ' -d temp | mysql -u' + username + ' -D csx', shell=True)
	else:
		subprocess.run('mysqldump -u' + username + ' -p' + password + ' csx | mysql -u' + username + ' -p' + password + ' -e "CREATE DATABASE temp" -D temp', shell=True)
		subprocess.run('mysqladmin -u' + username + ' -p' + password + ' drop csx', shell=True)
		subprocess.run('mysqldump -u' + username + ' -p' + password + ' -d temp | mysql -u' + username + ' -p' + password + '-e "CREATE DATABASE csx" -D csx', shell=True)


def rebuild(username, password = ''):
	if (password == ''):
		subprocess.run('mysqladmin -u' + username + ' drop csx', shell=True)
		asubprocess.run('mysqladmin -u' + username + ' create csx', shell=True)
		subprocess.run('mysqldump -u' + username + ' temp | mysql -u' + username + ' -D csx', shell=True)
		subprocess.run('mysqladmin -u' + username + ' drop temp', shell=True)
	else:
		subprocess.run('mysqladmin -u' + username + ' -p' + password + ' drop csx', shell=True)
		subprocess.run('mysqldump -u' + username + ' -p' + password + ' temp | mysql -u' + username + ' -p' + password + '-e "CREATE DATABASE csx" -D csx', shell=True)
		subprocess.run('mysqladmin -u' + username + ' -p' + password + ' drop temp', shell=True)
