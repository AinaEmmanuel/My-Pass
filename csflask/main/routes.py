from flask import Blueprint, render_template, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from csflask.models import Accounts
from flask import url_for
from flask_login import current_user
main = Blueprint('main', __name__)

@main.route('/mypasswords')
@login_required
def mypasswords():
    #page = request.args.get('page', 1, type=int)
    details = Accounts.query.all()#order_by(Accounts.date_added.desc()).paginate(page=page, per_page=5)
    if current_user.is_authenticated:
        try:
            user_details = []
            for detail in details:
                if detail.creator == current_user:
                    user_details.append(detail)
                else:
                    pass
            image_file = url_for('static', filename='img/'+current_user.image_file)
            return render_template('mypasswords.html', user_details=user_details, details=details, image_file=image_file)
        except UnboundLocalError:
            return redirect(url_for('users.login'))
    return render_template('mypasswords.html', user_details=user_details, details=details)

@main.route('/')
def home():
    return render_template('home2.html', title='Home')