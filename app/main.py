from flask import Flask, request, redirect, render_template, url_for, flash, make_response
from flask_login import LoginManager,  login_required, current_user, login_user, logout_user

import pathlib
print(pathlib.Path(__file__).parent.resolve())

import hashlib


try:
    from interactBDD import InteractBDD
except:
    pass

from user import User, Anonymous

from output import Output
from ticket import Ticket

from forms import LoginForm, IndexForm, RegisterForm, LotForm, TrainForm, ApplicationForm, AnomalieForm, EvolutionForm

login_manager = LoginManager()
login_manager.anonymous_user = Anonymous
login_manager.current_user = User
login_manager.login_view = "login"

app = Flask(__name__)
app.secret_key = 'secretKeys12344321'

login_manager.init_app(app)


# TODO https://developer.mozilla.org/docs/Web/HTTP/Headers/Set-Cookie/SameSite



@app.route("/handle_data", methods=['GET', 'POST'])
def handle_data():
    

    if "password2" in request.form:
        if sanitization([request.form['username'], request.form['password1'], request.form['password2']]):
            exists=InteractBDD.existInDB(request.form['username'])
            if not exists:
                if request.form['password1'] == request.form['password2']:
                    InteractBDD.createUser(request.form['username'], hashPassword(request.form['password1']))

    if "password" in request.form:
        checkPassword(request.form['username'], request.form['password'])
        return redirect(url_for('menu', username=current_user.username, id=current_user.id))
    
    user_input="None"
    if "user_input" in request.form:
        user_input=request.form["user_input"]

    if current_user.is_authenticated:
        current_user.id=request.cookies.get('id')
        return redirect(url_for('menu', username=current_user.username, id=current_user.id, user_input=user_input))
        
    return redirect(url_for('login'))

@app.route("/menu/<username>/", methods=['GET','POST'])
@login_required
def menu(username):
    output = Output.content
    ticket=Ticket("REI", "C02", "22.11")
    resp= make_response(render_template('index.html', output=output, form=IndexForm(), username=username, ticket=ticket))
    return resp

@app.route("/lots/<username>", methods=['GET','POST'])
@login_required
def lots(username):
    output = Output.content
    resp= make_response(render_template('lots.html', output=output, form=LotForm(), username=username))
    #resp.set_cookie('id', id)
    return resp

@app.route("/trains/<username>/", methods=['GET','POST'])
@login_required
def trains(username):
    output = Output.content
    resp= make_response(render_template('trains.html', output=output, form=TrainForm(), username=username))
    return resp

    
@app.route("/applications/<username>/", methods=['GET','POST'])
@login_required
def applications(username):
    output = Output.content
    resp= make_response(render_template('applications.html', output=output, form=ApplicationForm(), username=username))
    return resp

    
@app.route("/anomalies/<username>/", methods=['GET','POST'])
@login_required
def anomalies(username):
    output = Output.content
    resp= make_response(render_template('anomalies.html', output=output, form=AnomalieForm(), username=username))
    return resp
    
    
@app.route("/evolution/<username>/<application>/<train>/<couloir>/", methods=['GET','POST'])
@login_required
def evolution(username, application, train, couloir):
    ticket=Ticket(application, couloir, train)
    resp= make_response(render_template('evolution.html', form=EvolutionForm(), username=username, ticket=ticket))
    return resp
    


def checkPassword(username, password):
    if sanitization([username, password]):
        password=hashPassword(password)
        if InteractBDD.existInDB(username) and InteractBDD.checkPassword(username, password):
            user = User(username)
            login_user(user)
            return True
                
        return False

            
@app.errorhandler(404)
def page_not_found(error):
    print("page not found error")
    if current_user.is_authenticated:
        return redirect(url_for('menu', username=current_user.username, id=current_user.id))
    else:
        return redirect(url_for('login'))

        
@app.errorhandler(500)
def page_not_found(error):
    print("Internal Server Error")
    if current_user.is_authenticated:
        return redirect(url_for('menu', username=current_user.username, id=current_user.id))
    else:
        return redirect(url_for('login'))


@login_manager.unauthorized_handler
def unauthorized():
    print("unauthorized action")
    if current_user.is_authenticated:
        return redirect(url_for('menu', username=current_user.username, id=current_user.id))
    else:
        return redirect(url_for('login'))

@app.route("/login/", methods=['GET','POST'])
def login():
    if current_user.is_authenticated: # redirection in case the user modified the url path to login
        user_input="None"
        if "user_input" in request.form:
            user_input= request.form["user_input"]
        return redirect(url_for('menu', username=current_user.username, user_input=user_input, id=current_user.id))
 
    return render_template('login.html', form=LoginForm())


@app.route("/register/", methods=['GET','POST'])
def register():
    if current_user.is_authenticated: # redirection in case the user modified the url path to login
        user_input="None"
        if "user_input" in request.form:
            user_input= request.form["user_input"]
        return redirect(url_for('menu', username=current_user.username, user_input=user_input, id=current_user.id))
 
    return render_template('register.html', form=RegisterForm())




@app.route("/logout")
def logout():
    logout_user()
    flash("You've been logged out! Come back soon!", "success")
    return redirect(url_for('login'))


@login_manager.user_loader
def load_user(id):
    username = InteractBDD.getUsername(id)
    user = User(username) # at the user creation, it seems it returns the None account
    return user




def sanitization(user_input):
    forbiddenCharacters=["'", "\"", "\\", "&", "~", "{", "(", "[", "-", "|", "`", "_", "ç", "^", "à", "@", ")", "]", "=", "}", "+", "$", "£", "¤", "*", "µ", "ù", "%", "!", "§", ":", "/", ";", ".", ",", "?", "<", ">", "²"]
    if len(user_input)==0 or user_input=="": # empty input
        return False

    for elem in user_input:
        if len(elem)>=40: # max 15 characters
            return False
            
        for char in forbiddenCharacters: # no special characters
            if char in elem:
                return False
    return True


    
def hashPassword(password):
    # https://docs.python.org/fr/3/library/hashlib.html
    password=hashlib.blake2b(password.encode('utf-8')).hexdigest()
    try:
        password=password[0:240]
    except:
        pass
    return password



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)
    