from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, BooleanField, SelectField, validators, PasswordField, SubmitField
from wtforms.validators import DataRequired


class HumanForm(FlaskForm):
    name = StringField('音乐人名', [DataRequired('音乐人名必填')])
    content = TextAreaField('音乐人简介', [DataRequired('音乐人简介必填')])
    img = FileField('图片', validators=[
        FileAllowed(['jpg', 'png'], '仅能上传图片!')
    ])


class StudioForm(FlaskForm):
    name = StringField('录音棚名称', [DataRequired('录音棚名称必填')])
    content = TextAreaField('录音棚简介', [DataRequired('录音棚简介必填')])
    img = FileField('图片', validators=[
        FileAllowed(['jpg', 'png'], '仅能上传图片!')
    ])


class NewsForm(FlaskForm):
    name = StringField('文章标题', [DataRequired('文章标题必填')])
    content = TextAreaField('文章内容', [DataRequired('文章内容必填')])
    img = FileField('图片', validators=[
        FileAllowed(['jpg', 'png'], '仅能上传图片!')
    ])


class UserLoginForm(FlaskForm):
    username = StringField('用户名', [DataRequired('用户名必填！')])
    password = PasswordField('密码', [DataRequired('密码必填！')])
