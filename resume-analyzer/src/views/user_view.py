from flask import render_template, request, redirect, url_for
from ..controllers.user_controller import UserController

user_controller = UserController()

def user_profile_view(user_id):
    user_data = user_controller.get_user_data(user_id)
    return render_template('user_profile.html', user=user_data)

def user_registration_view():
    if request.method == 'POST':
        user_data = request.form
        user_controller.register_user(user_data)
        return redirect(url_for('user_profile_view', user_id=user_data['id']))
    return render_template('user_registration.html')

def user_resume_upload_view(user_id):
    if request.method == 'POST':
        resume_file = request.files['resume']
        user_controller.upload_resume(user_id, resume_file)
        return redirect(url_for('user_profile_view', user_id=user_id))
    return render_template('user_resume_upload.html', user_id=user_id)