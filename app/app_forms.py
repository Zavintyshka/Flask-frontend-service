from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, validators
from wtforms.validators import InputRequired, EqualTo, Length, Regexp

name_regexp_message = "{} must contain only Latin letters"
username_length_message = "username length must be between 4 and 15 characters"
username_regexp_message = "username can contain only Latin letters, numbers and underscores"
password_length_message = "password length must be at least 10 characters"
password_regexp_message = "password must contain at least one lowercase letter, one uppercase letter, one digit, and one special character"
password_equal_to_message = "Passwords must match"


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
    password = PasswordField("Password",
                             validators=[InputRequired(message="The field is required"),
                                         Length(min=10,
                                                message=password_length_message),
                                         Regexp(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{10,}$",
                                                message=password_regexp_message)
                                         ])
    repeated_password = PasswordField("Repeated password",
                                      validators=[InputRequired(),
                                                  EqualTo("password", message="Passwords must match")])


class UserLoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


class UserRegisterForm(FlaskForm):
    firstname = StringField("Firstname",
                            validators=[
                                InputRequired(message="The field is required"),
                                Regexp(r"^[A-Za-z]+$",
                                       message=name_regexp_message.format("firstname"))
                            ])
    lastname = StringField("Lastname",
                           validators=[
                               InputRequired(message="The field is required"),
                               Regexp(r"^[A-Za-z]+$",
                                      message=name_regexp_message.format("lastname"))
                           ])
    username = StringField("Username",
                           validators=[InputRequired(message="The field is required"),
                                       Length(min=4, max=15,
                                              message=username_length_message),
                                       Regexp(r"^\w+$",
                                              message=username_regexp_message)
                                       ])
    email = EmailField("E-mail",
                       validators=[InputRequired()])
    password = PasswordField("Password",
                             validators=[InputRequired(message="The field is required"),
                                         Length(min=10,
                                                message=password_length_message),
                                         Regexp(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{10,}$",
                                                message=password_regexp_message)
                                         ])
    repeat_password = PasswordField("Repeat Password",
                                    validators=[InputRequired(message="The field is required"),
                                                EqualTo("password",
                                                        message=password_equal_to_message)
                                                ])
