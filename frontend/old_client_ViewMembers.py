import customtkinter as ctk


ctk.set_appearance_mode('System')
ctk.set_default_color_theme('blue')


# 先自行設定假資料
class Group:
    def __init__(self, name, ID, members):
        self.name = name
        self.ID = ID
        self.members = members

class User:
    def __init__(self, name):
        self.name = name


# =====


class ViewMembers(ctk.CTkFrame):
    def __init__(self, master, group_name):
        super().__init__(master)
        self.group_name = group_name



        # 整體排版
        self.grid_rowconfigure(1, weight=1)  # 可捲動區
        self.grid_columnconfigure(0, weight=1)

        font_top_bar = ctk.CTkFont(family='Gotham', size=20, weight='bold')
        mid_font = ctk.CTkFont(family='Gotham', size=16)
        small_font = ctk.CTkFont(family='Gotham', size=12)

        # 頂端列
        top_bar = ctk.CTkFrame(self, fg_color='#F3F6F4')
        top_bar.grid(row=0, column=0, sticky='ew')
        top_bar.grid_columnconfigure(1, weight=1)

        self.back_button = ctk.CTkButton(top_bar, text='Back', font=small_font, command=self.on_navigate_back, width=80)
        self.title_label = ctk.CTkLabel(top_bar, text='Members', text_color='black', font=font_top_bar)
        self.logout_button = ctk.CTkButton(top_bar, text='Logout', font=small_font, command=self.on_logout, width=80)

        self.back_button.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.title_label.grid(row=0, column=1, padx=10, pady=10)
        self.logout_button.grid(row=0, column=2, padx=10, pady=10, sticky='e')


        # 可捲動區
        scrollable = ctk.CTkScrollableFrame(self)
        scrollable.grid(row=1, column=0, sticky='nsew', padx=10)

        # 模擬群組內有成員
        User_list = [User('Alice'), User('Bob')]
        self.group_members = [Group('Group A', str(000012), User_list)] 
        # 預期 self.group_members 是從資料庫抓取，列表中為 Group 類別

        if self.group_members:
            for i in range(len(self.group_members)):
                members_frame = ctk.CTkFrame(scrollable, fg_color='transparent')
                members_frame.pack(padx=10, pady=10, fill='x')
                members_frame.grid_columnconfigure(0, weight=1)

                group = self.group_members[i]
                group_name = group.name
                group_id = group.ID
                group_members = group.members

                group_name_label = ctk.CTkLabel(members_frame, text=f'Group Name: {group_name}', font=mid_font)
                group_id_label = ctk.CTkLabel(members_frame, text=f'ID: {group_id}', font=small_font)

                group_name_label.grid(row=0, column=0, padx=20)
                group_id_label.grid(row=1, column=0, padx=20)

                # 正確：針對 group.members 迴圈
                for idx_member, member in enumerate(self.group_members[i].members): # self.group_members[i].members：一個Group object裡面的屬性members
                    # self.group_members：list（集合），每個元素都是一個 Group object
                    # self.group_members[i]：一個Group object
                    # self.group_members[i].name：一個Group object裡面的屬性name
                    # self.group_members[i].ID：一個Group object裡面的屬性ID
                    # self.group_members[i].members：一個Group object裡面的屬性members
                    
                    group_member_label = ctk.CTkLabel(members_frame, text=member.name, font=mid_font)
                    group_member_label.grid(row=2 + idx_member * 2, column=0, padx=20, sticky='w') # double space

                    # 加一條黑色橫線
                    line_frame = ctk.CTkFrame(members_frame, height=1, fg_color='black')
                    line_frame.grid(row=3 + idx_member * 2, column=0, padx=20, sticky='ew') # double space

        else:
            no_members_label = ctk.CTkLabel(scrollable, text='There are no members in this group.', font=small_font)
            no_members_label.pack(pady=20)



        # 底部按鈕
        bottom_frame = ctk.CTkFrame(self, fg_color='transparent')
        bottom_frame.grid(row=2, column=0, sticky='ew', padx=10, pady=10)

        bottom_frame.grid_columnconfigure(0, weight=1)

        self.leave_group_button = ctk.CTkButton(bottom_frame, text='Leave Group', font=small_font, command=self.on_leave_group)
        self.leave_group_button.grid(row=0, column=0, padx=10)


# 轉換頁面

    def on_navigate_back(self):
        return

    def on_logout(self):
        return

    def on_leave_group(self):
        return


if __name__ == '__main__':
    app = ctk.CTk()
    app.geometry('400x640')
    app.title('Group Expense Tracker')

    view_members = ViewMembers(app, 'Group A')
    view_members.pack(fill='both', expand=True)

    app.mainloop()
