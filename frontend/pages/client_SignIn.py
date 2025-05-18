import customtkinter as ctk
from api_client import sign_in


ctk.set_appearance_mode('System')
ctk.set_default_color_theme('blue')


class SignIn(ctk.CTkFrame):
    def __init__(self, master, on_sign_in_callback=None):
        super().__init__(master)

        # 使用 grid 讓元件居中
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)  # 上下平均分布一點空間

        font_title = ctk.CTkFont(family='Gotham', size=24, weight='bold')
        small_font = ctk.CTkFont(family='Gotham', size=12)
        # 標題
        self.title_label = ctk.CTkLabel(self, text='Group Expense Tracker', font=font_title)

        # 放 label + entry 的內部框架，方便組合左上角，並使用 grid 排版
        self.input_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.name_label = ctk.CTkLabel(self.input_frame, text='Name', font=small_font, anchor='w')
        self.name_entry = ctk.CTkEntry(self.input_frame, width=200)

        # Sign In 按鈕
        self.sign_in_button = ctk.CTkButton(self, width=200, text='Sign In', font=small_font, command=self.handle_sign_in)

        # 結果文字
        self.result_label = ctk.CTkLabel(self, width=200, text='', font=small_font)

        # 在 grid 中放入元件
        self.title_label.grid(row=0, column=0, padx=15, pady=(40, 20), sticky='nsew')
        self.input_frame.grid(row=1, column=0, sticky='nsew')
        self.name_label.grid(row=0, column=0, sticky='nsew', padx=(15, 0), pady=(0, 2))
        self.name_entry.grid(row=1, column=0, padx=15, pady=(0, 20), sticky='nsew')
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


if __name__ == '__main__':
    app = ctk.CTk()
    app.geometry('400x640')
    app.title('Group Expense Tracker')

    home_page = SignIn(app)
    home_page.pack(expand=True)

    app.mainloop()
