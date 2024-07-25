from wtforms import Form, StringField, EmailField, validators


class UserDataForm(Form):
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
