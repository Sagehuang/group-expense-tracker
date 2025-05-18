import customtkinter as ctk
import datetime
import api_client

from pages.client_SignIn import SignIn
from pages.homepage.client_HomePage import HomePage
from pages.homepage.client_AddGroup import AddGroup
from pages.homepage.client_JoinGroup import JoinGroup
from pages.homepage.client_ViewGroup import ViewGroup
from pages.homepage.expenses.client_AddExpense import AddExpense
from pages.homepage.expenses.client_EditExpense_undone import EditExpense
from pages.homepage.expenses.client_ViewMembers import ViewMembers
from pages.homepage.expenses.client_SettleUp import SettleUp

ctk.set_appearance_mode('System')
ctk.set_default_color_theme('blue')

if __name__ == '__main__':
    app = ctk.CTk()
    app.geometry('400x640')
    app.title('Group Expense Tracker')

    sign_in = SignIn(app)
    sign_in.pack(expand=True)

    app.mainloop()
