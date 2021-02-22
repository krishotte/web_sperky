import time
from masonite.auth.Sign import Sign


class SvkMustVerifyEmail:

    def verify_email(self, mail_manager, request):
        """Sends email for user verification

        Arguments:
            mail_manager {masonite.managers.MailManager} -- Masonite mail manager class.
            request {masonite.request.Request} -- Masonite request class.
        """
        mail = mail_manager.helper()
        sign = Sign()

        token = sign.sign("{0}::{1}".format(self.id, time.time()))
        # link = "{0}/email/verify/{1}".format(request.environ["HTTP_HOST"], token)
        link = "{0}/email/verify/{1}".format(request.header("APP_URL"), token)

        mail.to(self.email).template(
            "auth/verifymail", {"name": self.name, "email": self.email, "link": link}
        ).subject("Prosím potvrďte emailovú adresu").send()
