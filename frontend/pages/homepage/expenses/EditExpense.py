import customtkinter as ctk
from datetime import datetime
from api_client import get_expense_info, edit_expense

ctk.set_appearance_mode('System')
ctk.set_default_color_theme('blue')


class EditExpense(ctk.CTkFrame):
    def __init__(self, master, show_page_callback, controller):
        super().__init__(master)
        self.show_page = show_page_callback
        self.controller = controller

        # 整體排版
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Pre-defined fonts
        self.font_top_bar = ctk.CTkFont(family='Gotham', size=20, weight='bold')
        self.small_font = ctk.CTkFont(family='Gotham', size=12)

        # 1st frame: top bar
        self.top_bar = ctk.CTkFrame(self, fg_color='#F3F6F4')
        self.top_bar.grid(row=0, column=0, sticky='ew')
        self.top_bar.grid_columnconfigure(1, weight=1)

        self.back_button = ctk.CTkButton(self.top_bar, text='Back', font=self.small_font, command=self.on_navigate_back, width=80)
        self.title_label = ctk.CTkLabel(self.top_bar, text='Edit Expense', text_color='black', font=self.font_top_bar)
        self.logout_button = ctk.CTkButton(self.top_bar, text='Logout', font=self.small_font, command=self.on_logout, width=80)

        self.back_button.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.title_label.grid(row=0, column=1, padx=10, pady=10)
        self.logout_button.grid(row=0, column=2, padx=10, pady=10, sticky='e')

        # 2rd frame（主要容器）: Item, Amount, Payer, Participants, Note, Edit button
        bottom_frame = ctk.CTkFrame(self, fg_color='transparent')
        bottom_frame.grid(row=1, column=0, pady=20, sticky='nsew')
        bottom_frame.grid_columnconfigure((0, 1), weight=1)
        bottom_frame.grid_rowconfigure((1, 2, 3, 4, 5, 6, 7), weight=1)

        # 3rd frame（2nd frame的子容器）: Date, Time
        top_date_time_frame = ctk.CTkFrame(bottom_frame)
        top_date_time_frame.grid(row=0, column=0, columnspan=2, pady=5, sticky='ew')

        # 設定 frame 的欄寬，使內容置中
        top_date_time_frame.grid_columnconfigure(0, weight=1)
        top_date_time_frame.grid_columnconfigure(1, weight=1)

        now = datetime.now()
        date_str = now.strftime("%Y/%m/%d")  # Y：完整年份
        time_str = now.strftime("%H:%M")

        self.date_label = ctk.CTkLabel(top_date_time_frame, text=f"Date: {date_str}", font=self.small_font)
        self.date_label.grid(row=0, column=0, padx=10, pady=5, sticky='e')  # 靠右對齊

        self.time_label = ctk.CTkLabel(top_date_time_frame, text=f"Time: {time_str}", font=self.small_font)
        self.time_label.grid(row=0, column=1, padx=10, pady=5, sticky='w')  # 靠左對齊

        # 1st row：Item
        self.item_label = ctk.CTkLabel(bottom_frame, text='Item', font=self.small_font, anchor='w')
        self.item_label.grid(row=1, column=0, padx=(10, 5), pady=10, sticky='w')

        self.item_entry = ctk.CTkEntry(bottom_frame)
        self.item_entry.grid(row=1, column=1, padx=(5, 10), pady=10, sticky='ew')

        # 2nd row：Amount
        self.amount_label = ctk.CTkLabel(bottom_frame, text='Amount', font=self.small_font, anchor='w')
        self.amount_label.grid(row=2, column=0, padx=(10, 5), pady=10, sticky='w')

        # 4th frame（放NT$ + entry）
        self.amount_frame = ctk.CTkFrame(bottom_frame, fg_color='transparent')
        self.amount_frame.grid(row=2, column=1, padx=(5, 10), pady=10, sticky='ew')
        self.amount_frame.grid_columnconfigure(1, weight=1)

        self.amount_prefix_label = ctk.CTkLabel(self.amount_frame, text='NT$', font=self.small_font, width=45, anchor='w')
        self.amount_prefix_label.grid(row=0, column=0, sticky='w')

        self.amount_entry = ctk.CTkEntry(self.amount_frame)
        self.amount_entry.grid(row=0, column=1, sticky='ew')

        # 3rd row：Payer
        self.payer_label = ctk.CTkLabel(bottom_frame, text='Payer', font=self.small_font, anchor='w')
        self.payer_label.grid(row=3, column=0, padx=(10, 5), pady=10, sticky='w')

        self.payer_entry = ctk.CTkEntry(bottom_frame)
        self.payer_entry.grid(row=3, column=1, padx=(5, 10), pady=10, sticky='ew')

        # 4th row：Participants
        self.participants_label = ctk.CTkLabel(bottom_frame, text='Participants', font=self.small_font, anchor='w')
        self.participants_label.grid(row=4, column=0, padx=(10, 5), pady=10, sticky='w')

        self.participants_entry = ctk.CTkEntry(bottom_frame)
        self.participants_entry.grid(row=4, column=1, padx=(5, 10), pady=10, sticky='ew')

        # 5th row：Note
        self.note_label = ctk.CTkLabel(bottom_frame, text='Note', font=self.small_font, anchor='w')
        self.note_label.grid(row=5, column=0, padx=(10, 5), pady=10, sticky='w')

        self.note_entry = ctk.CTkEntry(bottom_frame)
        self.note_entry.grid(row=5, column=1, padx=(5, 10), pady=10, sticky='ew')

        # 6th row：Edit button
        self.edit_group_button = ctk.CTkButton(bottom_frame, text='Edit', font=self.small_font, command=self.on_edit)
        self.edit_group_button.grid(row=6, column=0, columnspan=2, pady=20)

        # 7th row: result
        self.result_label = ctk.CTkLabel(bottom_frame, text='', font=self.small_font, text_color='red')
        self.result_label.grid(row=7, column=0, columnspan=2, pady=(5, 0))

    def load_expense(self):
        original_name, original_amount, original_note, original_created_at, original_payer, original_participants = get_expense_info(self.controller.clicked_expense_id)

        self.item_entry.delete(0, 'end')
        self.item_entry.insert(0, original_name)

        self.amount_entry.delete(0, 'end')
        self.amount_entry.insert(0, original_amount)

        self.payer_entry.delete(0, 'end')
        self.payer_entry.insert(0, original_payer)

        self.participants_entry.delete(0, 'end')
        self.participants_entry.insert(0, ', '.join(original_participants))

        self.note_entry.delete(0, 'end')

        # original_note 可能是 str 也可能是 None
        if original_note:
            self.note_entry.insert(0, original_note)  # str 的情況沒問題
        else:
            self.note_entry.insert(0, '')  # 若為 None 時欄位要填入空字串

    # 頁面切換
    def on_navigate_back(self):
        self.show_page('ViewGroup')

    def on_logout(self):
        self.show_page('SignIn')

    # EDIT EXPENSE
    def on_edit(self):

        # collect data
        name = self.item_entry.get().strip()

        amount_str = self.amount_entry.get().strip().replace(',', '')

        payer = self.payer_entry.get().strip()

        participants_raw = self.participants_entry.get().strip()

        # 確定輸入格式正確
        if ',' not in participants_raw:
            if len(participants_raw.split()) > 1: # 使用者可能是用空格輸入
                self.result_label.configure(text='Please separate multiple participants with commas.', text_color='red')
                return

        participants = []
        for participant in participants_raw.split(','):
            stripped_participant = participant.strip()
            if stripped_participant:
                participants.append(stripped_participant)

        note = self.note_entry.get().strip()

        if not name or not amount_str or not payer or not participants_raw:
            self.result_label.configure(text='Please fill in all fields.', text_color='red')
            return
        if not amount_str.isdigit():
            self.result_label.configure(text='Amount must contain numbers.', text_color='red')
            return
        amount = int(amount_str)
        if amount <= 0:
            self.result_label.configure(text='Amount must be a valid positive number.', text_color='red')
            return

        group_name, members_list = get_members_info(self.controller.clicked_group_id)
        if payer not in members_list:
            self.result_label.configure(text='Payer is not a group member.', text_color='red')
            return
        invalid_participants = []
        for participant in participants:
            if participant not in members_list:
                invalid_participants.append(participant)
        if invalid_participants:
            self.result_label.configure(text=f"Participants not in group: {', '.join(invalid_participants)}", text_color='red')
            return

        # 呼叫API function
        try:
            success = edit_expense(self.controller.clicked_expense_id, name, amount, payer, participants, note)
            print('edit_expense API 回傳:', success)
        except Exception as error:
            print('edit_expense API 發生錯誤:', error)

        if success:
            self.result_label.configure(text='Expense edited successfully.', text_color='green')
            # 1 秒後回到 ViewGroup
            self.after(1000, lambda: self.on_navigate_back())
        else:
            self.result_label.configure(text='Failed to edit expense.', text_color='red')

    def reset_fields(self):
        self.result_label.configure(text='')
        # self.reset_fields()  # load 時會 delete 這時應該不用 reset
