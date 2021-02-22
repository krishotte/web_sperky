"""The RegisterController Module."""

from masonite.auth import Auth, MustVerifyEmail
from masonite.managers import MailManager
from masonite.request import Request
from masonite.validation import Validator
from masonite.view import View
from orator.exceptions.query import QueryException
from masonite.validation import MessageBag
from app.tools.SvkMustVerifyEmail import SvkMustVerifyEmail


class RegisterController:
    """The RegisterController class."""

    def __init__(self):
        """The RegisterController Constructor."""
        pass

    def show(self, view: View):
        """Show the registration page.

        Arguments:
            Request {masonite.request.request} -- The Masonite request class.

        Returns:
            masonite.view.View -- The Masonite View class.
        """
        return view.render("auth/register")

    def store(
        self,
        request: Request,
        mail_manager: MailManager,
        auth: Auth,
        validate: Validator,
    ):
        """Register the user with the database.

        Arguments:
            request {masonite.request.Request} -- The Masonite request class.

        Returns:
            masonite.request.Request -- The Masonite request class.
        """

        errors = request.validate(
            validate.required(["name", "email", "password"],
                              messages={
                                  "name": 'Meno je povinné',
                                  "email": "Email je povinný",
                                  "password": "Heslo je povinné",
                              }),
            validate.email(["email"], messages={'email': "Emailová adresa nie je platná"}),
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
            return request.back().with_errors(errors).with_input()

        try:
            user = auth.register(
                {
                    "name": request.input("name"),
                    "password": request.input("password"),
                    "email": request.input("email"),
                }
            )
        except QueryException as err:
            print(f' register user failed: {err}')
            bag = MessageBag()
            bag.add('error', 'Užívateľa nebolo možné zaregistrovať, už existuje iný s rovnakou emailovou adresou')
            return request.back().with_errors(bag)

        if isinstance(user, SvkMustVerifyEmail):
            user.verify_email(mail_manager, request)

        # Login the user
        if auth.login(request.input("email"), request.input("password")):
            # Redirect to the homepage
            return request.redirect("/dashboard/profile")

        # Login failed. Redirect to the register page.
        return request.back().with_input()
