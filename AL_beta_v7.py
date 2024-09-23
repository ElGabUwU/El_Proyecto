from forms.login.form_login import FormLogin
from forms.master.form_master import MasterPanel
from MainAppConector import start_starter


def start_login():
    login = FormLogin()
    login.show()

if __name__ == "__main__":
    start_login()