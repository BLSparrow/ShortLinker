from flask import Flask, render_template, request, url_for, flash
from flask_login.utils import logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from UserLogin import UserLogin
import bd
bd.db_create()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hgfg85thf1hr1th56t89h5fg1ht'

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Авторизируйтесь для доступа к данной странице!'


@login_manager.user_loader
def load_user(user_id):
    print('load_user')
    return UserLogin().fromDB(user_id, bd)



menu = [
{'name': 'Регистрация', 'url': 'register'},
{'name': 'Авторизация', 'url': 'login'},
{'name': 'Мои ссылки', 'url': 'office'},]

@app.route('/', methods=['POST', 'GET']) 
def index(): 
    print(url_for('index'))
    return render_template('index.html', links = links,  menu = menu) 


@app.route('/register', methods=['POST', 'GET']) 
def register(): 
    print(url_for('register'))
    if request.method == 'POST': 
        if len(request.form['password']) >= 4 and len(request.form['login'])>0:
            login = request.form['login'] 
            password = request.form['password'] 
            hash = generate_password_hash(password)
            reg = bd.db_loginId(login)
            if reg == 1:
                flash("Такой логин уже есть!")
            elif reg == 0:
                bd.db_reg_user(login, hash)
                flash("Вы зарегистрировались!")
                return redirect(url_for('login'))
        else:
            flash('Неверное заполнение полей! (Пароль>3 и Логин>0)')
    return render_template('register.html', title='Регистрация', menu = menu) 

@app.route('/login', methods=['POST', 'GET']) 
def login(): 
    if current_user.is_authenticated:
        return redirect(url_for('office'))
    if request.method == 'POST': 
        user = bd.getUserByLogin(request.form['login']) 
        if user and check_password_hash(user[2], request.form['password']):
            userLogin = UserLogin().create(user)
            rm = True if request.form.get('remainme') else False
            login_user(userLogin, remember=rm)
            return redirect(request.args.get('next') or url_for('office'))
        flash('Неверная пара логин/пароль!')
    return render_template('login.html', title='Авторизация', menu = menu) 


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта')
    return redirect(url_for('login'))



@app.route('/office',  methods=['POST', 'GET']) 
@login_required
def office(): 
    try:
        login = user[1]
        flash(f'Ваш личный кабинет')
    except:
         flash('Что-то пошло не так!')
    return render_template('office.html', title='Личный кабинет', login = login, menu = menu) 



if __name__ == "__main__": 
    app.run()
