# Chat App

Hey! This is a chat app created with Python Flask.

You can see how this app looks like in given youtube link.
https://www.youtube.com/watch?v=N4BUsRmNbsg

Languages used in this projects:
<h2>For Frontend:</h2>
1- Html
2- CSS
3- python jinja2 template 
4- JavaScript

<h2>For Backend</h2>
1- Python Flask
2- Socket Io 
3- MySQL Database

<h1>How You can clone it </h1>
Step No 1:
First install python in your system from https://www.python.org/downloads/

Step No 2:
Install xampp for localhost connection with Database

Step No 3:
Now, you have to create the virtual environment for this project
	for windows use this command in cmd "py -3 -m venv .venv"
   	for linux or macos use this command in terminal "python3 -m venv .venv"

Step No 4:
Activate the virtual environment
	for windows use this command in cmd ".venv\Scripts\activate"
	for linux or mac use this command in terminal"source .venv/bin/activate"

Step No 5:
Now, clone these all files including templates and static folders
and open these files in visual studio code or in any other editor.

Step No 6:
After cloning all the files again go to cmd and type "pip install flask" to install flask.

List of libraries need to run this project.

1- Install the authlib library to use the github or google signin integration
	for windows use this command "pip install authlib"
	check the linux or macos commad on internet

2- Install the socket-io library to real time message sending or receiving
	for windows use this command "pip install flask-socketio"
	check the linux or macos command on internet

3- Install the mysqldb library to connect it through database
	for windows use this command "pip install flask-mysqldb"
	check the linux or macos command on internet

<h1>To Create database:</h1>

Step No 1:
Start mysql and apache from xampp control panel
Now go to any browser write "127.0.0.1/phpmyadmin" to access the xampp admin panel.

Step No 2:
create the new database named "userlogin"
create the table named detail include these fields
"first_name[varchar], last_name[varchar], email[varchar], phone[bigint], username[varchar], password[varchar]" 

OR
you can directly import the userlogin database file (SQL format) given in repository.

<h1>For Google integration</h1>
First for google integration go to google cloud platform and create the client id and 
client secret key given in sample image.
<br />
<br />

![My Image](https://github.com/sahilkhimani/Flask-chatApp/blob/main/images/google%20cloud%20platform.png
)

Now, paste these google client id and client secret in google route in app.py file.

<h1>For Github integration</h1>
For github integration go to your github account and from settings go to developer option and create the client id and client secret key given in sample image.
<br />
<br />

![My Image](https://github.com/sahilkhimani/Flask-ChatApp/blob/main/images/github.png)

Now, paste these client id and client secret in github section in app.py file.

<h2>Congratulations! Now from command prompt run "python app.py" command.</h2>
