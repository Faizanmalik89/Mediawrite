import os
import uuid
from flask import render_template, url_for, flash, redirect, request, abort
from app import app, db
from models import User, Blog, Video, Comment, WebsiteStats
from forms import BlogForm, VideoForm
from flask_login import current_user, login_required
from datetime import datetime
import logging
from werkzeug.utils import secure_filename

# Save uploaded file and return path
def save_file(file, file_type):
    if file and file.filename:
        # Generate a unique filename to avoid collisions
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        
        # Determine the upload folder based on file type
        if file_type == 'image':
            upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'images')
        elif file_type == 'video':
            upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'videos')
        else:
            upload_folder = app.config['UPLOAD_FOLDER']
            
        # Ensure the upload folder exists
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
            
        # Save the file
        file_path = os.path.join(upload_folder, unique_filename)
        file.save(file_path)
        
        # Return the URL-friendly path
        # Convert absolute path to URL path that starts with /static/
        return '/' + file_path
    
    return None

# Admin panel access check
def admin_required(f):
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return login_required(decorated_function)

# Admin Panel - Main
@app.route('/admin')
@admin_required
def admin_panel():
    stats = WebsiteStats.query.first()
    recent_blogs = Blog.query.order_by(Blog.created_at.desc()).limit(5).all()
    recent_videos = Video.query.order_by(Video.created_at.desc()).limit(5).all()
    
    return render_template('admin_panel.html', 
                           stats=stats, 
                           recent_blogs=recent_blogs, 
                           recent_videos=recent_videos,
                           title="Admin Panel")

# Admin - Blog Management
@app.route('/admin/blogs', methods=['GET', 'POST'])
@admin_required
def admin_blogs():
    form = BlogForm()
    
    if form.validate_on_submit():
        # Handle image upload if provided
        featured_image = form.featured_image.data
        
        # Check if file upload is provided
        if form.image_file.data:
            featured_image = save_file(form.image_file.data, 'image')
            
        blog = Blog(
            title=form.title.data,
            content=form.content.data,
            featured_image=featured_image,
            user_id=current_user.id
        )
        db.session.add(blog)
        
        # Update stats
        stats = WebsiteStats.query.first()
        if stats:
            stats.total_blogs += 1
            stats.last_updated = datetime.utcnow()
            
        db.session.commit()
        flash('Blog post created successfully!', 'success')
        return redirect(url_for('admin_blogs'))
    
    blogs = Blog.query.order_by(Blog.created_at.desc()).all()
    return render_template('admin_blogs.html', form=form, blogs=blogs, title="Manage Blogs")

# Admin - Edit Blog
@app.route('/admin/blogs/edit/<int:blog_id>', methods=['GET', 'POST'])
@admin_required
def edit_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    form = BlogForm()
    
    if form.validate_on_submit():
        blog.title = form.title.data
        blog.content = form.content.data
        
        # Keep existing image URL unless updated
        featured_image = form.featured_image.data
        
        # Check if new file is uploaded
        if form.image_file.data:
            featured_image = save_file(form.image_file.data, 'image')
            
        blog.featured_image = featured_image
        blog.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Blog post updated successfully!', 'success')
        return redirect(url_for('admin_blogs'))
    
    elif request.method == 'GET':
        form.title.data = blog.title
        form.content.data = blog.content
        form.featured_image.data = blog.featured_image
    
    return render_template('admin_blogs.html', form=form, blogs=Blog.query.all(), 
                           editing=True, blog_id=blog_id, title="Edit Blog")

# Admin - Delete Blog
@app.route('/admin/blogs/delete/<int:blog_id>', methods=['POST'])
@admin_required
def delete_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    
    # Delete associated comments first
    Comment.query.filter_by(blog_id=blog_id).delete()
    
    db.session.delete(blog)
    
    # Update stats
    stats = WebsiteStats.query.first()
    if stats and stats.total_blogs > 0:
        stats.total_blogs -= 1
        stats.last_updated = datetime.utcnow()
        
    db.session.commit()
    flash('Blog post deleted!', 'success')
    return redirect(url_for('admin_blogs'))

# Admin - Video Management
@app.route('/admin/videos', methods=['GET', 'POST'])
@admin_required
def admin_videos():
    form = VideoForm()
    
    if form.validate_on_submit():
        # Handle file uploads if provided
        video_url = form.video_url.data
        thumbnail = form.thumbnail.data
        
        # Check if video file upload is provided
        if form.video_file.data:
            video_url = save_file(form.video_file.data, 'video')
            
        # Check if thumbnail image upload is provided
        if form.thumbnail_file.data:
            thumbnail = save_file(form.thumbnail_file.data, 'image')
        
        video = Video(
            title=form.title.data,
            description=form.description.data,
            video_url=video_url,
            thumbnail=thumbnail,
            user_id=current_user.id
        )
        db.session.add(video)
        
        # Update stats
        stats = WebsiteStats.query.first()
        if stats:
            stats.total_videos += 1
            stats.last_updated = datetime.utcnow()
            
        db.session.commit()
        flash('Video added successfully!', 'success')
        return redirect(url_for('admin_videos'))
    
    videos = Video.query.order_by(Video.created_at.desc()).all()
    return render_template('admin_videos.html', form=form, videos=videos, title="Manage Videos")

# Admin - Edit Video
@app.route('/admin/videos/edit/<int:video_id>', methods=['GET', 'POST'])
@admin_required
def edit_video(video_id):
    video = Video.query.get_or_404(video_id)
    form = VideoForm()
    
    if form.validate_on_submit():
        video.title = form.title.data
        video.description = form.description.data
        
        # Keep existing values unless updated
        video_url = form.video_url.data
        thumbnail = form.thumbnail.data
        
        # Check if video file upload is provided
        if form.video_file.data:
            video_url = save_file(form.video_file.data, 'video')
            
        # Check if thumbnail image upload is provided
        if form.thumbnail_file.data:
            thumbnail = save_file(form.thumbnail_file.data, 'image')
            
        video.video_url = video_url
        video.thumbnail = thumbnail
        video.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Video updated successfully!', 'success')
        return redirect(url_for('admin_videos'))
    
    elif request.method == 'GET':
        form.title.data = video.title
        form.description.data = video.description
        form.video_url.data = video.video_url
        form.thumbnail.data = video.thumbnail
    
    return render_template('admin_videos.html', form=form, videos=Video.query.all(), 
                           editing=True, video_id=video_id, title="Edit Video")

# Admin - Delete Video
@app.route('/admin/videos/delete/<int:video_id>', methods=['POST'])
@admin_required
def delete_video(video_id):
    video = Video.query.get_or_404(video_id)
    
    # Delete associated comments first
    Comment.query.filter_by(video_id=video_id).delete()
    
    db.session.delete(video)
    
    # Update stats
    stats = WebsiteStats.query.first()
    if stats and stats.total_videos > 0:
        stats.total_videos -= 1
        stats.last_updated = datetime.utcnow()
        
    db.session.commit()
    flash('Video deleted!', 'success')
    return redirect(url_for('admin_videos'))
