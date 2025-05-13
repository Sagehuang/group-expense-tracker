import customtkinter as ctk
from api_client import sign_in


ctk.set_appearance_mode('System')
ctk.set_default_color_theme('blue')


class HomePage(ctk.CTkFrame):
    def __init__(self, master, on_sign_in_callback=None):
        super().__init__(master)

        # 使用 grid 讓元件居中
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)  # 上下平均分布一點空間

        font_title = ctk.CTkFont(family='Gotham', size=24,
                                        weight='bold')
        small_font = ctk.CTkFont(family='Gotham', size=12)
        # 標題
        self.title_label = ctk.CTkLabel(self, text='Group Expense Tracker',
                                        font=font_title)

        # 放 label + entry 的內部框架，方便組合左上角，並使用 grid 排版
        self.input_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.name_label = ctk.CTkLabel(self.input_frame, text='Name',
                                       font=small_font, anchor='w')
        self.name_entry = ctk.CTkEntry(self.input_frame, width=200)

        # Sign In 按鈕
        self.sign_in_button = ctk.CTkButton(self, width=200, text='Sign In',
                                            font=small_font,
                                            command=self.handle_sign_in)

        # 結果文字
        self.result_label = ctk.CTkLabel(self, width=200, text='',
                                         font=small_font)

        # 在 grid 中放入元件
        self.title_label.grid(row=0, column=0, padx=15, pady=(40, 20),
                              sticky='nsew')
        self.input_frame.grid(row=1, column=0, sticky='nsew')
        self.name_label.grid(row=0, column=0, sticky='nsew',
                             padx=(15, 0), pady=(0, 2))
        self.name_entry.grid(row=1, column=0, padx=15, pady=(0, 20),
                             sticky='nsew')
        self.sign_in_button.grid(row=2, column=0, padx=15, sticky='nsew')
        self.result_label.grid(row=3, column=0, padx=15, sticky='nsew')

    def handle_sign_in(self):
        name = self.name_entry.get().strip()
        if not name:
            self.result_label.configure(text='Please enter a name.')
            return

        user = sign_in(name)  # 將 name 發給 backend 處理註冊登入邏輯，return 是否成功登入
        print(user)
        if user:
            self.result_label.configure(text=f"Signed in as {user['name']}")
        else:
            self.result_label.configure(text='Sign-in failed.')


'''
class Dashboard(ctk.CTkFrame):
    def __init__(self, master, username, on_navigate_home, on_logout,
                 on_add_group=None, on_join_group=None):
        super().__init__(master)
        self.username = username

        # 整體排版
        self.grid_rowconfigure(1, weight=1)  # 可捲動區
        self.grid_columnconfigure(0, weight=1)

        # 頂端列
        top_bar = ctk.CTkFrame(self, fg_color="blue")
        top_bar.grid(row=0, column=0, sticky="ew")
        top_bar.grid_columnconfigure(1, weight=1)

        self.home_button = ctk.CTkButton(top_bar, text="Home",
                                         command=on_navigate_home,
                                         width=80)
        self.title_label = ctk.CTkLabel(top_bar, text="My Group",
                                        font=ctk.CTkFont(size=18,
                                                         weight="bold"))
        self.logout_button = ctk.CTkButton(top_bar, text="Logout",
                                           command=on_logout, width=80)

        self.logout_button.grid(row=0, column=2, padx=10, pady=10, sticky="e")
        self.home_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.title_label.grid(row=0, column=1, padx=10, pady=10)

        # 主體捲動區
        scrollable = ctk.CTkScrollableFrame(self)
        scrollable.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        # 模擬是否有群組
        self.groups = []  # 空代表尚未加入群組

        if self.groups:
            for i, group_name in self.groups:
                group_button = ctk.CTkButton(scrollable, text=group_name)
                group_button.pack(pady=5)
        else:
            no_group_label = ctk.CTkLabel(scrollable,
                                          text="Add or Join a group!",
                                          font=ctk.CTkFont(size=14))
            no_group_label.pack(pady=20)

        # 底部按鈕
        bottom_frame = ctk.CTkFrame(scrollable, fg_color="transparent")
        bottom_frame.pack(pady=20)

        self.add_group_button = ctk.CTkButton(bottom_frame, text="Add Group",
                                              command=on_add_group)
        self.add_group_button.pack(side="left", padx=10)

        self.join_group_button = ctk.CTkButton(bottom_frame, text="Join Group",
                                               command=on_join_group)
        self.join_group_button.pack(side="left", padx=10)
'''

if __name__ == '__main__':
    app = ctk.CTk()
    app.geometry('400x640')
    app.title('Group Expense Tracker')

    home_page = HomePage(app)
    home_page.pack(expand=True)

    app.mainloop()
