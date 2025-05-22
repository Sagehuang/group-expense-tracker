import customtkinter as ctk
from datetime import datetime


ctk.set_appearance_mode('System')
ctk.set_default_color_theme('blue')

# 【假資料】
group_name = '這是一個名字非常非常長的群組'
# # 要讓ViewGroup頁面上能出現組內所有expense的資訊，會需要跨頁面傳遞group_id, list of expense_id（群組ID、該ID有哪些expense）


class ViewGroup(ctk.CTkFrame):
    def __init__(self, master, show_page_callback, controller):
        super().__init__(master)
        self.show_page = show_page_callback
        self.controller = controller

        # self.group_name_display = group_name[:8] + '...' if len(group_name) > 10 else group_name # self
        self.group_name_display = group_name

        # 整體排版
        self.grid_rowconfigure(1, weight=1)  # 可捲動區
        self.grid_columnconfigure(0, weight=1)

        font_top_bar = ctk.CTkFont(family='Gotham', size=20, weight='bold')
        mid_font = ctk.CTkFont(family='Gotham', size=16)
        small_font = ctk.CTkFont(family='Gotham', size=12)

        # 頂端列
        top_bar = ctk.CTkFrame(self, fg_color='#F3F6F4')
        top_bar.grid(row=0, column=0, sticky='ew')
        top_bar.grid_columnconfigure(1, weight=1)

        self.home_button = ctk.CTkButton(top_bar, text='Home', font=small_font, command=self.on_navigate_home, width=80)
        self.title_label = ctk.CTkLabel(top_bar, text=self.group_name_display, text_color='black', font=font_top_bar)
        self.logout_button = ctk.CTkButton(top_bar, text='Logout', font=small_font, command=self.on_logout, width=80)

        self.logout_button.grid(row=0, column=2, padx=10, pady=10, sticky='e')
        self.home_button.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.title_label.grid(row=0, column=1, padx=10, pady=10)

        scrollable = ctk.CTkScrollableFrame(self)
        scrollable.grid(row=1, column=0, sticky='nsew', padx=10)

        self.expenses = obtain_expense(self.controller.clicked_group_id)  # !!!
        # 群組內項目假資料
        '''
        self.expenses = [
            {
                'name': 'Dinner',
                'amount': 200,
                'note': 'Sushi',
                'created_at': datetime.datetime.strptime('2025-05-13 18:30:00', '%Y-%m-%d %H:%M:%S'),
                'payer': 'Bob',  # user_name
                'participants': [1, 2],
                'expense_id': 1  # expense id
            },
            {
                'name': 'Really long name',
                'amount': 1000,
                'note': None,
                'created_at': datetime.datetime.strptime('2025-05-14 19:00:00', '%Y-%m-%d %H:%M:%S'),
                'payer': 'Alice',  # user_name
                'participants': [1, 2],
                'expense_id': 2  # expense id
            },
            {
                'name': 'Appliances',
                'amount': 5000,
                'note': None,
                'created_at': datetime.datetime.strptime('2025-05-16 12:00:00', '%Y-%m-%d %H:%M:%S'),
                'payer': 'Alice',  # user_name
                'participants': [1, 2],
                'expense_id': 3  # expense id
            },
        ]
        '''

        if self.expenses:
            for exp in self.expenses:
                expense_frame = ctk.CTkFrame(scrollable, fg_color='transparent')
                expense_frame.pack(padx=10, pady=15, fill='x')
                expense_frame.grid_columnconfigure((0, 1), weight=1)
                expense_frame.grid_columnconfigure(2, weight=0)
                expense_frame.grid_rowconfigure((0, 1), weight=1)

                # item_name = exp['name'][:8] + '...' if len(exp['name']) > 10 else exp['name']
                item_name = exp['name']
                item_payer = exp['payer']
                item_amount = exp['amount']

                item_name_label = ctk.CTkLabel(expense_frame, text=item_name, font=mid_font)
                item_payer_label = ctk.CTkLabel(expense_frame, text=f'Paid by {item_payer}', font=small_font)
                item_amount_label = ctk.CTkLabel(expense_frame, text=f'NT$ {item_amount}', font=mid_font)
                edit_button_button = ctk.CTkButton(expense_frame, text='Edit', text_color='#FFFFFF', font=small_font,
                                                   width=60, border_width=1, border_color='#B0B0B0',
                                                   fg_color='#B0B0B0',
                                                   command=lambda e=exp: self.on_edit(e))

                item_name_label.grid(row=0, column=0, sticky='w')
                item_payer_label.grid(row=1, column=0, sticky='w')
                item_amount_label.grid(row=0, column=1, rowspan=2, padx=10, sticky='e')
                edit_button_button.grid(row=0, column=2, rowspan=2, sticky='e')

                # 底線
                line_frame = ctk.CTkFrame(scrollable, height=1, fg_color='black')
                line_frame.pack(fill='x', padx=10, pady=(0, 10))

        else:
            no_group_label = ctk.CTkLabel(scrollable, text='Add an expense!', font=small_font)
            no_group_label.pack(pady=20)

        # 底部按鈕
        bottom_frame = ctk.CTkFrame(self, fg_color='transparent')
        bottom_frame.grid(row=2, column=0, sticky='ew', padx=10, pady=10)

        bottom_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.members_button = ctk.CTkButton(bottom_frame, text='Members', font=small_font, command=self.on_members)
        self.plus_button = ctk.CTkButton(bottom_frame, text='+', font=small_font, command=self.on_plus)
        self.settle_up_button = ctk.CTkButton(bottom_frame, text='Settle Up', font=small_font, command=self.on_settle_up)

        self.members_button.grid(row=0, column=0, padx=10, sticky='ew')
        self.plus_button.grid(row=0, column=1, padx=10, sticky='ew')
        self.settle_up_button.grid(row=0, column=2, padx=10, sticky='ew')

    # 頁面切換
    def on_navigate_home(self):
        self.show_page('HomePage')

    def on_logout(self):
        self.show_page('SignIn')

    def on_members(self):
        self.show_page('ViewMembers')

    def on_plus(self):
        self.show_page('AddExpense')

    def on_settle_up(self):
        self.show_page('SettleUp')

    def on_edit(self, expense):
        self.controller.clicked_expense_id = expense['expense_id']
        self.show_page('EditExpense')


if __name__ == '__main__':
    app = ctk.CTk()
    app.geometry('400x640')
    app.title('Group Expense Tracker')

    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(0, weight=1)

    view_group = ViewGroup(app, show_page_callback)
    view_group.grid(row=0, column=0, sticky='nsew')

    app.mainloop()
