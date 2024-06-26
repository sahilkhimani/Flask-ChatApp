from flask import Flask, render_template, request, redirect, url_for, session;
from authlib.integrations.flask_client import OAuth
from authlib.common.security import generate_token
from flask_socketio import join_room, leave_room, SocketIO, send;
import random;
from string import ascii_uppercase
from flask_mysqldb import MySQL;
import jinja2; 


app = Flask(__name__)
app.secret_key = "sAhIlKhImAnIsOfTwArEeNgInEeRiNg7"
socketio= SocketIO(app, async_mode='threading')

rooms = {}


def generateCode(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        
        if code not in rooms:
            break
    
    return code


app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'userlogin'
 
mysql = MySQL(app)
oauth = OAuth(app)


@socketio.on("message")
def message(message):
    send(message, broadcast=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM detail WHERE username = %s AND password = %s",(username,password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            session["username"] = username
            return render_template('home.html', user=user[4])
        else:
            return render_template('index.html', message = 'Wrong Username or Password')
    else:
        return render_template('index.html')
    


@app.route('/google/')
def google():

    GOOGLE_CLIENT_ID = 'YOUR GOOGLE CLIENT ID'
    GOOGLE_CLIENT_SECRET = 'YOUR GOOGLE CLIENT SECRET'

    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

    redirect_uri = url_for('google_auth', _external=True)
    # print(redirect_uri)
    session['nonce'] = generate_token()
    return oauth.google.authorize_redirect(redirect_uri, nonce=session['nonce'])

@app.route('/google/auth')
def google_auth():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token, nonce=session['nonce'])
    session['username'] = user['name']
    # print(" Google User ", user)
    return render_template('home.html')



github = oauth.register(
    name='github',
    client_id='YOUR GITHUB CLIENT ID',
    client_secret='YOUR GITHUB CLIENT SECRET',
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)


@app.route('/github')
def github():
   github = oauth.create_client('github')
   redirect_uri = url_for('authorize', _external=True)
   return github.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    github = oauth.create_client('github')
    token = github.authorize_access_token()
    resp = github.get('user', token=token)
    profile = resp.json()
    session['username'] = profile['name']
    return render_template('home.html')
       

@app.route('/main')
def main():
    if 'username' in session:
        return render_template('main.html')
    else:
        return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first = request.form['first_name']
        last = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO detail (first_name, last_name, email, phone, username, password) VALUES (%s,%s,%s,%s,%s,%s)",(first, last, email, phone, username, password))
        mysql.connection.commit()
        cursor.close()

        return render_template('index.html', message="Registered Succesfully")
    else:
        return render_template('index.html', message="All fields are not filled")


@app.route('/edited', methods=['GET', 'POST'])
def edited():
    if request.method == 'POST':
        first = request.form['firstname']
        last = request.form['lastname']
        email = request.form['emailadd']
        phone = request.form['phoneno']
        username = request.form['user']
      
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE detail SET first_name = %s, last_name = %s, email = %s, phone = %s WHERE username = %s" , (first, last, email, phone, username))
        mysql.connection.commit()
        cursor.close()

        return render_template('main.html', message="Data is edited Successfully")
    else:
        return render_template('main.html', message="All fields are not filled")


@app.route('/showdata', methods=['GET', 'POST'])
def showdata():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM detail")
    data = cursor.fetchall()
    cursor.close()
    return render_template('main.html', data=data)





@app.route("/home", methods=['GET', 'POST'])
def home():
    if 'username' in session:
        # session.clear()
        if request.method == "POST":
            name = request.form.get("name")
            code = request.form.get("code")
            join = request.form.get("join", False)
            create = request.form.get("create", False)

            if not name:
                return render_template("home.html", message="Enter Your Name to join chat", code=code, name=name)

            if join != False and not code:
                return render_template("home.html", message="Please enter a valid room code to join.", code=code, name=name)
            
            room = code
            if create != False:
                room = generateCode(6)
                rooms[room] = {"members": 0, "messages": []}
            elif code not in rooms:
                return render_template("home.html", message="This Chat Room does not exist.", code=code, name=name)
            
            session["room"] = room
            session["name"] = name
            return redirect(url_for("room"))

        return render_template('home.html')
    else:
        return redirect('/')
    

@app.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))

    return render_template("room.html", code=room, messages=rooms[room]["messages"])

@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return 
    
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    # print(f"{session.get('name')} said: {data['data']}")

@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    
    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"] += 1
    # print(f"{name} joined room {room}")

@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
    
    send({"name": name, "message": "has left the room"}, to=room)
    # print(f"{name} has left the room {room}")



if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
