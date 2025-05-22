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

        font_top_bar = ctk.CTkFont(family='Gotham', size=20, weight='bold')
        small_font = ctk.CTkFont(family='Gotham', size=12)

        # 頂端列
        top_bar = ctk.CTkFrame(self, fg_color='#F3F6F4')
        top_bar.grid(row=0, column=0, sticky='ew')
        top_bar.grid_columnconfigure(0, weight=0)
        top_bar.grid_columnconfigure(1, weight=1)
        top_bar.grid_columnconfigure(2, weight=0)

        self.home_button = ctk.CTkButton(top_bar, text='Home', font=small_font, command=self.on_navigate_home, width=80)
        self.title_label = ctk.CTkLabel(top_bar, text='My Group', text_color='black', font=font_top_bar)
        self.logout_button = ctk.CTkButton(top_bar, text='Logout', font=small_font, command=self.on_logout, width=80)

        self.home_button.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.title_label.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
        self.logout_button.grid(row=0, column=2, padx=10, pady=10, sticky='e')

        # 群組假資料
        '''
        self.current_groups = [{'id': 1, 'name': 'Group A', 'members': [1, 2, 4]},
                               {'id': 2, 'name': 'Group B', 'members': [1, 3, 4]},
                               {'id': 3, 'name': 'Group C', 'members': [1, 9, 10]},
                               {'id': 4, 'name': 'Group D', 'members': [1, 8, 23]}]
        '''

        try:  # !!!
            self.current_groups = get_groups_info(self.controller.user_id)
            print(f'API 回傳：{self.current_groups}')
        except Exception as error:
            print(f'API 發生錯誤：{error}')

        # 主體捲動區
        scrollable = ctk.CTkScrollableFrame(self)
        scrollable.grid(row=1, column=0, sticky='nsew', padx=10, pady=(0, 10))
        scrollable.grid_columnconfigure(0, weight=1)

        if self.current_groups:
            for group in self.current_groups:
                group_button = ctk.CTkButton(scrollable, text=group['name'], text_color='#FFFFFF', font=small_font,
                                             border_width=1, border_color='#B0B0B0',  # '#F3F6F4'
                                             fg_color='#B0B0B0',  # 'transparent'
                                             command=lambda g=group: self.check_group(g))
                group_button.pack(fill='x', padx=5, pady=5)
        else:
            no_group_label = ctk.CTkLabel(scrollable, text='You are not in any group for now. :(\nWhy not try adding or joining a group?', font=small_font)
            no_group_label.pack(pady=20)

        # 底部按鈕
        bottom_frame = ctk.CTkFrame(self, fg_color='transparent')
        bottom_frame.grid(row=2, column=0, sticky='ew', padx=10, pady=10)
        bottom_frame.grid_columnconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(1, weight=1)

        self.add_group_button = ctk.CTkButton(bottom_frame, text='Add Group', font=small_font, command=self.on_add_group)
        self.join_group_button = ctk.CTkButton(bottom_frame, text='Join Group', font=small_font, command=self.on_join_group)

        self.add_group_button.grid(row=0, column=0, padx=10, sticky='ew')
        self.join_group_button.grid(row=0, column=1, padx=10, sticky='ew')

    # 頁面切換
    def on_navigate_home(self):
        return

    def on_logout(self):
        self.show_page('SignIn')

    def check_group(self, group):
        self.controller.clicked_group_id = group['group_id']
        print('Checking the group with ID {self.controller.clicked_group_id}...')
        self.show_page('ViewGroup')

    def on_add_group(self):
        self.show_page('AddGroup')

    def on_join_group(self):
        self.show_page('JoinGroup')


if __name__ == '__main__':
    app = ctk.CTk()
    app.geometry('400x640')
    app.title('Group Expense Tracker')

    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(0, weight=1)

    homepage = HomePage(app, show_page_callback)
    homepage.grid(row=0, column=0, sticky='nsew')

    app.mainloop()
