import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
#from Library.librerias import
from Library.db_pokimon import *
import random
import subprocess
from backend.Libros_Frames_2 import *
from backend.Usuarios_Frames_3 import *
from backend.Prestamos_Frames_2 import *
import sys
from pathlib import Path
# Añade el directorio raíz del proyecto al PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parent))
from forms.login.form_login import FormLogin, FormLoginDesigner
from forms.master.form_master import MasterPanel

if __name__ == "__main__":
   app = FormLogin()