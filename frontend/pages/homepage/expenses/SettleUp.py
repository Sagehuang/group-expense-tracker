import customtkinter as ctk
from api_client import get_balance_info
from api_client import get_settle_info


ctk.set_appearance_mode('System')
ctk.set_default_color_theme('blue')


# 【假資料】
# group_id = 1
# group_balance = [{'user_name': 'Alice', 'net_balance': -500}, {'user_name': 'Bob', 'net_balance': 250}, {'user_name': 'Brian', 'net_balance': 250}]
# group_settlement = [{'payer': 'Alice', 'receiver': 'Bob', 'amount': 250}, {'payer': 'Alice', 'receiver': 'Brian', 'amount': 250}]
## 要讓SettleUp頁面上能出現組員之間的balance、settle，會需要跨頁面傳遞group_id


class SettleUp(ctk.CTkFrame):
    def __init__(self, master, show_page_callback, controller):
        super().__init__(master)
        self.show_page = show_page_callback
        self.controller = controller

        group_balance = get_balance_info(self.controller.clicked_group_id)
        group_settlement = get_settle_info(self.controller.clicked_group_id)

        # 整體排版
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        font_top_bar = ctk.CTkFont(family='Gotham', size=20, weight='bold')
        mid_font = ctk.CTkFont(family='Gotham', size=16)
        small_font = ctk.CTkFont(family='Gotham', size=12)

        # 頂端列
        top_bar = ctk.CTkFrame(self, fg_color='#F3F6F4')
        top_bar.grid(row=0, column=0, sticky='ew')
        top_bar.grid_columnconfigure(1, weight=1)

        self.back_button = ctk.CTkButton(top_bar, text='Back', font=small_font, command=self.on_navigate_back, width=80)
        self.title_label = ctk.CTkLabel(top_bar, text='Settle Up', text_color='black', font=font_top_bar)
        self.logout_button = ctk.CTkButton(top_bar, text='Logout', font=small_font, command=self.on_logout, width=80)

        self.back_button.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.title_label.grid(row=0, column=1, padx=10, pady=10)
        self.logout_button.grid(row=0, column=2, padx=10, pady=10, sticky='e')

        # 可捲動區
        scrollable = ctk.CTkScrollableFrame(self)
        scrollable.grid(row=1, column=0, sticky='nsew', padx=10)

        # 模擬群組內有成員
        if group_balance:
            balance_frame = ctk.CTkFrame(scrollable, fg_color='transparent')
            balance_frame.pack(padx=10, pady=10, fill='x')
            balance_frame.grid_columnconfigure(0, weight=1)

            # 遍歷group_balance
            for index, balance_dict in enumerate(group_balance):
                # 組員
                member_balance_label = ctk.CTkLabel(balance_frame, text=balance_dict['user_name'], font=mid_font)
                member_balance_label.grid(row=index * 2, column=0, padx=20, sticky='w')  # double space

                # 金額
                amount_balance = balance_dict['net_balance']
                if amount_balance >= 0:
                    amount_balance_label = ctk.CTkLabel(balance_frame, text='+ NT$' + str(amount_balance), font=mid_font)
                else:
                    amount_balance_label = ctk.CTkLabel(balance_frame, text='- NT$' + str(abs(amount_balance)), font=mid_font)
                amount_balance_label.grid(row=index * 2, column=1, padx=20, sticky='e')

                # 加一條黑色橫線
                line_frame = ctk.CTkFrame(balance_frame, height=1, fg_color='black')
                line_frame.grid(row=1 + index * 2, column=0, columnspan=2, padx=20, sticky='ew')  # double space

        else:
            no_members_label = ctk.CTkLabel(scrollable, text='There are no members in this group.', font=small_font)
            no_members_label.pack(pady=20)

        # 雙線分隔（frame）
        separator1 = ctk.CTkFrame(scrollable, height=1, fg_color='black')
        separator1.pack(fill='x', pady=(25, 2))  # 25, 2

        separator2 = ctk.CTkFrame(scrollable, height=1, fg_color='black')
        separator2.pack(fill='x', pady=(0, 0))  # 0, 10

        # 模擬群組內有成員
        if group_settlement:
            settle_frame = ctk.CTkFrame(scrollable, fg_color='transparent')
            settle_frame.pack(padx=10, pady=5, fill='x')
            settle_frame.grid_columnconfigure(0, weight=1)

            # 遍歷group_settlement
            for index, settle_dict in enumerate(group_settlement):

                # 組員
                member_settle_label = ctk.CTkLabel(settle_frame, text=f"{settle_dict['payer']}   ⥤   {settle_dict['receiver']}", font=mid_font)
                member_settle_label.grid(row=index * 2, column=0, padx=20, sticky='w')  # double space

                # 金額
                amount_settle = settle_dict['amount']
                amount_settle_label = ctk.CTkLabel(settle_frame, text='NT$' + str(amount_settle), font=mid_font)
                amount_settle_label.grid(row=index * 2, column=1, padx=20, sticky='e')

                # 加一條黑色橫線
                line_frame = ctk.CTkFrame(settle_frame, height=1, fg_color='black')
                line_frame.grid(row=1 + index * 2, column=0, columnspan=2, padx=20, sticky='ew')  # double space

    # 頁面切換
    def on_navigate_back(self):
        self.show_page('ViewGroup')

    def on_logout(self):
        self.show_page('SignIn')


if __name__ == '__main__':
    app = ctk.CTk()
    app.geometry('400x640')
    app.title('Group Expense Tracker')

    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(0, weight=1)

    settle_up = SettleUp(app, show_page_callback)
    settle_up.grid(row=0, column=0, sticky='nsew')

    app.mainloop()
