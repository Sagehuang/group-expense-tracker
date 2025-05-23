import customtkinter as ctk
from api_client import get_groups_info

ctk.set_appearance_mode('System')
ctk.set_default_color_theme('blue')


class HomePage(ctk.CTkFrame):
    def __init__(self, master, show_page_callback, controller):
        super().__init__(master)
        self.show_page = show_page_callback
        self.controller = controller

        # grid 行列配置
        self.grid_rowconfigure(0, weight=0)  # 頂端列高度固定
        self.grid_rowconfigure(1, weight=1)  # 主體可伸展
        self.grid_rowconfigure(2, weight=0)  # 底部按鈕高度固定
        self.grid_columnconfigure(0, weight=1)

        # Pre-defined fonts
        self.font_top_bar = ctk.CTkFont(family='Gotham', size=20, weight='bold')
        self.small_font = ctk.CTkFont(family='Gotham', size=12)

        # 頂端列設置
        self.top_bar = ctk.CTkFrame(self, fg_color='#F3F6F4')
        self.top_bar.grid(row=0, column=0, sticky='ew')
        self.top_bar.grid_columnconfigure(0, weight=0)
        self.top_bar.grid_columnconfigure(1, weight=1)
        self.top_bar.grid_columnconfigure(2, weight=0)

        # 設定頂端列的物件
        self.home_button = ctk.CTkButton(self.top_bar, text='Home', font=self.small_font, command=self.on_navigate_home, width=80)
        self.title_label = ctk.CTkLabel(self.top_bar, text='My Group', text_color='black', font=self.font_top_bar)
        self.logout_button = ctk.CTkButton(self.top_bar, text='Logout', font=self.small_font, command=self.on_logout, width=80)

        # 將物件放入頂端列
        self.home_button.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.title_label.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
        self.logout_button.grid(row=0, column=2, padx=10, pady=10, sticky='e')

        # 主體捲動區設置
        self.scrollable = ctk.CTkScrollableFrame(self)
        self.scrollable.grid(row=1, column=0, sticky='nsew', padx=10)
        self.scrollable.grid_columnconfigure(0, weight=1)

        # 底部列設置
        self.bottom_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.bottom_frame.grid(row=2, column=0, sticky='ew', padx=10, pady=10)
        self.bottom_frame.grid_columnconfigure((0, 1), weight=1)

        # 設定底部的按鈕
        self.add_group_button = ctk.CTkButton(self.bottom_frame, text='Add Group', font=self.small_font, command=self.on_add_group)
        self.join_group_button = ctk.CTkButton(self.bottom_frame, text='Join Group', font=self.small_font, command=self.on_join_group)

        # 將物件放入底部列
        self.add_group_button.grid(row=0, column=0, padx=10, sticky='ew')
        self.join_group_button.grid(row=0, column=1, padx=10, sticky='ew')

    # 從後端抓取資料，需在切換頁面時先呼叫此 method 載入資料，之後才渲染畫面
    def load_groups(self):
        # 清空 scrollable 的內容，避免先前的內容殘留
        for widget in self.scrollable.winfo_children():
            widget.destroy()

        try:
            current_groups = get_groups_info(self.controller.user_id)
            print(f'get_groups_info API 回傳: {current_groups}')
        except Exception as error:
            print(f'get_groups_info API 發生錯誤: {error}')

        if current_groups:
            for group in current_groups:
                group_button = ctk.CTkButton(self.scrollable, text=group['name'], text_color='#FFFFFF', font=self.small_font,
                                             border_width=1, border_color='#B0B0B0', fg_color='#B0B0B0',
                                             command=lambda g=group: self.check_group(g))
                group_button.pack(fill='x', padx=5, pady=5)
        else:
            self.no_group_label = ctk.CTkLabel(self.scrollable, text='You are not in any group for now. :(\nWhy not try adding or joining a group?', font=self.small_font)
            self.no_group_label.pack(pady=20)
        return

    # 頁面切換
    def on_navigate_home(self):
        return

    def on_logout(self):
        self.show_page('SignIn')

    def check_group(self, group):
        self.controller.clicked_group_id = group['id']
        self.show_page('ViewGroup')
        print(f'Checking the group with ID {self.controller.clicked_group_id}...')

    def on_add_group(self):
        self.show_page('AddGroup')

    def on_join_group(self):
        self.show_page('JoinGroup')
