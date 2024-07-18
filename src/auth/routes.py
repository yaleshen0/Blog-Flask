from flask import Flask, request, url_for, flash, redirect, render_template
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from . import auth_bp
from ..dtos.user import user_dto
from ..models.user import User

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # remember = request.form.get('remember')
        user = user_dto.get_by_email(email)
        if not user or not check_password_hash(user.password, password):
            flash('Email and/or password not correct')
            return redirect('login')
        user.authenticated = True
        login_user(user)
        return redirect(url_for('post.index'))
    return render_template('auth/login.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        # if email already existed, return to signup
        user = User.query.filter_by(email = email).first()
        if user:
            flash('Email address already exists')
            return redirect('/signup')
        new_user = User(name= name, email= email, password=generate_password_hash(password))
        user_dto.create_user(new_user)
        flash('Registered successfully')
        return redirect('/login')
    elif request.method=='GET':
        return render_template('auth/signup.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout successfully")
    return redirect('/login')
