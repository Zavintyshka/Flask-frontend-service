from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, validators
from wtforms.validators import InputRequired, EqualTo


class UserDataForm(FlaskForm):
    firstname = StringField("Firstname:",
                            validators=[
                                validators.Length(min=4, max=20,
                                                  message="Firstname must be between 4 and 20 characters"),
                                validators.Regexp("^[A-Za-z]+$",
                                                  message="Firstname must contain only a-z, A-Z characters")
                            ]
                            )
    lastname = StringField("Lastname:",
                           validators=[
                               validators.Length(min=4, max=20,
                                                 message="Lastname must be between 4 and 20 characters"),
                               validators.Regexp("^[A-Za-z]+$",
                                                 message="Lastname must contain only a-z, A-Z characters")
                           ]
                           )
    username = StringField("Username:", render_kw={"readonly": True, "style": "color:gray"})
    email = EmailField("E-mail:")
    registered_at = StringField("Registered:", render_kw={"readonly": True, "style": "color:gray"})


class ResetPasswordForm(FlaskForm):
    email = EmailField("E-mail", validators=[InputRequired()])
    username = StringField("Username", validators=[InputRequired()])


class ChangePasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[InputRequired()])
    repeated_password = PasswordField("Repeated password",
                                      validators=[InputRequired(),
                                                  EqualTo("password", message="Passwords must match.")])


class UserLoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


class UserRegisterForm(FlaskForm):
    firstname = StringField("Firstname", validators=[InputRequired()])
    lastname = StringField("Lastname", validators=[InputRequired()])
    username = StringField("Username", validators=[InputRequired()])
    email = EmailField("E-mail", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    repeat_password = PasswordField("Repeat Password", validators=[InputRequired()])
