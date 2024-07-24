from wtforms import Form, StringField, EmailField


class UserDataForm(Form):
    firstname = StringField("Firstname:")
    lastname = StringField("Lastname:")
    username = StringField("Username:", render_kw={"readonly": True, "style": "color:gray"})
    email = EmailField("E-mail:")
    registered_at = StringField("Registered:", render_kw={"readonly": True, "style": "color:gray"})
