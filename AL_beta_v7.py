from Login.backend.form_login import FormLogin
from Login.frontend.form_master import MasterPanel
from MainAppConector import start_starter

def start_login():
    login = FormLogin()
    login.show()

if __name__ == "__main__":
    start_login()