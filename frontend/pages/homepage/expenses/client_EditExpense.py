import customtkinter as ctk
from datetime import datetime
# from api_client import edit_expense as api_edit_expense
# from api_client import get_expense_info



ctk.set_appearance_mode('System')
ctk.set_default_color_theme('blue')

original_item = 'Food'
original_amount = 300
original_payer = 'Alice'
original_participants = 'Bob, Brian'
orginial_note = 'McDonald\'s'



class EditExpense(ctk.CTkFrame):
    def __init__(self, master, group_name):
        super().__init__(master)
        self.group_name = group_name # 存入Group Name



        # 1st frame: top bar
        top_bar = ctk.CTkFrame(self, fg_color='#0066CC')
        top_bar.grid(row=0, column=0, sticky='ew')
        top_bar.grid_columnconfigure(1, weight=1)

        self.back_button = ctk.CTkButton(top_bar, text='Back',
                                         command=self.on_navigate_back,
                                         width=80)
        self.title_label = ctk.CTkLabel(top_bar, text='Edit Expense',
                                        font=ctk.CTkFont(size=18,
                                                         weight='bold'))
        self.logout_button = ctk.CTkButton(top_bar, text='Logout',
                                           command=self.on_logout, width=80)

        self.back_button.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.title_label.grid(row=0, column=1, padx=10, pady=10)
        self.logout_button.grid(row=0, column=2, padx=10, pady=10, sticky='e')



        # 2rd frame（主要容器）: Item, Amount, Payer, Participants, Note, Edit button
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
        self.item_entry.insert(0, original_item)


        # 2nd row：Amount
        # self.amount_label = ctk.CTkLabel(bottom_frame, text='Amount', anchor='w')
        # self.amount_label.grid(row=2, column=0, padx=(10, 5), pady=10, sticky='w')

        # self.amount_prefix_label = ctk.CTkLabel(bottom_frame, text='NT$', anchor='w')
        # self.amount_prefix_label.grid(row=2, column=1, padx=(10, 0), pady=10, sticky='w')

        # self.amount_entry = ctk.CTkEntry(bottom_frame)
        # self.amount_entry.grid(row=2, column=2, padx=(0, 10), pady=10, sticky='w')
        # self.amount_entry.insert(0, original_amount)


        # 2nd row：Amount
        self.amount_label = ctk.CTkLabel(bottom_frame, text='Amount', anchor='w')
        self.amount_label.grid(row=2, column=0, padx=(10, 5), pady=10, sticky='w')

        # 建立一個小框來放 NT$ + Entry
        amount_frame = ctk.CTkFrame(bottom_frame, fg_color='transparent')  # 不要背景色
        amount_frame.grid(row=2, column=1, columnspan=2, padx=(5, 10), pady=10, sticky='w')  # columnspan=2 合併兩欄

        self.amount_prefix_label = ctk.CTkLabel(amount_frame, text='NT$', anchor='w')
        self.amount_prefix_label.pack(side='left', padx=(0, 2))  # 和 entry 靠得很近

        self.amount_entry = ctk.CTkEntry(amount_frame, width=120)
        self.amount_entry.pack(side='left')
        self.amount_entry.insert(0, original_amount)


        # 3rd row：Payer
        self.payer_label = ctk.CTkLabel(bottom_frame, text='Payer', anchor='w')
        self.payer_label.grid(row=3, column=0, padx=(10, 5), pady=10, sticky='w')

        self.payer_entry = ctk.CTkEntry(bottom_frame)
        self.payer_entry.grid(row=3, column=1, padx=(5, 10), pady=10, sticky='ew')
        self.payer_entry.insert(0, original_payer)


        # 4th row：Participants
        self.participants_label = ctk.CTkLabel(bottom_frame, text='Participants', anchor='w')
        self.participants_label.grid(row=4, column=0, padx=(10, 5), pady=10, sticky='w')

        self.participants_entry = ctk.CTkEntry(bottom_frame)
        self.participants_entry.grid(row=4, column=1, padx=(5, 10), pady=10, sticky='ew')
        self.participants_entry.insert(0, original_participants)


        # 5th row：Note
        self.note_label = ctk.CTkLabel(bottom_frame, text='Note', anchor='w')
        self.note_label.grid(row=5, column=0, padx=(10, 5), pady=10, sticky='w')

        self.note_entry = ctk.CTkEntry(bottom_frame)
        self.note_entry.grid(row=5, column=1, padx=(5, 10), pady=10, sticky='ew')
        self.note_entry.insert(0, orginial_note)


        # 6th row：Edit
        self.edit_group_button = ctk.CTkButton(bottom_frame, text='Edit', command=self.on_edit)
        self.edit_group_button.grid(row=6, column=0, columnspan=2, pady=20)


        # 7th row: result
        self.result_label = ctk.CTkLabel(bottom_frame, text='', text_color='red')
        self.result_label.grid(row=7, column=0, columnspan=2, pady=(5, 0))



# 轉換頁面

    def on_navigate_back(self):
        # self.master.show_page('HomePage')
        return

    def on_logout(self):
        # self.master.show_page('SignIn')
        return



# ADD EXPENSE
    def on_edit(self):
        item = self.item_entry.get().strip()

        amount_str = self.amount_entry.get().strip().replace(',', '')
        if not amount_str.isdigit():
            self.result_label.configure(text='Amount must contain numbers.')
            return 
        amount = int(amount_str)
        if amount <= 0:
            self.result_label.configure(text='Amount must be a valid positive number.')
            return

        payer = self.payer_entry.get().strip()

        participants_raw = self.participants_entry.get().strip()
        participants_list = []
        for participant in participants_raw.split(','):
            stripped_participant = participant.strip()
            if stripped_participant:
                participants_list.append(stripped_participant)

        note = self.note_entry.get().strip()


        if not item or not amount_str or not payer or not participants_list:
            self.result_label.configure(text='Please fill in all fields.', text_color='red')
            return

        

        # 資料集合成一個dictionary，回傳給後端
        expense_data = {
            'Date': datetime.now().strftime('%Y/%m/%d'),
            'Time': datetime.now().strftime('%H:%M'),
            'Item': item,
            'Amount': amount,
            'Payer': payer,
            'Participants': participants_list,
            'Note': note,
            'Group Name': self.group_name  # 這筆資料存入這個Group
        }

        # 呼叫API function
        # success = api_edit_expense(expense_data)

        # if success:
        #     self.result_label.configure(text='Expense edited successfully.', text_color='green')
        #     self.after(2000, self.on_navigate_back) # 延遲2秒後，跳轉回Homepage 

        # else:
        #     self.result_label.configure(text='Failed to edit expense.', text_color='red')


if __name__ == '__main__':
    app = ctk.CTk()
    app.geometry('400x640')
    app.title('Group Expense Tracker')

    # group_name = get_group_name()

    edit_expense = EditExpense(app, 'Group A') # 自訂假資料
    # edit_expense = EditExpense(app, group_name)

    edit_expense.pack(expand=True)

    app.mainloop()
