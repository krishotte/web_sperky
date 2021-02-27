"""A LoginController Module."""

from masonite.auth import Auth
from masonite.request import Request
from masonite.validation import Validator
from masonite.view import View


class LoginController:
    """Login Form Controller."""

    def __init__(self):
        """LoginController Constructor."""
        pass

    def show(self, request: Request, view: View):
        """Show the login page.

        Arguments:
            request {masonite.request.Request} -- The Masonite request class.
            view {masonite.view.View} -- The Masonite view class.

        Returns:
            masonite.view.View -- Returns the Masonite view class.
        """
        caller = get_caller_path(request)
        print(f' login caller: {caller}')

        if request.user():
            return request.redirect("/home")

        return view.render("auth/login", {
            'caller': caller,
        })

    def store(self, request: Request, auth: Auth, validate: Validator):
        """Login the user.

        Arguments:
            request {masonite.request.Request} -- The Masonite request class.
            auth {masonite.auth.auth} -- The Masonite auth class.
            validate {masonite.validator.Validator} -- The Masonite Validator class.

        Returns:
            masonite.request.Request -- The Masonite request class.
        """
        caller = request.input('caller_path')
        print(f' post caller: {caller}')

        errors = request.validate(
            validate.required(["email", "password"]),
            validate.email("email"),
        )

        if errors:
            return request.back().with_errors(errors).with_input()

        if auth.login(request.input("email"), request.input("password")):
            # return request.redirect("/dashboard/profile")
            return request.redirect(caller)

        return request.back().with_errors({"email": ["Email alebo heslo je nesprávne."]})

    def logout(self, request: Request, auth: Auth):
        """Log out the user.

        Arguments:
            request {masonite.request.Request} -- The Masonite request class.
            auth {masonite.auth.auth} -- The Masonite auth class.

        Returns:
            masonite.request.Request -- The Masonite request class.
        """
        request.session.reset()
        auth.logout()
        caller = get_caller_path(request)
        # return request.redirect("/login")
        return request.redirect(caller)


def get_caller_path(request):
    caller_http = request.header('HTTP_REFERER')
    http_host = request.header('HTTP_HOST')
    caller_subpath = caller_http.split(http_host)
    print(f' caller: {caller_subpath}')

    return caller_subpath[-1]