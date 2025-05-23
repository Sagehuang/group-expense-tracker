import customtkinter as ctk
from api_client import sign_in

ctk.set_appearance_mode('System')
ctk.set_default_color_theme('blue')


class SignIn(ctk.CTkFrame):
    def __init__(self, master, show_page_callback, controller):
        super().__init__(master)
        self.show_page = show_page_callback
        self.controller = controller  # self.controller 就是 app 這個 object
        # 改用 self.controller.user_id 來取得或修改 user_id

        # 整體用 grid 分三行，上中下置中
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # 主體框架，放標題與輸入元件
        self.main_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.main_frame.grid(row=1, column=0, sticky='nsew')
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Pre-defined fonts
        self.font_title = ctk.CTkFont(family='Gotham', size=24, weight='bold')
        self.small_font = ctk.CTkFont(family='Gotham', size=12)

        # 標題
        self.title_label = ctk.CTkLabel(self.main_frame, text='Group Expense Tracker', font=self.font_title)
        self.title_label.grid(row=0, column=0, pady=(0, 20), sticky='ew')

        # 放 label, entry 的內部框架
        self.input_frame = ctk.CTkFrame(self.main_frame, fg_color='transparent')
        self.input_frame.grid(row=1, column=0, pady=10)
        self.input_frame.grid_columnconfigure(0, weight=1)

        # 固定寬度的 container_frame，讓 label, entry 對齊
        self.container_frame = ctk.CTkFrame(self.input_frame, fg_color='transparent', width=200)
        self.container_frame.grid(row=0, column=0)  # 不加 sticky，預設置中
        self.container_frame.grid_columnconfigure(0, weight=1)

        # Label 和 Entry 都放在這個固定寬度的區塊中
        self.name_label = ctk.CTkLabel(self.container_frame, text='Name', font=self.small_font, anchor='w')
        self.name_entry = ctk.CTkEntry(self.container_frame, width=200)

        self.name_label.grid(row=0, column=0, sticky='w', pady=(0, 2))
        self.name_entry.grid(row=1, column=0, sticky='w', pady=(0, 20))  # sticky='w' 對齊左邊

        # Sign In button
        self.sign_in_button = ctk.CTkButton(self.main_frame, width=75, text='Sign In', font=self.small_font, command=self.handle_sign_in)
        self.sign_in_button.grid(row=2, column=0, pady=(0, 10))

        # 結果文字
        self.result_label = ctk.CTkLabel(self.main_frame, width=200, text='', font=self.small_font)
        self.result_label.grid(row=3, column=0, pady=(0, 10))

    def handle_sign_in(self):
        name = self.name_entry.get().strip()
        if not name:
            self.result_label.configure(text='Please enter a name.')
            return

        try:  # !!!
            self.controller.user_id = sign_in(name)
            print(f'User ID {self.controller.user_id} logging in...')
        except Exception as error:
            print(error)

        if self.controller.user_id:
            self.result_label.configure(text=f'Welcome, {name}!', text_color='green')
            # 1秒後跳到HomePage
            self.after(1000, lambda: self.show_page('HomePage'))
        else:
            self.result_label.configure(text='Sign-in failed.', text_color='red')

    def reset_fields(self):
        self.name_entry.delete(0, 'end')
        self.result_label.configure(text='')


if __name__ == '__main__':
    app = ctk.CTk()
    app.geometry('400x640')
    app.title('Group Expense Tracker')

    # 設定 app 內 grid
    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(0, weight=1)

    sign_in = SignIn(app, show_page_callback)
    sign_in.grid(row=0, column=0, sticky='nsew')

    app.mainloop()
