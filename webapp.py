from flask import Flask,render_template,request,redirect
from flask_login import login_required, current_user, login_user, logout_user
from user_data import UserInfo,db,login
 
app = Flask(__name__)
app.secret_key = 'abc'
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
 
db.init_app(app)
login.init_app(app)
login.login_view = 'login'
 
@app.before_first_request
def create_all():
    db.create_all()
     
@app.route('/')

@app.route('/home')
@login_required
def home():
    return render_template('home.html')
 
 
@app.route('/login', methods = ['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect('/home')
     
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = UserInfo.query.filter_by(username = username).first()
        if username == "" or password == "":
            return ("You can't leave any boxes blank")
        elif user is not None and password == user.password:
            login_user(user)
            return redirect('/home')
        elif password != user.password:
            return ('Incorrect password')
    return render_template('login.html')
 
@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect('/home')
     
    if request.method == 'POST':
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        password = request.form['password']
 
        if UserInfo.query.filter_by(email=email).first():
            return ('Entered email is already present')
        if email != "" or first_name != "" or last_name != "" or username != "" or password != "":
            user = UserInfo(email=email, first_name=first_name, last_name=last_name, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return redirect('/login')
        else:
            return ("You can't leave any boxes blank")
    return render_template('register.html')
 
 
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/home')

if __name__ == "__main__":
    # app.debug = True
    app.run(host="0.0.0.0", port = 80)
