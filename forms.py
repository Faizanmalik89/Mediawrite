from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField, SelectField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, Length, URL, Optional
from flask_wtf.file import FileAllowed

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class BlogForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    content = TextAreaField('Content', validators=[DataRequired()])
    featured_image = StringField('Featured Image URL (optional)', validators=[Optional(), URL()])
    image_file = FileField('Upload Image', validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Images only!')])
    submit = SubmitField('Save Blog')

class VideoForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Optional()])
    video_url = StringField('Video URL (YouTube, Vimeo, etc.)', validators=[Optional(), URL()])
    video_file = FileField('Upload Video File', validators=[Optional(), FileAllowed(['mp4', 'mov', 'avi', 'webm'], 'Videos only!')])
    thumbnail = StringField('Thumbnail URL (optional)', validators=[Optional(), URL()])
    thumbnail_file = FileField('Upload Thumbnail Image', validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Images only!')])
    submit = SubmitField('Save Video')

class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()])
    blog_id = HiddenField('Blog ID')
    video_id = HiddenField('Video ID')
    submit = SubmitField('Post Comment')

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')
