import os

from data import db_session
from flask import Flask, render_template, url_for
from data.users import User
from data.forms import RegisterForm
from werkzeug.utils import redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
@app.route('/index')
def index():
    base_params = {'css_path': url_for('static', filename='css/style.css')}
    session = db_session.create_session()
    users = session.query(User).all()
    return render_template('index.html', title='Users log', users=users, **base_params)


@app.route('/register', methods=['GET', 'POST'])
def register():
    base_params = {'css_path': url_for('static', filename='css/style.css')}
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.repeat_password.data:
            return render_template('register.html', title='Registration',
                                   form=form, message="Passwords doesn't match", **base_params)
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Registration', form=form,
                                   message='The user with this email is already registered',
                                   **base_params)
        user = User(
            email=form.email.data,
            surname=form.surname.data,
            name=form.name.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        try:
            user.age = int(form.age.data)
        except ValueError:
            user.age = None
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/')
    return render_template('register.html', title='Registration', form=form, **base_params)


if __name__ == '__main__':
    db_session.global_init(os.path.join('db', 'mars_explorer.db'))
    app.run()
