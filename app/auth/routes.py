from . import auth
from .. import database
from .forms import LoginForm, RegistrationForm
from ..email import send_email
from ..models import User
from flask import render_template, flash, redirect, request, url_for
from flask_login import login_user, logout_user, login_required, current_user


@auth.before_app_request
def before_request():
    if (current_user.is_authenticated
        and not current_user.confirmed
        and request.blueprint != 'auth'
        and request.blueprint != 'static'):
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect('main.index')
    return render_template('auth/unconfirmed.html', user=current_user)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next_page = request.args.get('next')
            if next_page is None or not next_page.startswith('/'):
                next_page = url_for('main.index')
            return redirect(next_page)
        else:
            flash('Invalid email or password.')
            form.data['password'] = ''
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data.lower()
        if User.query.filter_by(email=email).first():
            flash('The email is already registered.')
            return render_template('auth/registration.html', form=form)
        elif User.query.filter_by(username=username).first():
            flash('The username is already taken.')
            return render_template('auth/registration.html', form=form)
        user = User()
        user.username = username
        user.email = email
        user.password = form.password.data
        database.session.add(user)
        database.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 
                   'Registration confirmation',
                   'mail/registration_letter',
                   user=user,
                   token=token,
                   link=url_for('auth.confirm', token=token, _external=True))
        login_user(user, remember=False)
        return redirect(url_for('main.index'))
    return render_template('auth/registration.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        database.session.commit()
        flash('Your account has been confirmed.')
    else:
        flash('The confirmation link is invalid or has expired. Please sign up again.')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email,
               'Registration confirmation',
               'mail/registration_letter',
               user=current_user,
               token=token,
               link=url_for('auth.confirm', token=token, _external=True))
    flash('A new confirmation letter has been sent to ' + current_user.email)
    return redirect(url_for('main.index'))