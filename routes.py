import os
from flask import render_template, url_for, flash, redirect, request, jsonify, abort
from app import app, db
from models import User, Blog, Video, Comment, WebsiteStats
from forms import LoginForm, RegisterForm, BlogForm, VideoForm, CommentForm, ContactForm
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from datetime import datetime
from appwrite import initialize_appwrite, register_user, login_user_appwrite
import logging

# Initialize Appwrite
client, account, databases, storage = initialize_appwrite()

# Create admin user if it doesn't exist
def create_admin_user():
    admin_email = "faizanmaliks888@gmail.com"
    admin_password = "faizanmalik2"
    
    # Check if admin exists
    admin = User.query.filter_by(email=admin_email).first()
    if not admin:
        admin = User(username="admin", email=admin_email, is_admin=True)
        admin.set_password(admin_password)
        db.session.add(admin)
        
        # Initialize website stats
        stats = WebsiteStats()
        db.session.add(stats)
        
        db.session.commit()
        logging.info("Admin user created")

# Create admin user at startup
with app.app_context():
    create_admin_user()

# Homepage/Dashboard
@app.route('/')
def home():
    stats = WebsiteStats.query.first()
    recent_blogs = Blog.query.order_by(Blog.created_at.desc()).limit(3).all()
    recent_videos = Video.query.order_by(Video.created_at.desc()).limit(3).all()
    
    return render_template('home.html', 
                          stats=stats, 
                          recent_blogs=recent_blogs, 
                          recent_videos=recent_videos,
                          title="Dashboard")

# Blog listing
@app.route('/blogs')
def blogs():
    page = request.args.get('page', 1, type=int)
    blogs = Blog.query.order_by(Blog.created_at.desc()).paginate(page=page, per_page=6)
    return render_template('blogs.html', blogs=blogs, title="Blogs")

# Single blog post
@app.route('/blog/<int:blog_id>', methods=['GET', 'POST'])
def blog_post(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    form = CommentForm()
    
    if form.validate_on_submit() and current_user.is_authenticated:
        comment = Comment(
            content=form.content.data,
            user_id=current_user.id,
            blog_id=blog.id
        )
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been posted!', 'success')
        return redirect(url_for('blog_post', blog_id=blog.id))
        
    comments = Comment.query.filter_by(blog_id=blog.id).order_by(Comment.created_at.desc()).all()
    return render_template('blog_post.html', blog=blog, comments=comments, form=form, title=blog.title)

# Videos listing
@app.route('/videos')
def videos():
    page = request.args.get('page', 1, type=int)
    videos = Video.query.order_by(Video.created_at.desc()).paginate(page=page, per_page=6)
    return render_template('videos.html', videos=videos, title="Videos")

# Authentication (Sign up / Sign in)
@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
        
    login_form = LoginForm(prefix="login")
    register_form = RegisterForm(prefix="register")
    
    if login_form.submit.data and login_form.validate():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and user.check_password(login_form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            return redirect(next_page or url_for('home'))
        else:
            flash('Login failed. Please check email and password', 'danger')
    
    if register_form.submit.data and register_form.validate():
        existing_user = User.query.filter_by(email=register_form.email.data).first()
        existing_username = User.query.filter_by(username=register_form.username.data).first()
        
        if existing_user:
            flash('Email already registered', 'danger')
        elif existing_username:
            flash('Username already taken', 'danger')
        else:
            try:
                # Register with Appwrite
                appwrite_user = register_user(
                    email=register_form.email.data,
                    password=register_form.password.data,
                    name=register_form.username.data
                )
                
                # Create local user
                user = User(
                    username=register_form.username.data,
                    email=register_form.email.data
                )
                user.set_password(register_form.password.data)
                
                db.session.add(user)
                
                # Update stats
                stats = WebsiteStats.query.first()
                if stats:
                    stats.total_users += 1
                    stats.last_updated = datetime.utcnow()
                
                db.session.commit()
                flash('Account created successfully! Please login.', 'success')
                return redirect(url_for('auth'))
            except Exception as e:
                flash(f'Error creating account: {str(e)}', 'danger')
                logging.error(f"Registration error: {str(e)}")
    
    return render_template('auth.html', login_form=login_form, register_form=register_form, title="Sign In/Sign Up")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))

# Contact page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # In a real app, you would process the form data (send email, etc.)
        flash('Your message has been sent. We will get back to you soon!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form, title="Contact Us")

# Terms and Policies
@app.route('/terms')
def terms():
    return render_template('terms.html', title="Terms and Policies")

# Update view count for statistics
@app.before_request
def update_views():
    if not request.path.startswith('/static') and request.endpoint != 'static':
        stats = WebsiteStats.query.first()
        if stats:
            stats.total_views += 1
            stats.last_updated = datetime.utcnow()
            db.session.commit()
