import customtkinter as ctk
from api_client import get_members_info, leave_group

ctk.set_appearance_mode('System')
ctk.set_default_color_theme('blue')


class ViewMembers(ctk.CTkFrame):
    def __init__(self, master, show_page_callback, controller):
        super().__init__(master)
        self.show_page = show_page_callback
        self.controller = controller

        # 整體排版
        self.grid_rowconfigure(1, weight=1)  # 可捲動區
        self.grid_columnconfigure(0, weight=1)

        self.font_top_bar = ctk.CTkFont(family='Gotham', size=20, weight='bold')
        self.mid_font = ctk.CTkFont(family='Gotham', size=16)
        self.small_font = ctk.CTkFont(family='Gotham', size=12)

        # 頂端列
        self.top_bar = ctk.CTkFrame(self, fg_color='#F3F6F4')
        self.top_bar.grid(row=0, column=0, sticky='ew')
        self.top_bar.grid_columnconfigure(1, weight=1)

        self.back_button = ctk.CTkButton(self.top_bar, text='Back', font=self.small_font, command=self.on_navigate_back, width=80)
        self.title_label = ctk.CTkLabel(self.top_bar, text='Members', text_color='black', font=self.font_top_bar)
        self.logout_button = ctk.CTkButton(self.top_bar, text='Logout', font=self.small_font, command=self.on_logout, width=80)

        self.back_button.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.title_label.grid(row=0, column=1, padx=10, pady=10)
        self.logout_button.grid(row=0, column=2, padx=10, pady=10, sticky='e')

        # 可捲動區
        self.scrollable = ctk.CTkScrollableFrame(self)
        self.scrollable.grid(row=1, column=0, sticky='nsew', padx=10)

        # Leave Group button
        self.bottom_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.bottom_frame.grid(row=2, column=0, sticky='ew', padx=10, pady=10)
        self.bottom_frame.grid_columnconfigure(0, weight=1)

        self.leave_group_button = ctk.CTkButton(self.bottom_frame, text='Leave Group', font=self.small_font, command=self.on_leave_group)
        self.leave_group_button.grid(row=0, column=0, padx=10)

        # result
        self.result_label = ctk.CTkLabel(self.bottom_frame, text='', text_color='red')
        self.result_label.grid(row=7, column=0, columnspan=2, pady=(5, 0))

    def load_members(self):
        for widget in self.scrollable.winfo_children():
            widget.destroy()

        group_name, members_list = get_members_info(self.controller.clicked_group_id)

        members_frame = ctk.CTkFrame(self.scrollable, fg_color='transparent')
        members_frame.pack(padx=10, pady=10, fill='x')
        members_frame.grid_columnconfigure(0, weight=1)

        group_name_label = ctk.CTkLabel(members_frame, text=f'Group: {group_name}', font=self.mid_font)
        group_id_label = ctk.CTkLabel(members_frame, text=f'ID: {self.controller.clicked_group_id}', font=self.small_font)
        group_name_label.grid(row=0, column=0, padx=20)
        group_id_label.grid(row=1, column=0, padx=20)

        if members_list:
            for index, member in enumerate(members_list):
                member_label = ctk.CTkLabel(members_frame, text=member, font=self.mid_font)
                member_label.grid(row=2 + index * 2, column=0, padx=20, sticky='w')

                line_frame = ctk.CTkFrame(members_frame, height=1, fg_color='black')
                line_frame.grid(row=3 + index * 2, column=0, padx=20, sticky='ew')
        else:
            no_members_label = ctk.CTkLabel(members_frame, text='There are no members in this group.', font=self.small_font)
            no_members_label.grid(row=2, column=0, padx=20, pady=10)

    # 頁面切換
    def on_navigate_back(self):
        self.show_page('ViewGroup')

    def on_logout(self):
        self.show_page('SignIn')

    # LEAVE GROUP
    def on_leave_group(self):
        try:
            success = leave_group(self.controller.user_id, self.controller.clicked_group_id)
            print('leave_group API 回傳:', success)
        except Exception as error:
            print('leave_group API 發生錯誤:', error)

        if success:
            self.result_label.configure(text='Left group.', text_color='green')
            # 1 秒後回到 HomePage
            self.after(1000, lambda: self.show_page('HomePage'))
        else:
            self.result_label.configure(text='Failed to leave group.', text_color='red')
        return

    def reset_fields(self):
        self.result_label.configure(text='')
