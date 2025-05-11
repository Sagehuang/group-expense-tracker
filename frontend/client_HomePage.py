import customtkinter as ctk


ctk.set_appearance_mode('System')
ctk.set_default_color_theme('blue')


class Dashboard(ctk.CTkFrame):
    def __init__(self, master, username):
        super().__init__(master)
        self.username = username

        # 整體排版
        self.grid_rowconfigure(1, weight=1)  # 可捲動區
        self.grid_columnconfigure(0, weight=1)

        font_top_bar = ctk.CTkFont(family='Gotham', size=20, weight='bold')
        small_font = ctk.CTkFont(family='Gotham', size=12)

        # 頂端列
        top_bar = ctk.CTkFrame(self, fg_color='#F3F6F4')
        top_bar.grid(row=0, column=0, sticky='ew')
        top_bar.grid_columnconfigure(1, weight=1)

        self.home_button = ctk.CTkButton(top_bar, text='Home', font=small_font, command=self.on_navigate_home, width=80)
        self.title_label = ctk.CTkLabel(top_bar, text='My Group', text_color='black', font=font_top_bar)
        self.logout_button = ctk.CTkButton(top_bar, text='Logout', font=small_font, command=self.on_logout, width=80)

        self.logout_button.grid(row=0, column=2, padx=10, pady=10, sticky='e')
        self.home_button.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.title_label.grid(row=0, column=1, padx=10, pady=10)

        # 主體捲動區
        scrollable = ctk.CTkScrollableFrame(self)
        scrollable.grid(row=1, column=0, sticky='nsew', padx=10)

        # 模擬是否有群組
        self.groups = []  # 空代表尚未加入群組

        if self.groups:
            for i, group_name in self.groups:
                group_button = ctk.CTkButton(scrollable, text=group_name, font=small_font)
                group_button.pack(pady=5)
        else:
            no_group_label = ctk.CTkLabel(scrollable, text='Add or Join a group!', font=small_font)
            no_group_label.pack(pady=20)

        # 底部按鈕
        bottom_frame = ctk.CTkFrame(self, fg_color='transparent')
        bottom_frame.grid(row=2, column=0, sticky='ew', padx=10, pady=10)

        bottom_frame.grid_columnconfigure((0, 1), weight=1)  # 左右側按鈕各占一半

        self.add_group_button = ctk.CTkButton(bottom_frame, text='Add Group', font=small_font, command=self.on_add_group)
        self.join_group_button = ctk.CTkButton(bottom_frame, text='Join Group', font=small_font, command=self.on_join_group)

        self.add_group_button.grid(row=0, column=0, padx=10, sticky='ew')
        self.join_group_button.grid(row=0, column=1, padx=10, sticky='ew')

        # # 查詢元件寬度
        # def check_button_sizes():
        #     print("Add Group button width:", self.add_group_button.winfo_width())
        #     print("Join Group button width:", self.join_group_button.winfo_width())

        # self.after(100, check_button_sizes)


# 轉換頁面


    def on_navigate_home(self):
        return

    def on_logout(self):
        return

    def on_add_group(self):
        return

    def on_join_group(self):
        return


if __name__ == '__main__':
    app = ctk.CTk()
    app.geometry('400x640')
    app.title('Group Expense Tracker')

    dashboard = Dashboard(app, 'Alice')
    dashboard.pack(fill='both', expand=True)

    app.mainloop()
