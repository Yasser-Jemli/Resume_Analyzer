from flask import Blueprint, render_template, request, redirect, url_for, flash, session

admin_view = Blueprint('admin', __name__)

# Import controller after blueprint creation to avoid circular import
from ..controllers.admin_controller import AdminController
admin_controller = AdminController()

@admin_view.route('/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if admin_controller.authenticate(username, password):
            session['admin_logged_in'] = True
            return redirect(url_for('admin.admin_dashboard'))
        else:
            flash('Invalid credentials', 'error')
    
    return render_template('admin/admin_login.html')

@admin_view.route('/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.admin_login'))
    users = admin_controller.get_all_users()
    return render_template('admin/dashboard.html', users=users)

@admin_view.route('/user/<int:user_id>')
def view_user_data(user_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.admin_login'))
    user_data = admin_controller.get_user_data(user_id)
    return render_template('user_data.html', user=user_data)

@admin_view.route('/user/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.admin_login'))
    admin_controller.delete_user(user_id)
    return redirect(url_for('admin.admin_dashboard'))

@admin_view.route('/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin.admin_login'))