"""A PasswordController Module."""

import uuid

from masonite import env, Mail, Session
from masonite.auth import Auth
from masonite.helpers import config, password as bcrypt_password
from masonite.request import Request
from masonite.view import View
from masonite.validation import Validator
from config.auth import AUTH


class PasswordController:
    """Password Controller."""

    def forget(self, view: View, auth: Auth):
        return view.render("auth/forget", {"app": config("application"), "Auth": auth})

    def reset(self, view: View, request: Request, auth: Auth):
        token = request.param("token")
        user = AUTH["guards"]["web"]["model"].where("remember_token", token).first()
        if user:
            return view.render(
                "auth/reset",
                {"token": token, "app": config("application"), "Auth": auth},
            )

    def send(self, request: Request, session: Session, mail: Mail, validate: Validator):
        print(f' session email: {request.session.get("email")}')
        errors = request.validate(
            validate.required("email"),
            validate.email("email", messages={'email': "Emailová adresa nie je platná"})
        )

        print(f' errors: {errors}')
        if errors:
            return request.back().with_errors(errors)

        email = request.input("email")
        user = AUTH["guards"]["web"]["model"].where("email", email).first()

        if user:
            if not user.remember_token:
                user.remember_token = str(uuid.uuid4())
                user.save()

            message = "Prosím, kliknite na {}/password/{}/reset pre zresetovanie hesla".format(
                env("APP_URL"), user.remember_token
            )
            link = "{}/password/{}/reset".format(
                env("APP_URL"), user.remember_token)

            # mail.subject("Inštrukcie pre zresetovanie hesla").to(user.email).send(message)
            mail.to(user.email).template(
                "email/password_reset", {"name": user.name, "email": user.email, "link": link}
            ).subject("Inštrukcie pre zresetovanie hesla").send()

        session.flash(
            "success",
            #"If we found that email in our system then the email has been sent. Please follow the instructions in the email to reset your password.",
            "Ak emailová adresa existuje v našom systéme, email bol odoslaný."
            "Pre resetovanie hesla prosím postupujte podľa inštrukcií uvedených v emaili."
        )
        return request.redirect("/password")

    def update(self, request: Request, validate: Validator):
        errors = request.validate(
            validate.required("password"),
            # TODO: only available in masonite latest versions (which are not compatible with Masonite 2.2)
            validate.strong(
                "password",
                length=8,
                special=1,
                uppercase=1,
                # breach=True checks if the password has been breached before.
                # Requires 'pip install pwnedapi'
                breach=False,
                messages={
                    'password': 'Heslo musí obsahovať minimálne 8 znakov, jeden špeciálny znak, jedno veľké písmeno a dve číslice'
                }
            ),
        )

        if errors:
            return request.back().with_errors(errors)

        user = (
            AUTH["guards"]["web"]["model"]
            .where("remember_token", request.param("token"))
            .first()
        )
        if user:
            user.password = bcrypt_password(request.input("password"))
            user.save()
            return request.redirect("/login")
