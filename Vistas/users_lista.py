import tkinter as tk
from tkinter import ttk
import sqlite3
from Library.librerias import search_all_users

def show_users():
    root = tk.Tk()
    root.title("Usuarios y Roles")
    # Crear el Treeview
    style = ttk.Style()
    style.theme_use('alt')
    style.configure("mystyle.Treeview", 
                    highlightthickness=0, 
                    bd=0, 
                    font=('PressStart2P', 11),  
                    background="#D3D3D3",  
                    foreground="black",    
                    rowheight=25)
            
    style.configure("mystyle.Treeview.Heading", 
                    font=('PressStart2P', 13,),  
                    background="#6D6CFA",          
                    foreground="black") 
            
    style.map("mystyle.Treeview.Heading", 
                background=[("active", "#6D6CFA")], 
                foreground=[("active", "black")])

    style.map("mystyle.Treeview", 
                background=[("selected", "#94AAD6")],  
                foreground=[("selected", "black")])

    treeview = ttk.Treeview(root, columns=("Usuario", "Rol"), style="mystyle.Treeview")
    treeview.heading("#0", text="ID")
    treeview.heading("Usuario", text="Usuario")
    treeview.heading("Rol", text="Rol")

    # Obtener los datos de la función search_all_users
    users_data = search_all_users()
    for i, (usuario, rol) in enumerate(users_data[0], start=1):
        treeview.insert("", i, text=str(i), values=(usuario, rol))

    treeview.pack()
    root.mainloop()

if __name__ == "__main__":
    main()