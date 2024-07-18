from flask import Flask, request, url_for, flash, redirect, render_template
from flask_login import current_user, login_required, user_unauthorized
from . import post_bp
# from src.models.post import Post
from ..dtos.post import post_dto
from ..models.post import Post
from datetime import datetime

@post_bp.route('/')
@login_required
def index():
    user_id=current_user.id
    posts = post_dto.get_by_user(user_id)
    return render_template('post/index.html', name=current_user.name, posts=posts)

@post_bp.route('/create', methods=['POST', 'GET'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        error=None
        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
            
        new_post = Post(title=title, content=content, created_at=datetime.now(), created_by=current_user.id)
        post_dto.create_post(new_post=new_post)
        flash('Post created!')
        return redirect('/')
    
    return render_template('post/create.html')

@post_bp.route('/<int:post_id>', methods=['GET'])
@login_required
def get_post(post_id):
    post = post_dto.get_by_id(post_id)
    if post==None:
        return render_template("errors/404.html"), 404
    if (current_user.id!=post.created_by):
        return render_template("errors/401.html"), 401
    return render_template('post/create.html', post=post)

@post_bp.route('/<int:post_id>/update', methods=['POST'])
@login_required
def update(post_id):
    post = post_dto.get_by_id(post_id)
    if post==None:
        return render_template("errors/404.html"), 404
    if (current_user.id!=post.created_by):
        return render_template("errors/401.html"), 401
    title = request.form['title']
    content = request.form['content']
    error=None
    if not title:
        error = 'Title is required.'

    if error is not None:
        flash(error)
        
    updated_obj = {
        'title': title,
        'content': content
    }
    post_dto.update_by_id(post_id, updated_obj=updated_obj)
    flash('Post updated successfully!')
    return redirect('/')

@post_bp.route('/<int:post_id>/delete', methods=['POST',])
@login_required
def delete(post_id):
    post = post_dto.get_by_id(post_id)
    if post==None:
        return render_template("errors/404.html"), 404
    if (current_user and current_user.id!=post.created_by):
        return render_template("errors/401.html"), 401
    post_dto.delete_by_id(post_id)
    flash('Post deleted successfully!')
    return redirect('/')