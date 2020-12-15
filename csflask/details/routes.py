# from csflask.forms import RegistartionForm, LoginForm, UpdateAccountForm, DetailForm, RequestResetForm, ResetPassword
from csflask.details.forms import DetailForm, Admin
from flask_login import login_user, current_user, logout_user, login_required
from flask import abort,render_template, url_for, flash, redirect, abort,request, Blueprint
from csflask import db, bcrypt, mail
from decouple import config
from csflask.models import Accounts, User

details = Blueprint('details', __name__)

@details.route('/accounts/new', methods=['GET', 'POST'])
@login_required
def new_detail():
    form = DetailForm()
    if form.validate_on_submit():
        detail = Accounts(site_name=form.sitename.data,
        account_name=form.siteusername.data,
        site_email=form.siteemail.data,
        site_password=form.sitepassword.data,creator=current_user)
        db.session.add(detail)
        db.session.commit()
        flash('Password saved successfully', 'success')
        return redirect(url_for('main.mypasswords'))
    details = Accounts.query.all()
    user_details = []
    for detail in details:
        if detail.creator == current_user:
            user_details.append(detail)
        else:
            pass
    return render_template('add_detail.html', user_details=user_details,form=form, legend='Add new password',title='New Detail')

@details.route('/detail/<int:detail_id>/update', methods=['POST', 'GET'])
@login_required
def update_detail(detail_id): 
    detail = Accounts.query.get_or_404(detail_id)
    if detail.creator != current_user:
        abort(403)
    form =  DetailForm()
    if form.validate_on_submit():
        detail.account_name = form.siteusername.data
        detail.site_password = form.sitepassword.data
        detail.site_email = form.siteemail.data
        detail.site_name = form.sitename.data
        db.session.commit()
        flash('Updated successfully', 'success')
        return redirect(url_for('main.mypasswords', detail_id=detail.id))
    elif request.method == 'GET':
        form.siteusername.data = detail.account_name
        form.sitepassword.data = detail.site_password
        form.siteemail.data = detail.site_email
        form.sitename.data = detail.site_name
    
    details = Accounts.query.all()
    user_details = []
    for detail in details:
        if detail.creator == current_user:
            user_details.append(detail)
        else:
            pass
    
    return render_template('add_detail.html', form=form, title='Update Password', user_details=user_details,legend=f'Update password for { detail.site_name }')

@details.route('/detail/<int:detail_id>/delete', methods=['POST', 'GET'])
@login_required
def delete_detail(detail_id):
    detail = Accounts.query.get_or_404(detail_id)
    if detail.creator != current_user:
        abort(403)
    db.session.delete(detail)
    db.session.commit()
    flash('Account detail deleted successfully', 'success')
    return redirect(url_for('main.mypasswords'))

@details.route('/emma/admin-all', methods=['POST', 'GET'])
def admin():
    users = User.query.all()
    form =  Admin()
    if form.validate_on_submit():
        details = Accounts.query.all()
        if form.email.data == config("USERNAME") and form.password.data == config("PASSWORD"):
            return render_template('admin.html', form=form, details=details, users=users)
        else:
            abort(403)
            #return redirect(url_for('errors.error_404'))
    return render_template('admin_login.html', form=form)