import customtkinter as ctk


ctk.set_appearance_mode('System')
ctk.set_default_color_theme('blue')



# 先設定假資料（上半部balance_frame）
# nested dictionary 
balance_database = {'000012': {'Alice': -250, 'Bob': 250},
                 '000013': {'Charlie': 300, 'Daisy': -300}}
        
def get_balance_info(group_id):
    balance_data = balance_database.get(group_id)
    if balance_data:
        members_balance_list = list(balance_data.keys())
        amount_balance_list = list(balance_data.values())
        return members_balance_list, amount_balance_list


# 先設定假資料（下半部settle_frame）
# nested dictionary 
settle_database = {'000012': {('Alice', 'Bob'): 250, ('Anna', 'Brian'): 500},
                   '000013': {('Charlie', 'Daisy'): 750, ('Calvin', 'Dora'): 1000}}

def get_settle_info(group_id):
    settle_data = settle_database.get(group_id)
    if settle_data:
        members_settle_list = list(settle_data.keys())
        amount_settle_list = list(settle_data.values())
        return members_settle_list, amount_settle_list




class SettleUp(ctk.CTkFrame):
    def __init__(self, master, group_id):
        super().__init__(master)

        members_balance_list, amount_balance_list = get_balance_info(group_id)
        members_settle_list, amount_settle_list = get_settle_info(group_id)


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
        if members_balance_list and amount_balance_list:
            balance_frame = ctk.CTkFrame(scrollable, fg_color='transparent')
            balance_frame.pack(padx=10, pady=10, fill='x')
            balance_frame.grid_columnconfigure(0, weight=1)

            # 遍歷members_balance_list
            for index, member_balance in enumerate(members_balance_list): 
                amount_balance = amount_balance_list[index]
                member_balance_label = ctk.CTkLabel(balance_frame, text=member_balance, font=mid_font)
                member_balance_label.grid(row= index * 2, column=0, padx=20, sticky='w') # double space
                
                # 金額
                if amount_balance >= 0:
                    amount_balance_label = ctk.CTkLabel(balance_frame, text='+ NT$' + str(amount_balance), font=mid_font)
                else:
                    amount_balance_label = ctk.CTkLabel(balance_frame, text='- NT$' + str(abs(amount_balance)), font=mid_font)
                amount_balance_label.grid(row= index * 2, column=1, padx=20, sticky='e')

                # 加一條黑色橫線
                line_frame = ctk.CTkFrame(balance_frame, height=1, fg_color='black')
                line_frame.grid(row=1 + index * 2, column=0, columnspan=2, padx=20, sticky='ew') # double space

        else:
            no_members_label = ctk.CTkLabel(scrollable, text='There are no members in this group.', font=small_font)
            no_members_label.pack(pady=20)


        # 雙線分隔（frame）
        separator1 = ctk.CTkFrame(scrollable, height=1, fg_color='black')
        separator1.pack(fill='x', pady=(25, 2)) # 25, 2

        separator2 = ctk.CTkFrame(scrollable, height=1, fg_color='black')
        separator2.pack(fill='x', pady=(0, 0)) # 0, 10



        # 模擬群組內有成員
        if members_settle_list and amount_settle_list:
            settle_frame = ctk.CTkFrame(scrollable, fg_color='transparent')
            settle_frame.pack(padx=10, pady=5, fill='x')
            settle_frame.grid_columnconfigure(0, weight=1)

            # 遍歷members_settle_list
            for index, member_settle in enumerate(members_settle_list): 
                # members_settle_list = [('Alice', 'Bob'), ('Anna', 'Brian')]
                # at index=0, member_settle = ('Alice', 'Bob')
                # at index=1, member_settle = ('Anna', 'Brian')

                debtor = member_settle[0]
                creditor = member_settle[1]
                amount_settle = amount_settle_list[index]

                member_settle_label = ctk.CTkLabel(settle_frame, text= f'{debtor}   ⥤   {creditor}', font=mid_font) # 箭頭很醜，之後再弄好看一點
                member_settle_label.grid(row= index * 2, column=0, padx=20, sticky='w') # double space
                
                # 金額
                amount_settle_label = ctk.CTkLabel(settle_frame, text='NT$' + str(amount_settle), font=mid_font)
                amount_settle_label.grid(row= index * 2, column=1, padx=20, sticky='e')

                # 加一條黑色橫線
                line_frame = ctk.CTkFrame(settle_frame, height=1, fg_color='black')
                line_frame.grid(row=1 + index * 2, column=0, columnspan=2, padx=20, sticky='ew') # double space



# 轉換頁面

    def on_navigate_back(self):
        return

    def on_logout(self):
        return



if __name__ == '__main__':
    app = ctk.CTk()
    app.geometry('400x640')
    app.title('Group Expense Tracker')

    settle_up = SettleUp(app, '000012')
    settle_up.pack(fill='both', expand=True)

    app.mainloop()
