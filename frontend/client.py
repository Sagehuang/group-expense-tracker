import tkinter as tk
from api_client import sign_in

def handle_sign_in():
    name = name_entry.get().strip()
    if not name:
        result_label.config(text="Please enter a name.")
        return

    user = sign_in(name)  # 將 name 發給 backend 處理註冊登入邏輯，return 是否成功登入
    print(user)
    if user:
        result_label.config(text=f"Signed in as {user['name']}")
    else:
        result_label.config(text="Sign-in failed.")

# 建立 GUI 視窗
window = tk.Tk()
window.title("Group Expense Sign-In")
window.geometry("300x180")

# 輸入欄位與按鈕
tk.Label(window, text="Enter your name:").pack(pady=10)
name_entry = tk.Entry(window)
name_entry.pack()

sign_in_button = tk.Button(window, text="Sign In", command=handle_sign_in)
sign_in_button.pack(pady=10)

result_label = tk.Label(window, text="")
result_label.pack()

window.mainloop()
