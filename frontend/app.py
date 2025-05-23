import customtkinter as ctk
from datetime import datetime
import api_client

from pages.SignIn import SignIn
from pages.homepage.HomePage import HomePage
from pages.homepage.AddGroup import AddGroup
from pages.homepage.JoinGroup import JoinGroup
from pages.homepage.ViewGroup import ViewGroup
from pages.homepage.expenses.AddExpense import AddExpense
from pages.homepage.expenses.EditExpense import EditExpense
from pages.homepage.expenses.ViewMembers import ViewMembers
from pages.homepage.expenses.SettleUp import SettleUp

ctk.set_appearance_mode('System')
ctk.set_default_color_theme('blue')


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 跨頁面紀錄 user_id, clicked_group_id, clicked_expense_id
        self.user_id = None
        self.clicked_group_id = None
        self.clicked_expense_id = None

        self.geometry('400x640')
        # self.minsize(400, 640)
        self.title('Group Expense Tracker')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # 加一個主 Frame 當容器
        self.container = ctk.CTkFrame(self)
        self.container.grid(row=0, column=0, sticky='nsew')
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # 建立一個容器來放所有頁面
        self.pages = {}

        # 初始化頁面
        self.init_pages()

        # 顯示初始頁面
        self.show_page('SignIn')

    def init_pages(self):
        # 建立所有頁面的實例並存入self.pages字典，放進self.container，傳入 app object 讓每個 page 都可以 access user_id, clicked_group_id, clicked_expense_id
        self.pages['SignIn'] = SignIn(self.container, self.show_page, self)
        self.pages['HomePage'] = HomePage(self.container, self.show_page, self)
        self.pages['AddGroup'] = AddGroup(self.container, self.show_page, self)
        self.pages['JoinGroup'] = JoinGroup(self.container, self.show_page, self)
        self.pages['ViewGroup'] = ViewGroup(self.container, self.show_page, self)
        self.pages['AddExpense'] = AddExpense(self.container, self.show_page, self)
        self.pages['EditExpense'] = EditExpense(self.container, self.show_page, self)
        self.pages['ViewMembers'] = ViewMembers(self.container, self.show_page, self)
        self.pages['SettleUp'] = SettleUp(self.container, self.show_page, self)

        # 建立再隱藏所有頁面
        for page in self.pages.values():
            page.grid(row=0, column=0, sticky='nsew')
            page.grid_remove()

    def show_page(self, page_name):

        # 隱藏所有頁面
        for page in self.pages.values():
            page.grid_remove()

        if page_name in self.pages:
            page = self.pages[page_name]

            # HomePage attribute: load_groups
            if page_name == 'HomePage' and hasattr(page, 'load_groups'):
                page.load_groups()

            # ViewGroup attribute: load_group_expenses
            if page_name == 'ViewGroup' and hasattr(page, 'load_group_expenses'):
                page.load_group_expenses()

            # EditExpense attribute: load_expense
            if page_name == 'EditExpense' and hasattr(page, 'load_expense'):
                page.load_expense()

            # ViewMembers attribute: load_members
            if page_name == 'ViewMembers' and hasattr(page, 'load_members'):
                page.load_members()
            
            # SettleUp attribute: load_balance
            if page_name == 'SettleUp' and hasattr(page, 'load_balance'):
                page.load_balance()

            # SettleUp attribute: load_settle
            if page_name == 'SettleUp' and hasattr(page, 'load_settle'):
                page.load_settle()


            # 清空重置
            if hasattr(page, 'reset_fields'):
                page.reset_fields()

            page.grid()
        
        else:
            print(f'頁面 {page_name} 不存在')


if __name__ == '__main__':
    app = App()
    app.mainloop()
