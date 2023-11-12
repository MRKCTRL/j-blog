from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField

##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()]
    password = PasswordField('Password', validators=[DataRequired()]
    name = StringField('Name', validators=[DataRequired()]
    submit = SubmitField('Sign Me up')

class LoginFlask(FlaskForm):
    email  = StringField('Email', validators=[DataRequired())
    password  = PasswordField('Password', validators=[DataRequired())
    submit = SubmitField('Let Me In')

    class CommnentForm(Form.Form):
        comment_text = CKEditor('Comment', validators=[DataRequired()])
        submit = SubmitField('Submit Comment')
        # content = forms.CharField(widget = CKEditorWidget())
#
# class Parent(Base):
#     __table__ = 'parent'
#     id = Column(Integer, primary_key=True)
#     children = relationship('child')
#
# class Child(Base):
#     __table__ = 'child'
#     id = Column(Integer, primary_key=True)
#     parent_id = Column(Integer, foreignKey('parent_id'))
