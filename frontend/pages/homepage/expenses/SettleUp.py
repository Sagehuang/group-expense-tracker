import customtkinter as ctk
from api_client import get_balance_info, get_settle_info

ctk.set_appearance_mode('System')
ctk.set_default_color_theme('blue')


class SettleUp(ctk.CTkFrame):
    def __init__(self, master, show_page_callback, controller):
        super().__init__(master)
        self.show_page = show_page_callback
        self.controller = controller

        # 整體排版
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.font_top_bar = ctk.CTkFont(family='Gotham', size=20, weight='bold')
        self.mid_font = ctk.CTkFont(family='Gotham', size=16)
        self.small_font = ctk.CTkFont(family='Gotham', size=12)

        # 頂端列
        top_bar = ctk.CTkFrame(self, fg_color='#F3F6F4')
        top_bar.grid(row=0, column=0, sticky='ew')
        top_bar.grid_columnconfigure(1, weight=1)

        self.back_button = ctk.CTkButton(top_bar, text='Back', font=self.small_font, command=self.on_navigate_back, width=80)
        self.title_label = ctk.CTkLabel(top_bar, text='Settle Up', text_color='black', font=self.font_top_bar)
        self.logout_button = ctk.CTkButton(top_bar, text='Logout', font=self.small_font, command=self.on_logout, width=80)

        self.back_button.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.title_label.grid(row=0, column=1, padx=10, pady=10)
        self.logout_button.grid(row=0, column=2, padx=10, pady=10, sticky='e')

        # 可捲動區
        self.scrollable = ctk.CTkScrollableFrame(self)
        self.scrollable.grid(row=1, column=0, sticky='nsew', padx=10)

    def load_balance(self):
        for widget in self.scrollable.winfo_children():
            widget.destroy()

        # 呼叫API function
        try:
            group_balance = get_balance_info(self.controller.clicked_group_id)
            print('get_balance_info API 回傳:', group_balance)
        except Exception as error:
            print('get_balance_info API 發生錯誤:', error)

        # 模擬群組內有成員
        if group_balance:
            balance_frame = ctk.CTkFrame(self.scrollable, fg_color='transparent')
            balance_frame.pack(padx=10, pady=10, fill='x')
            balance_frame.grid_columnconfigure(0, weight=1)

            # 遍歷 group_balance
            for index, balance_dict in enumerate(group_balance):
                # 組員
                member_balance_label = ctk.CTkLabel(balance_frame, text=balance_dict['user_name'], font=self.mid_font)
                member_balance_label.grid(row=index * 2, column=0, padx=20, sticky='w')  # double space

                # 金額
                amount_balance = balance_dict['net_balance']
                if amount_balance >= 0:
                    amount_balance_label = ctk.CTkLabel(balance_frame, text='+ NT$' + str(amount_balance), font=self.mid_font)
                else:
                    amount_balance_label = ctk.CTkLabel(balance_frame, text='- NT$' + str(abs(amount_balance)), font=self.mid_font)
                amount_balance_label.grid(row=index * 2, column=1, padx=20, sticky='e')

                # 加一條黑色橫線
                line_frame = ctk.CTkFrame(balance_frame, height=1, fg_color='black')
                line_frame.grid(row=1 + index * 2, column=0, columnspan=2, padx=20, sticky='ew')  # double space

        else:
            no_members_label = ctk.CTkLabel(self.scrollable, text='There are no members in this group.', font=self.small_font)
            no_members_label.pack(pady=20)

        # 雙線分隔（frame）
        separator1 = ctk.CTkFrame(self.scrollable, height=1, fg_color='black')
        separator1.pack(fill='x', pady=(25, 2))  # 25, 2

        separator2 = ctk.CTkFrame(self.scrollable, height=1, fg_color='black')
        separator2.pack(fill='x', pady=(0, 0))  # 0, 10

    def load_settle(self):
        # 這裡不能清空元件！在 load_balance 清空一次即可
        # for widget in self.scrollable.winfo_children():
        #     widget.destroy()  # 清空原有元件

        # 呼叫API function
        try:
            group_settlement = get_settle_info(self.controller.clicked_group_id)
            print('get_settle_info API 回傳:', group_settlement)
        except Exception as error:
            print('get_settle_info API 發生錯誤:', error)

        # 模擬群組內有成員
        if group_settlement:
            settle_frame = ctk.CTkFrame(self.scrollable, fg_color='transparent')
            settle_frame.pack(padx=10, pady=5, fill='x')
            settle_frame.grid_columnconfigure(0, weight=1)

            # 遍歷 group_settlement
            for index, settle_dict in enumerate(group_settlement):

                # 組員
                member_settle_label = ctk.CTkLabel(settle_frame, text=f"{settle_dict['payer']}   ⥤   {settle_dict['receiver']}", font=self.mid_font)
                member_settle_label.grid(row=index * 2, column=0, padx=20, sticky='w')  # double space

                # 金額
                amount_settle = settle_dict['amount']
                amount_settle_label = ctk.CTkLabel(settle_frame, text='NT$' + str(amount_settle), font=self.mid_font)
                amount_settle_label.grid(row=index * 2, column=1, padx=20, sticky='e')

                # 加一條黑色橫線
                line_frame = ctk.CTkFrame(settle_frame, height=1, fg_color='black')
                line_frame.grid(row=1 + index * 2, column=0, columnspan=2, padx=20, sticky='ew')  # double space

    # 頁面切換
    def on_navigate_back(self):
        self.show_page('ViewGroup')

    def on_logout(self):
        self.show_page('SignIn')
