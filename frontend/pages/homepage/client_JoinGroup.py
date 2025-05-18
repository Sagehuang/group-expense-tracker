import customtkinter as ctk


ctk.set_appearance_mode('System')
ctk.set_default_color_theme('blue')


class JoinGroup(ctk.CTkFrame):
    def __init__(self, master, username):
        super().__init__(master)
        self.username = username

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        font_top_bar = ctk.CTkFont(family='Gotham', size=20, weight='bold')
        small_font = ctk.CTkFont(family='Gotham', size=12)

        top_bar = ctk.CTkFrame(self, fg_color='#F3F6F4')
        top_bar.grid(row=0, column=0, sticky='ew')
        top_bar.grid_columnconfigure(1, weight=1)

        self.home_button = ctk.CTkButton(top_bar, text='Home', font=small_font, command=self.on_navigate_home, width=80)
        self.title_label = ctk.CTkLabel(top_bar, text='Join Group', text_color='black', font=font_top_bar)
        self.logout_button = ctk.CTkButton(top_bar, text='Logout', font=small_font, command=self.on_logout, width=80)

        self.logout_button.grid(row=0, column=2, padx=10, pady=10, sticky='e')
        self.home_button.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.title_label.grid(row=0, column=1, padx=10, pady=10)

        # -----

        main_space = ctk.CTkFrame(self, fg_color='transparent')
        main_space.grid(row=1, column=0, padx=10, sticky='nsew')
        main_space.grid_rowconfigure((1, 2, 3), weight=1)
        main_space.grid_columnconfigure(0, weight=1)

        self.group_name_label = ctk.CTkLabel(main_space, text='Group ID', font=small_font, anchor='w')
        self.group_name_entry = ctk.CTkEntry(main_space)
        self.add_button = ctk.CTkButton(main_space, text='Add', font=small_font, command=self.add_new_group)
        self.result_label = ctk.CTkLabel(self, text='', font=small_font)

        self.group_name_label.grid(row=0, column=0, pady=(10, 2), sticky='w')
        self.group_name_entry.grid(row=1, column=0, pady=(0, 5), sticky='nsew')
        self.add_button.grid(row=2, column=0, pady=5, sticky='nsew')
        self.result_label.grid(row=3, column=0, pady=5, sticky='nsew')

    def on_navigate_home(self):
        return

    def on_logout(self):
        return

    def add_new_group(self):
        group_name = self.group_name_entry.get().strip()
        if not group_name:
            self.result_label.configure(text='Please enter a group ID.')
            return


if __name__ == '__main__':
    app = ctk.CTk()
    app.geometry('400x640')
    app.title('Group Expense Tracker')

    join_group = JoinGroup(app, 'Alice')
    join_group.pack(expand=True)

    app.mainloop()
