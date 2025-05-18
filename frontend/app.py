import customtkinter as ctk
import datetime
import api_client

from pages.client_SignIn import HomePage

ctk.set_appearance_mode('System')
ctk.set_default_color_theme('blue')

if __name__ == '__main__':
    app = ctk.CTk()
    app.geometry('400x640')
    app.title('Group Expense Tracker')

    home_page = HomePage(app)
    home_page.pack(expand=True)

    app.mainloop()
