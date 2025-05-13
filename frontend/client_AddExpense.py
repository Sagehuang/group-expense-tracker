import customtkinter as ctk
from datetime import datetime


ctk.set_appearance_mode('System')
ctk.set_default_color_theme('blue')


class AddExpense(ctk.CTkFrame):
    def __init__(self, master, group_name):
        super().__init__(master)
        self.group_name = group_name



        # 1st frame: top bar
        top_bar = ctk.CTkFrame(self, fg_color='#0066CC')
        top_bar.grid(row=0, column=0, sticky='ew')
        top_bar.grid_columnconfigure(1, weight=1)

        self.back_button = ctk.CTkButton(top_bar, text='Back',
                                         command=self.on_navigate_back,
                                         width=80)
        self.title_label = ctk.CTkLabel(top_bar, text='Add Expense',
                                        font=ctk.CTkFont(size=18,
                                                         weight='bold'))
        self.logout_button = ctk.CTkButton(top_bar, text='Logout',
                                           command=self.on_logout, width=80)

        self.back_button.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.title_label.grid(row=0, column=1, padx=10, pady=10)
        self.logout_button.grid(row=0, column=2, padx=10, pady=10, sticky='e')



        # 2rd frame（主要容器）: Item, Amount, Payer, Participants, Note, Add
        bottom_frame = ctk.CTkFrame(self, fg_color='transparent')
        bottom_frame.grid(row=1, column=0, pady=20, sticky='n')
        bottom_frame.grid_columnconfigure((0, 1), weight=1)
        bottom_frame.grid_rowconfigure((1, 2, 3, 4, 5, 6, 7), weight=1)

        # 3rd frame（2nd frame的子容器）: Date, Time
        top_date_time_frame = ctk.CTkFrame(bottom_frame)
        top_date_time_frame.grid(row=0, column=0, columnspan=2, pady=5, sticky="w")

        now = datetime.now()
        date_str = now.strftime("%Y/%m/%d")  # Y：完整年份
        time_str = now.strftime("%H:%M")

        self.date_label = ctk.CTkLabel(top_date_time_frame, text=f"Date: {date_str}")
        self.date_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        self.time_label = ctk.CTkLabel(top_date_time_frame, text=f"Time: {time_str}")
        self.time_label.grid(row=0, column=1, padx=10, pady=5, sticky='e')


        # 1st row：Item
        self.item_label = ctk.CTkLabel(bottom_frame, text='Item', anchor='w')
        self.item_label.grid(row=1, column=0, padx=(10, 5), pady=10, sticky='w')

        self.item_entry = ctk.CTkEntry(bottom_frame)
        self.item_entry.grid(row=1, column=1, padx=(5, 10), pady=10, sticky='ew')


        # 2nd row：Amount
        self.amount_label = ctk.CTkLabel(bottom_frame, text='Amount', anchor='w')
        self.amount_label.grid(row=2, column=0, padx=(10, 5), pady=10, sticky='w')

        self.amount_entry = ctk.CTkEntry(bottom_frame)
        self.amount_entry.grid(row=2, column=1, padx=(5, 10), pady=10, sticky='ew')


        # 3rd row：Payer
        self.payer_label = ctk.CTkLabel(bottom_frame, text='Payer', anchor='w')
        self.payer_label.grid(row=3, column=0, padx=(10, 5), pady=10, sticky='w')

        self.payer_entry = ctk.CTkEntry(bottom_frame)
        self.payer_entry.grid(row=3, column=1, padx=(5, 10), pady=10, sticky='ew')


        # 4th row：Participants
        self.participants_label = ctk.CTkLabel(bottom_frame, text='Participants', anchor='w')
        self.participants_label.grid(row=4, column=0, padx=(10, 5), pady=10, sticky='w')

        self.participants_entry = ctk.CTkEntry(bottom_frame)
        self.participants_entry.grid(row=4, column=1, padx=(5, 10), pady=10, sticky='ew')


        # 5th row：Notes
        self.notes_label = ctk.CTkLabel(bottom_frame, text='Notes', anchor='w')
        self.notes_label.grid(row=5, column=0, padx=(10, 5), pady=10, sticky='w')

        self.notes_entry = ctk.CTkEntry(bottom_frame)
        self.notes_entry.grid(row=5, column=1, padx=(5, 10), pady=10, sticky='ew')


        # 6th row：Add
        self.add_group_button = ctk.CTkButton(bottom_frame, text='Add', command=self.on_add)
        self.add_group_button.grid(row=6, column=0, columnspan=2, pady=20)

        # 7th row (potential): 
        self.result_label = ctk.CTkLabel(bottom_frame, text='', text_color='red')
        self.result_label.grid(row=7, column=0, columnspan=2, pady=(5, 0))



# 轉換頁面

    def on_navigate_back():
        return

    def on_logout():
        return



# ADD EXPENSE
    def on_add(self):
        item = self.item_entry.get().strip()
        amount_str = self.amount_entry.get().strip()
        payer = self.payer_entry.get().strip()
        participants = self.participants_entry.get().strip()

        if not item or not amount_str or not payer or not participants:
            self.result_label.configure(text='Please fill in all fields.')
            return

        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError("Amount must be positive.")
        except ValueError:
            self.result_label.configure(text='Amount must be a valid positive number.')
            return

        # # 回傳這筆added expense給後端

        # expense_data = {
        # 'item': item,
        # 'amount': amount,
        # 'payer': payer,
        # 'note': note,
        # 'date': datetime.now().strftime('%Y-%m-%d'),
        # 'time': datetime.now().strftime('%H:%M'),
        # 'group': self.username  # 假設 self.username 是 group 名
        # }

        # success = send_expense_to_backend(expense_data)  # 回傳expense給後端的function

        # if success:
        #     self.result_label.configure(text='Expense added successfully.')
            
        #     # 清空輸入欄
        #     self.item_entry.delete(0, 'end')
        #     self.amount_entry.delete(0, 'end')
        #     self.payer_entry.delete(0, 'end')
        #     self.note_entry.delete(0, 'end')
        # else:
        #     self.result_label.configure(text='Failed to add expense.')


if __name__ == '__main__':
    app = ctk.CTk()
    app.geometry('400x640')
    app.title('Group Expense Tracker')

    add_expense = AddExpense(app, "Group A")
    add_expense.pack(expand=True)

    app.mainloop()
