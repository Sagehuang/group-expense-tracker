import customtkinter as ctk


ctk.set_appearance_mode('System')
ctk.set_default_color_theme('blue')


# 先自行設定假資料
class Expense:
    def __init__(self, name, amount, payer):
        self.name = name
        self.amount = amount
        self.payer = payer


class User:
    def __init__(self, name):
        self.name = name

# =====


class ViewGroup(ctk.CTkFrame):
    def __init__(self, master, username, group_name):
        super().__init__(master)
        self.username = username
        self.group_name = group_name

        self.group_name_display = group_name[:8] + '...' if len(self.group_name) > 10 else self.group_name

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

        # 模擬群組內是否有項目
        self.expenses = [Expense('晚餐晚餐晚餐晚餐晚餐晚餐晚餐', 200, User('Bob'))]  # !!!
        # 預期 self.expenses 是從資料庫抓取，列表中為 Expense 類別。

        if self.expenses:
            for i in range(len(self.expenses)):
                expense_frame = ctk.CTkFrame(scrollable, fg_color='transparent')
                expense_frame.pack(padx=10, pady=10, fill='x')
                expense_frame.grid_columnconfigure((0, 1, 2), weight=1)
                expense_frame.grid_columnconfigure(3, weight=0)

                item_name = self.expenses[i].name[:8] + '...' if len(self.expenses[i].name) > 10 else self.expenses[i].name
                item_payer = self.expenses[i].payer.name
                item_amount = self.expenses[i].amount

                item_name_label = ctk.CTkLabel(expense_frame, text=item_name, font=mid_font)
                item_payer_label = ctk.CTkLabel(expense_frame, text=item_payer + ' 先付', font=small_font)
                item_amount_label = ctk.CTkLabel(expense_frame, text='NT$' + str(item_amount), font=mid_font)
                edit_button_button = ctk.CTkButton(expense_frame, text='Edit', font=small_font, width=60, command=lambda e=self.expenses[i]: self.edit_expense(e))

                item_name_label.grid(row=0, column=0, sticky='w')
                item_payer_label.grid(row=0, column=1, sticky='w')
                item_amount_label.grid(row=0, column=2, padx=5, sticky='e')
                edit_button_button.grid(row=0, column=3, sticky='e')
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


# 轉換頁面


    def on_navigate_home(self):
        return

    def on_logout(self):
        return

    def on_members(self):
        return

    def on_plus(self):
        return

    def on_settle_up(self):
        return

    def edit_expense(self, expense):
        return


if __name__ == '__main__':
    app = ctk.CTk()
    app.geometry('400x640')
    app.title('Group Expense Tracker')

    view_group = ViewGroup(app, 'Alice', '這是一個名字非常非常長的群組')
    view_group.pack(fill='both', expand=True)

    app.mainloop()
