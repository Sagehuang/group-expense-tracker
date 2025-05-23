import customtkinter as ctk
from api_client import add_group

ctk.set_appearance_mode('System')
ctk.set_default_color_theme('blue')


class AddGroup(ctk.CTkFrame):
    def __init__(self, master, show_page_callback, controller):
        super().__init__(master)
        self.show_page = show_page_callback
        self.controller = controller

        # 版面配置
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Pre-defined fonts
        self.font_title = ctk.CTkFont(family='Gotham', size=24, weight='bold')
        self.font_top_bar = ctk.CTkFont(family='Gotham', size=20, weight='bold')
        self.small_font = ctk.CTkFont(family='Gotham', size=12)

        # 頂端列設置
        self.top_bar = ctk.CTkFrame(self, fg_color='#F3F6F4')
        self.top_bar.grid(row=0, column=0, sticky='ew')
        self.top_bar.grid_columnconfigure(1, weight=1)

        # 設定頂端列的物件
        self.home_button = ctk.CTkButton(self.top_bar, text='Home', font=self.small_font, command=self.on_navigate_home, width=80)
        self.title_label = ctk.CTkLabel(self.top_bar, text='Add Group', text_color='black', font=self.font_top_bar)
        self.logout_button = ctk.CTkButton(self.top_bar, text='Logout', font=self.small_font, command=self.on_logout, width=80)

        # 將物件放入頂端列
        self.logout_button.grid(row=0, column=2, padx=10, pady=10, sticky='e')
        self.home_button.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.title_label.grid(row=0, column=1, padx=10, pady=10)

        # 主體框架，放標題與輸入元件
        self.main_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.main_frame.grid(row=1, column=0, padx=10, sticky='nsew')
        self.main_frame.grid_columnconfigure(0, weight=1)

        # spacer，排版用
        self.spacer = ctk.CTkLabel(self.main_frame, text='', font=self.font_title)
        self.spacer.grid(row=0, column=0, pady=(0, 20), sticky='ew')

        # 放 label, entry 的內部框架
        self.input_frame = ctk.CTkFrame(self.main_frame, fg_color='transparent')
        self.input_frame.grid(row=1, column=0, pady=10)
        self.input_frame.grid_columnconfigure(0, weight=1)

        # 固定寬度的 container_frame，讓 label, entry 對齊
        self.container_frame = ctk.CTkFrame(self.input_frame, fg_color='transparent', width=200)
        self.container_frame.grid(row=0, column=0)
        self.container_frame.grid_columnconfigure(0, weight=1)

        # Label 和 Entry 都放在這個固定寬度的區塊中
        self.group_name_label = ctk.CTkLabel(self.container_frame, text='Group Name', font=self.small_font, anchor='w')
        self.group_name_entry = ctk.CTkEntry(self.container_frame, width=200)
        self.group_name_label.grid(row=0, column=0, sticky='w', pady=(0, 2))
        self.group_name_entry.grid(row=1, column=0, sticky='w', pady=(0, 10))  # sticky='w' 對齊左邊

        # Add button
        self.add_button = ctk.CTkButton(self.main_frame, width=50, text='Add', font=self.small_font, command=self.add_new_group)
        self.add_button.grid(row=2, column=0, pady=(0, 10))

        # 結果文字
        self.result_label = ctk.CTkLabel(self.main_frame, width=200, text='', font=self.small_font)
        self.result_label.grid(row=3, column=0, pady=(0, 10))

    # 頁面切換
    def on_navigate_home(self):
        self.show_page('HomePage')

    def on_logout(self):
        self.show_page('SignIn')

    # ADD GROUP
    def add_new_group(self):
        group_name = self.group_name_entry.get().strip()
        if group_name:
            try:  # !!!
                new_group = add_group(group_name, self.controller.user_id)
                self.result_label.configure(text='Group added successfully.', text_color='green')
                print('add_group API 回傳:', new_group)
                # 1秒後回到HomePage並清空結果文字與文字框
                self.after(1000, lambda: self.on_navigate_home())
                self.after(1000, lambda: self.result_label.configure(text=''))
                self.after(1000, lambda: self.group_name_entry.delete(0, 'end'))
            except Exception as error:
                self.result_label.configure(text='Failed to add group.', text_color='red')
                print(error)
        else:
            self.result_label.configure(text='Please enter a Group Name.', text_color='red')


if __name__ == '__main__':
    app = ctk.CTk()
    app.geometry('400x640')
    app.title('Group Expense Tracker')

    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(0, weight=1)

    add_group = AddGroup(app, show_page_callback)
    add_group.grid(row=0, column=0, sticky='nsew')

    app.mainloop()
