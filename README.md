### Ballogy ###

* This app is for Ballogy Backend.
* v0.1

### Clone the repo ###

* clone entire repo

### Local deployment guidelines ###

* Create virtual enviornment and activate it.
	virtualenv <env name>
	source /<env name>/bin/activate
	sudo apt-get install libmysqlclient-dev
    sudo apt install libpq-dev
    sudo apt install libcurl4-openssl-dev libssl-dev

    dpkg --add-architecture i386
    apt-get update
    apt-get install libssl-dev:i386

* Install all requirements, provided in requirements.txt file.
	pip install -r requirements.txt

### Project Path on Server

* Ballogy project is placed in home directory of server. You will login to server by "ppk" file through putty.
* username will be required which is "username"
* No password is required.
* You will move in to project home directory by command "cd ballogy/"

### Database setup guidelines ###

* This application is using postgresql, which is located on server "52.34.249.155". So you don't
have to run migrations locally.
* DB credentials
*name: ballogydb
*username: ballogyadmin
*password: frt!ballogy

# You can verify ballogy api from Swagger
*Swagger Url: http://52.34.249.155:8001/docs/

# Usefull Commands
* Code push: git push bitbucket <branch-name>
* Code pull: git pull bitbucket <branch-name>
* Start server at background: nohup python manage.py runserver env=environment &
* env=environment option is for selecting environment. If you do not mention it, it will be run in local environment. Environment details are in env.py file.
* If it is beta server, you will set like env=beta-environment
* Options for environment are local/server/remote/beta-local/beta-server/beta-remote
* Free port: sudo fuser -k 8000/tcp

### Contribution guidelines ###

* Please do not push any file included in gitignore
