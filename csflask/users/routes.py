from flask import Blueprint, session, sessions
from csflask.users.forms import RegistartionForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPassword, ConfirmEmailForm, ResetPasswordCode
from flask_login import login_user, current_user, logout_user, login_required
from flask import render_template, url_for, flash, redirect, abort,request
from csflask import db, bcrypt, mail
from csflask.models import User, Accounts
from csflask.users.utils import save_picture, send_reset_email, send_confirm_email, send_reset_code

users = Blueprint('users', __name__)

@users.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.mypasswords'))
    form = RegistartionForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # user = User(username=form.username.data, email=form.email.data, password=hashed_pass)

        session['curr_mail'] = form.email.data
        session['curr_name'] = form.username.data
        session['curr_pass'] = hashed_pass

        x = send_confirm_email(form.email.data)
        session['ver_code'] = x

        flash(f'An email has been sent to {form.email.data} for verification purpose.', 'info')
        return redirect(url_for('users.verify'))
    return render_template('register.html', form=form, title='Register')
    
@users.route('/verify', methods=['POST', 'GET'])
def verify():
    x = session.get('ver_code', None)
    if current_user.is_authenticated:
        return redirect(url_for('main.mypasswords'))
    form = ConfirmEmailForm()
    if form.validate_on_submit():
        if form.code.data == str(x):
            flash(f'Your email has been verified. You can now proceed to login', 'info')

            mail = session.get('curr_mail', None)
            passw = session.get('curr_pass', None)
            name = session.get('curr_name', None)

            user = User(username=name, email=mail, password=passw)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('users.login'))
        else:
            flash(f'Invalid verification code. Please check your email and try again', 'danger')
            return redirect(url_for('users.verify'))
    return render_template('confirm_email.html', form=form)

@users.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.mypasswords'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            # flash('Login Successful', 'success')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('main.mypasswords'))
        else:
            flash('Incorrect Username or Password', 'danger')
    return render_template('login.html', form=form, title='Login')

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route('/myaccount', methods=['POST', 'GET'])
@login_required
def myaccount():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        # try:
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        # current_user.email = form.email.data
        
        db.session.commit()

        flash('Account updated successfully', 'success')
        return redirect(url_for('users.myaccount'))
        # except UnboundLocalError:
        #     return redirect(url_for('main.mypasswords'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        # form.email.data = current_user.email
    else:
        return redirect(url_for('main.mypasswords'))
    details = Accounts.query.all()

    user_details = []
    for detail in details:
        if detail.creator == current_user:
            user_details.append(detail)
        else:
            pass
    image_file = url_for('static', filename='img/'+current_user.image_file)
    return render_template('myaccount.html',user_details=user_details ,image_file=image_file, form=form, title='Account Info')


@users.route('/request_reset_code', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.mypasswords'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        # Eamil that needs to be reset
        session['reset_mail'] = form.email.data

        # Get the 6 digit code from a previously defined function
        x = send_reset_code(form.email.data)
        session['reset_code'] = x

        # send_reset_email(user)
        flash('The Reset Code has been sent to your email', 'info')
        return redirect(url_for('users.reset_code'))
    return render_template('reset_request.html', form=form, title='Request Code')


@users.route('/reset_code', methods=['POST', 'GET'])
def reset_code():
    x = session.get('reset_code', None)
    if current_user.is_authenticated:
        return redirect(url_for('main.mypasswords'))
    form = ResetPasswordCode()
    if form.validate_on_submit():
        if form.code.data == str(x):
            flash(f'Password Reset Successfuly', 'success')
            return redirect(url_for('users.reset_password'))
        else:
            flash(f'Invalid verification code. Please check your email and try again', 'danger')
            return redirect(url_for('users.reset_code'))
    return render_template('reset_code.html', form=form)

@users.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.mypasswords'))
    reset_mail = session.get('reset_mail', None)
    user = User.query.filter_by(email=reset_mail).first()

    if user is None:
        flash('Invalid or Expired Reset code', 'warning')
        return redirect(url_for('users.reset_code'))
    form = ResetPassword()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pass
        db.session.commit()

        flash(f'Your password has been updated successfully!', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', form=form, title='Reset Password')