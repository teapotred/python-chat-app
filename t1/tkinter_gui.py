import customtkinter

def button_callback():
    print("button clicked")

app = customtkinter.CTk()
app.geometry("400x150")



app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

button = customtkinter.CTkButton(app, text="my button", command=button_callback)
button.grid(row=1, column=1, sticky="ew")

tk_textbox = customtkinter.CTkTextbox(app, activate_scrollbars=False)
tk_textbox.grid(row=1, column =0, sticky="nsew")

tk_scrollbar = customtkinter.CTkScrollbar(app, command=tk_textbox.yview)
tk_scrollbar.grid(row=0, column=2, sticky="ns")

tk_textbox.configure(yscrollcommand=tk_scrollbar.set)




app.mainloop()

