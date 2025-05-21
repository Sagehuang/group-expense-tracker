import customtkinter as ctk
# from api_client import get_members_info
# from api_client import leave_group


ctk.set_appearance_mode('System')
ctk.set_default_color_theme('blue')

# 【假資料】
# user_id = 1
user_name = 'Alice'
# group_id = 1
group_name = 'Group A'
members_list = ['Alice', 'Bob', 'Charlie']
## 要讓ViewMembers頁面上能出現組員名單，會需要跨頁面傳遞group_id, user_id（群組ID、可能要退出群組的當前使用者的ID）


class ViewMembers(ctk.CTkFrame):
    def __init__(self, master, show_page_callback, user_id, group_id):
        super().__init__(master)
        self.show_page = show_page_callback
        self.user_id = user_id
        self.group_id = group_id

        # group_name, members_list = get_members_info(self.group_id)

        # 整體排版
        self.grid_rowconfigure(1, weight=1)  # 可捲動區
        self.grid_columnconfigure(0, weight=1)

        self.font_top_bar = ctk.CTkFont(family='Gotham', size=20, weight='bold')
        self.mid_font = ctk.CTkFont(family='Gotham', size=16)
        self.small_font = ctk.CTkFont(family='Gotham', size=12)

        # 頂端列
        top_bar = ctk.CTkFrame(self, fg_color='#F3F6F4')
        top_bar.grid(row=0, column=0, sticky='ew')
        top_bar.grid_columnconfigure(1, weight=1)

        self.back_button = ctk.CTkButton(top_bar, text='Back', font=self.small_font, command=self.on_navigate_back, width=80)
        self.title_label = ctk.CTkLabel(top_bar, text='Members', text_color='black', font=self.font_top_bar)
        self.logout_button = ctk.CTkButton(top_bar, text='Logout', font=self.small_font, command=self.on_logout, width=80)

        self.back_button.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.title_label.grid(row=0, column=1, padx=10, pady=10)
        self.logout_button.grid(row=0, column=2, padx=10, pady=10, sticky='e')

        # 可捲動區
        self.scrollable = ctk.CTkScrollableFrame(self)
        self.scrollable.grid(row=1, column=0, sticky='nsew', padx=10)

        # 成員資訊（靜態顯示，不會更新）
        members_frame = ctk.CTkFrame(self.scrollable, fg_color='transparent')
        members_frame.pack(padx=10, pady=10, fill='x')
        members_frame.grid_columnconfigure(0, weight=1)

        group_name_label = ctk.CTkLabel(members_frame, text=f'Group: {group_name}', font=self.mid_font)
        group_id_label = ctk.CTkLabel(members_frame, text=f'ID: {group_id}', font=self.small_font)
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

        # Leave Group button
        bottom_frame = ctk.CTkFrame(self, fg_color='transparent')
        bottom_frame.grid(row=2, column=0, sticky='ew', padx=10, pady=10)
        bottom_frame.grid_columnconfigure(0, weight=1)

        self.leave_group_button = ctk.CTkButton(bottom_frame, text='Leave Group', font=self.small_font, command=self.on_leave_group)
        self.leave_group_button.grid(row=0, column=0, padx=10)

        # result
        self.result_label = ctk.CTkLabel(bottom_frame, text='', text_color='red')
        self.result_label.grid(row=7, column=0, columnspan=2, pady=(5, 0))

    # 頁面切換
    def on_navigate_back(self):
        self.show_page('ViewGroup')

    def on_logout(self):
        self.show_page('SignIn')

    # LEAVE GROUP
    def on_leave_group(self):

        ## 呼叫API function
        # success = leave_group(self.user_id, self.group_id)

        ## 驗證是否成功
        # print('送出資料:', expense_data)
        # print('API 回傳:', success)

        # 假設成功
        success = True
        if success:
            self.result_label.configure(text='Left group.', text_color='green')
            # 1秒後回到HomePage
            self.after(1000, lambda: self.show_page('HomePage'))
        else:
            self.result_label.configure(text='Failed to leave group.', text_color='red')
        return


if __name__ == '__main__':
    app = ctk.CTk()
    app.geometry('400x640')
    app.title('Group Expense Tracker')

    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(0, weight=1)

    view_members = ViewMembers(app, show_page_callback)
    view_members.grid(row=0, column=0, sticky='nsew')

    app.mainloop()
