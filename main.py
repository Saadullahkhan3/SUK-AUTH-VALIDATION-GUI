# Custom Classess
from Sending_mail import SendMail
from validation_and_hashing import ValidateCredentials, PasswordHash
from sheety_curd import SheetyCURD

# GUI
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox



class Status:
    def __init__(self, controller):
        self.controller = controller
        

    def sign_up(self, username_var, username_status, name_var, name_status, email_var, email_status, password_var, password_status, confirm_password_var, confirm_password_status):
        accepted_list_score = list()

        if self.controller.validate_username(username_var.get()):
            if self.controller.verify_uniqness_of_value_by_key(key="username", value=username_var.get()):
                username_status.config(text="Accepted", fg="green")
                accepted_list_score.append(1)
            else:
                username_status.config(text="Occupied", fg="orange")
        else:
            username_status.config(text="Wrong", fg="red")


        if self.controller.validate_name(name_var.get()):
            name_status.config(text="Accepted", fg="green")
            accepted_list_score.append(1)
        else:
            name_status.config(text="Wrong", fg="red")


        if self.controller.validate_password(password_var.get()):
            password_status.config(text="Accepted", fg="green")
            if password_var.get() == confirm_password_var.get():
                confirm_password_status.config(text="Matched", fg="green")
                accepted_list_score.append(1)
            else:
                confirm_password_status.config(text="Un-Matched", fg="orange")
        else:
            password_status.config(text="Wrong", fg="red")
            confirm_password_status.config(text="Correct Password", fg="red")


        if self.controller.validate_email(email_var.get()):
            if self.controller.verify_uniqness_of_value_by_key(key="email", value=email_var.get()):
                email_status.config(text="Accepted", fg="green")
                accepted_list_score.append(1)
            else:
                email_status.config(text="Occupied", fg="orange")
        else:
            email_status.config(text="Wrong", fg="red")


        sign_up_accepted = (accepted_list_score.count(1) == 4)
        if sign_up_accepted:
            global USER_DATA
            USER_DATA = {
                "username": username_var.get(),
                "name": name_var.get(),
                "email": email_var.get(),
                "password": password_var.get(),
            }

            global ADD_THE_DATA
            ADD_THE_DATA = True

            global SEND_THE_CODE
            SEND_THE_CODE = True
            self.controller.show_frame("CodePage")
    
        return sign_up_accepted


    def sign_in(self, email_var, email_status, password_var, password_status):
        data = None

        if self.controller.validate_email(email_var.get()):
            data = self.controller.get_data_by_email(email_var.get())

            if data:
                email_status.config(text="Accepted", fg="green")
            
                if self.controller.validate_password(password_var.get()):
                    if self.controller.match_password_hash(data["password"], password_var.get()):
                        password_status.config(text="Accepted", fg="green")

                        global USER_DATA
                        USER_DATA = data

                        global SEND_THE_CODE
                        SEND_THE_CODE = True

                        self.controller.show_frame("CodePage")

                    else:
                        password_status.config(text="Not Matched", fg="orange")
                else:
                    password_status.config(text="Wrong", fg="red")
            
            else:
                email_status.config(text="Not Found", fg="red")
                password_status.config(text="Correct Email", fg="red")

        else:
            email_status.config(text="Wrong", fg="red")
            password_status.config(text="Correct Email", fg="red")

        return


    def match_delete_password(self, password_var, password_status):
        if self.controller.validate_password(password_var.get()):
            global USER_DATA

            if self.controller.match_password_hash(USER_DATA["password"], password_var.get()):
                password_status.config(text="Accepted", fg="green")
                
                global DELETE_OPERATION
                DELETE_OPERATION = True
                
                self.controller.show_frame("CodePage")

            else:
                password_status.config(text="Not Matched", fg="orange")
        else:
            password_status.config(text="Wrong", fg="red")


    def check_and_update_username(self, update_username_var, update_username_status):
        global USER_DATA
        if self.controller.validate_username(update_username_var.get()):
            if self.controller.verify_uniqness_of_value_by_key(key="username", value=update_username_var.get()):
                update_username_status.config(text="Accepted", fg="green")
                username_put = self.controller.update_data(_id = USER_DATA["id"],
                                            username = update_username_var.get(),
                                            is_username = True)
                if username_put:
                    # Update our cached data
                    USER_DATA = self.controller.get_data_by_email(USER_DATA["email"])
                    self.controller.show_frame("Home")
                else:
                    update_username_status.config(text="Error Occured while updating the username", fg="red")
            else:
                update_username_status.config(text="Occupied", fg="orange")
        else:
            update_username_status.config(text="Wrong", fg="red")


    def check_and_update_name(self, update_name_var, update_name_status):
        global USER_DATA
        if self.controller.validate_name(update_name_var.get()):
            update_name_status.config(text="Accepted", fg="green")
            name_put = self.controller.update_data(_id = USER_DATA["id"],
                                        name = update_name_var.get(),
                                        is_name = True)
            if name_put:
                # Update our cached data
                USER_DATA = self.controller.get_data_by_email(USER_DATA["email"])
                self.controller.show_frame("Home")
            else:
                update_name_status.config(text="Error Occured while updating the name", fg="red")
        else:
            update_name_status.config(text="Wrong", fg="red")


    def check_and_update_password(self, old_password_var, old_password_status, new_password_var, new_password_status):
        global USER_DATA
        global UPDATE_PASSWORD
        global _TEMP_UPDATE_PASSWORD_DICT

        accepted = False

        if self.controller.validate_password(old_password_var.get()):
            if self.controller.match_password_hash(USER_DATA["password"], old_password_var.get()):
                old_password_status.config(text="Accepted", fg="green")
                accepted = True
            else:
                old_password_status.config(text="Not Matched", fg="orange")
        else:
            old_password_status.config(text="Wrong", fg="red")

        if self.controller.validate_password(new_password_var.get()):                
            new_password_status.config(text="Accepted", fg="green")
            if accepted:
                UPDATE_PASSWORD = True
                _TEMP_UPDATE_PASSWORD_DICT = {
                    "value": new_password_var.get(),
                    "status": new_password_status
                }
                self.controller.show_frame("CodePage")
        else:
            new_password_status.config(text="Wrong", fg="red")




class Application(tk.Tk, Status, SheetyCURD, ValidateCredentials, PasswordHash):
    def __init__(self):
        super().__init__()
        SheetyCURD.__init__(self, SHEETY_END_POINT)
        self.read_data()

        self.title("Sign Up / Sign In")
        self.geometry("500x400")
    
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        
        self.frames = {}
        
        Status.__init__(self, controller=self)
        

        for F in (StartPage, SignUpPage, SignInPage, CodePage, Home, UpdateInfoPage, DeletePage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            
            frame.grid(row=0, column=0, sticky="nsew")

        # self.show_frame("Home")
        self.show_frame("StartPage")
    
    
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()



class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        signup_button = ttk.Button(self, text="Sign Up",
                                   command=lambda: controller.show_frame("SignUpPage"))
        signin_button = ttk.Button(self, text="Sign In",
                                   command=lambda: controller.show_frame("SignInPage"))
        
        signup_button.pack(pady=20)
        signin_button.pack(pady=20)



class SignUpPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        label = tk.Label(self, text="Sign Up Page")
        label.grid(row=0, column=1, pady=10)

        self.create_form()

        back_button = ttk.Button(self, text="Back to Home",
                                 command=lambda: controller.show_frame("StartPage"))
        back_button.grid(row=7, column=1, pady=10)


    def create_form(self):
        # text variables
        self.username_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.confirm_password_var = tk.StringVar()


        
        tk.Label(self, text="Username:").grid(row=1, column=0, padx=10, pady=5)
        username_entry = ttk.Entry(self, textvariable=self.username_var)
        username_entry.grid(row=1, column=1)
        self.username_status = tk.Label(self, text="", fg="red")
        self.username_status.grid(row=1, column=2)
        ttk.Button(self, text="i", command=lambda: messagebox.showinfo("Username Info", "Enter Username. \nRules: \n⦿ Must be unique \n⦿ Lowercase letters (a-z) \n⦿ Uppercase letters (A-Z) \n⦿ Numbers(0-9) \n⦿ No Spaces between words \n⦾ Minimum length is 3 letters \n⦾ Maximum length is 32 lettes")).grid(row=1, column=3, padx=5)


        tk.Label(self, text="Name:").grid(row=2, column=0, padx=10, pady=5)
        name_entry = ttk.Entry(self, textvariable=self.name_var)
        name_entry.grid(row=2, column=1)
        self.name_status = tk.Label(self, text="", fg="red")
        self.name_status.grid(row=2, column=2)
        ttk.Button(self, text="i", command=lambda: messagebox.showinfo("Name Info", "Enter your full name. \nName Rules: \n⦿ Lowercase letters (a-z) \n⦿ Uppercase letters (A-Z) \n⦿ Numbers(0-9) \n⦿ Spaces between words, spaces at start and at end will be strip.  \n⦾ Minimum length is 3 letters \n⦾ Maximum length is 32 lettes")).grid(row=2, column=3, padx=5)

        tk.Label(self, text="Email:").grid(row=3, column=0, padx=10, pady=5)
        email_entry = ttk.Entry(self, textvariable=self.email_var)
        email_entry.grid(row=3, column=1)
        self.email_status = tk.Label(self, text="", fg="red")
        self.email_status.grid(row=3, column=2)
        ttk.Button(self, text="i", command=lambda: messagebox.showinfo("Email Info", "Enter a valid email. \n⦿ Unique Email that not previously used for sign up.\nEmails are only accepted if from these sources: \n⦿ gmail.com \n⦿ outlook.com \n⦿ hotmail.com \n⦿ yahoo.com \n⦿ icloud.com \n⦿ aol.com")).grid(row=3, column=3, padx=5)

        tk.Label(self, text="Password:").grid(row=4, column=0, padx=10, pady=5)
        password_entry = ttk.Entry(self, textvariable=self.password_var, show="*")
        password_entry.grid(row=4, column=1)
        self.password_status = tk.Label(self, text="", fg="red")
        self.password_status.grid(row=4, column=2)
        ttk.Button(self, text="i", command=lambda: messagebox.showinfo("Password Info", "Enter a strong password. \nPassword should contains at least one from each: \n⦿ Lowercase letters (a-z) \n Uppercase letters (A-Z) \n⦿ Numbers(0-9) \n⦿ No Spaces between. \n⦿ Special character(!@#$%^&*)  \n⦾ Minimum length is 8 characters \n⦾ Maximum length is 64 characters")).grid(row=4, column=3, padx=5)

        tk.Label(self, text="Confirm Password:").grid(row=5, column=0, padx=10, pady=5)
        confirm_password_entry = ttk.Entry(self, textvariable=self.confirm_password_var, show="*")
        confirm_password_entry.grid(row=5, column=1)
        self.confirm_password_status = tk.Label(self, text="", fg="red")
        self.confirm_password_status.grid(row=5, column=2)
        ttk.Button(self, text="i", command=lambda: messagebox.showinfo("Confirm Password Info", "Re-enter your password.")).grid(row=5, column=3, padx=5)

        submit_btn = ttk.Button(self, text="Submit", command=lambda: self.controller.sign_up(self.username_var, self.username_status, self.name_var, self.name_status, self.email_var, self.email_status, self.password_var, self.password_status, self.confirm_password_var, self.confirm_password_status))
        submit_btn.grid(row=6, column=1, padx=10, pady=10)
        

        self.update_idletasks()
        self.update()

        

class SignInPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        label = tk.Label(self, text="Sign In Page")
        label.grid(row=0, column=1, pady=10)

        self.create_form()

        back_button = ttk.Button(self, text="Back to Home",
                                 command=lambda: controller.show_frame("StartPage"))
        back_button.grid(row=4, column=1, pady=10)


    def create_form(self):
        # textvariables
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()


        tk.Label(self, text="Email:").grid(row=1, column=0, padx=10, pady=5)
        self.email_entry = ttk.Entry(self, textvariable=self.email_var)
        self.email_entry.grid(row=1, column=1)
        self.email_status = tk.Label(self, text="", fg="red")
        self.email_status.grid(row=1, column=2)
    
        tk.Label(self, text="Password:").grid(row=2, column=0, padx=10, pady=5)
        self.password_entry = ttk.Entry(self, textvariable=self.password_var, show="*")
        self.password_entry.grid(row=2, column=1)
        self.password_status = tk.Label(self, text="", fg="red")
        self.password_status.grid(row=2, column=2)

        ttk.Button(self, text="i", command=lambda: messagebox.showinfo("Email Info", "Enter your registered email address.")).grid(row=1, column=3, padx=5)
        ttk.Button(self, text="i", command=lambda: messagebox.showinfo("Password Info", "Enter your password.")).grid(row=2, column=3, padx=5)

        submit_btn = ttk.Button(self, text="Submit", command=lambda: self.controller.sign_in(self.email_var, self.email_status, self.password_var, self.password_status))
        submit_btn.grid(row=3, column=1, padx=10, pady=10)

        self.update_idletasks()
        self.update()



class CodePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        self.sending_mail = SendMail(SMTP_EMAIL, SMTP_EMAIL_PASSWORD, SMTP_SERVER, SMTP_SSL_POST)

        self.controller = controller

        self.home_page = lambda: controller.show_frame("Home")

        self.create_code_page()


    def send_code(self):

        global SEND_THE_CODE
        if SEND_THE_CODE:
            global USER_DATA
            self.code = self.sending_mail.random_code()

            self.sending_mail.send_email(
                to_email=USER_DATA["email"],
                subject="SUK - Verification Code",
                message=self.sending_mail.code_message(self.code),
                html=True
            )

            self.send_code_btn.config(text="Resent Code")

            return self.code


    def delete_account_and_reset_cached(self):
        global USER_DATA
        global SEND_THE_CODE
        global ADD_THE_DATA
        global DELETE_OPERATION

        # Delete the account!
        delete_rq = self.controller.delete_row(USER_DATA["id"])

        # When response code is positive
        if delete_rq:
            # Reset the values
            USER_DATA = {
                "username": None,
                "name": None,
                "email": None,
                "password": None
            }
            SEND_THE_CODE = False
            ADD_THE_DATA = False
            DELETE_OPERATION = False

            # Reset the values
            self.code_var.set("")
            self.code_status.config(text="")
            self.code = ""
            
            self.controller.show_frame("StartPage")
        else:
            print(self.controller.formatted_str("ERROR While deleting the account, check internet connection Or reached usage limit."))


    def update_password(self):
        global USER_DATA
        global _TEMP_UPDATE_PASSWORD_DICT

        password_put = self.controller.update_data(_id = USER_DATA["id"],
                                                   password = _TEMP_UPDATE_PASSWORD_DICT["value"], 
                                                   is_password = True)
        if password_put:
            # Update our cached data
            USER_DATA = self.controller.get_data_by_email(USER_DATA["email"])
            # Reset the value
            _TEMP_UPDATE_PASSWORD_DICT = {
                "value": str(),
                "status": None
            }
            _TEMP_UPDATE_PASSWORD_DICT["status"].config(text="Accepted", fg="green")


            self.code_var.set("")
            self.code_status.config(text="")
            self.code = ""

            self.controller.show_frame("Home")
        else:
            _TEMP_UPDATE_PASSWORD_DICT["status"].config(text="Error Occured while updating the password", fg="red")


    def match_code(self, code_var, code_status):
        if self.code != None:
            if self.code == code_var.get():
                code_status.config(text="Accepted", fg="green")
                
                self.send_code_btn.config(text="Send Code")

                global ADD_THE_DATA
                global DELETE_OPERATION
                global UPDATE_PASSWORD

                if ADD_THE_DATA:
                    ADD_THE_DATA = False
                    self.add_the_data()
                elif DELETE_OPERATION:
                    self.delete_account_and_reset_cached()
                elif UPDATE_PASSWORD:
                    self.update_password()
                else:
                    # Reset the values
                    self.code_var.set("")
                    self.code_status.config(text="")
                    self.code = ""
                    self.home_page()
                return True 
            
            code_status.config(text="Wrong", fg="red")
            return False


    def add_the_data(self):
        global USER_DATA
        post = self.controller.add_new_row(
            username=USER_DATA["username"].strip(),
            name=USER_DATA["name"].strip(),
            email=USER_DATA["email"].strip(),
            password=str(self.controller.generate_password_hash(USER_DATA["password"].strip()))[2:-1],
        )
        if post:
            # Fetching data from Sheety to get id (row no) for deleting and updating operation if will needed in future.
            USER_DATA = self.controller.get_data_by_email(USER_DATA["email"])

            # Reset the values
            self.code_var.set("")
            self.code_status.config(text="")
            self.code = ""

            self.home_page()
        else:
            self.code_status.config(text="Error Occured while Adding the data!", fg="red")


    def create_code_page(self):
        self.send_code()   
        
        tk.Label(self, text="Enter 6-digit Code sent on your email.").grid(row=0, column=1, pady=10)
        
        self.code_var = tk.StringVar()

        tk.Label(self, text="Code:").grid(column=0, row=2, padx=20)
        tk.Entry(self, textvariable=self.code_var).grid(row=2, column=1, pady=10, padx=5)
        self.code_status = tk.Label(self, text="")
        self.code_status.grid(row=3, column=1, padx=5)


        submit_btn = ttk.Button(self, text="Submit", command=lambda: self.match_code(self.code_var, self.code_status))
        submit_btn.grid(row=4, column=1, padx=10, pady=10)


        self.send_code_btn = ttk.Button(self, text="Send Code", command=lambda: self.send_code())
        self.send_code_btn.grid(row=5, column=1, padx=10, pady=10)
            

        self.update_idletasks()
        self.update()



class Home(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.update_info_page = lambda: controller.show_frame("UpdateInfoPage")
        self.delete_page = lambda: controller.show_frame("DeletePage")

        self.welcome()

    def welcome(self):
        global USER_DATA
        

        tk.Label(self, text="SUK AUTH \nVALIDATION", font=(" 25"), fg="blue").grid(row=0, column=0, padx=10, pady=20)

        tk.Label(self, text="Username: ").grid(row=2, column=0, padx=10, pady=15)
        tk.Label(self, text=USER_DATA['username']).grid(row=2, column=1, padx=5, pady=10)

        tk.Label(self, text="Name: ").grid(row=3, column=0, padx=10, pady=10)
        tk.Label(self, text=USER_DATA['name']).grid(row=3, column=1, padx=5, pady=10)
        
        tk.Label(self, text="Email: ").grid(row=4, column=0, padx=10, pady=10)
        tk.Label(self, text=USER_DATA['email']).grid(row=4, column=1, padx=5, pady=10)

        tk.Label(self, text="Password: ").grid(row=5, column=0, padx=10, pady=10)
        tk.Label(self, text="Due to Hashing we haven't \nyour password in \noriginal form!\n").grid(row=5, column=1, padx=5, pady=10)

        reload_btn = ttk.Button(self, text="Reload ↻", command=lambda: self.welcome())
        reload_btn.grid(row=6, column=0, padx=10, pady=10)

        update_btn = ttk.Button(self, text="Update info ->", command=lambda: self.update_info_page())
        update_btn.grid(row=6, column=1, padx=10, pady=10)
        
        delete_btn = ttk.Button(self, text="⛔DELETE ACCOUNT‼⛔ ->", command=lambda: self.delete_page())
        delete_btn.grid(row=6, column=2, padx=10, pady=10)



class UpdateInfoPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.update_title = lambda: tk.Label(self, text="Update info", font=(" 25"), fg="blue").grid(row=0, column=0, pady=20, padx=20)

        self.email_update_info = lambda: tk.Label(self, text="Emails CAN'T\n be Update").grid(row=1, column=0, padx=20, pady=10)

        self.back_button = lambda: ttk.Button(self, text="<- Back", command=lambda: controller.show_frame("Home")).grid(row=7, column=1, pady=30)
        
        self.create_main_update_page()



    def remove_widgets(self):
        for widget in self.winfo_children():
            widget.grid_forget()


    def update_username(self):
        self.remove_widgets()

        self.update_username_var = tk.StringVar()
        self.update_title()

        tk.Label(self, text="New Username:").grid(row=1, column=1, padx=20, pady=10)
        tk.Entry(self, textvariable=self.update_username_var).grid(row=2, column=1, padx=20, pady=10)
        
        self.update_username_status = tk.Label(self, text="")
        self.update_username_status.grid(row=3, column=1, padx=20, pady=10)

        ttk.Button(self, text="Submit", command=lambda: self.controller.check_and_update_username(self.update_username_var, self.update_username_status)).grid(row=4, column=1, padx=20, pady=10)

        ttk.Button(self, text="Back <-", command=lambda: self.create_main_update_page()).grid(row=5, column=1, padx=20, pady=10)


    def update_name(self):
        self.remove_widgets()

        self.update_name_var = tk.StringVar()
        self.update_title()

        tk.Label(self, text="New Name:").grid(row=1, column=1, padx=20, pady=10)
        tk.Entry(self, textvariable=self.update_name_var).grid(row=2, column=1, padx=20, pady=10)
        
        self.update_name_status = tk.Label(self, text="")
        self.update_name_status.grid(row=3, column=1, padx=20, pady=10)

        ttk.Button(self, text="Submit", command=lambda: self.controller.check_and_update_name(self.update_name_var, self.update_name_status)).grid(row=4, column=1, padx=20, pady=10)

        ttk.Button(self, text="Back <-", command=lambda: self.create_main_update_page()).grid(row=5, column=1, padx=20, pady=10)


    def update_password(self):
        self.remove_widgets()

        self.update_title()
        
        self.old_password_var = tk.StringVar()
        self.new_password_var = tk.StringVar()

        tk.Label(self, text="Current Password:").grid(row=1, column=0, padx=20, pady=20)
        tk.Entry(self, textvariable=self.old_password_var).grid(row=1, column=1, padx=20, pady=10)
        self.old_password_status = tk.Label(self, text="")
        self.old_password_status.grid(row=1, column=2, padx=20, pady=10)

        tk.Label(self, text="New Password:").grid(row=2, column=0, padx=20, pady=20)
        tk.Entry(self, textvariable=self.new_password_var).grid(row=2, column=1, padx=20, pady=10)
        self.new_password_status = tk.Label(self, text="")
        self.new_password_status.grid(row=2, column=2, padx=20, pady=10)

        ttk.Button(self, text="Submit", command=lambda: self.controller.check_and_update_password(self.old_password_var, self.old_password_status, self.new_password_var, self.new_password_status)).grid(row=3, column=1, padx=20, pady=20)

        ttk.Button(self, text="Back <-", command=lambda: self.create_main_update_page()).grid(row=4, column=1, padx=20, pady=20)



    def create_main_update_page(self):
        self.remove_widgets()

        self.update_title()
        self.email_update_info()
        self.back_button()

        update_username = ttk.Button(self, text="Update Username ->", command=lambda: self.update_username())
        update_username.grid(row=2, column=1, padx=10, pady=10)

        update_name = ttk.Button(self, text="Update Name ->", command=lambda: self.update_name())
        update_name.grid(row=3, column=1, padx=10, pady=10)

        update_password = ttk.Button(self, text="Update Password ->",  command=lambda: self.update_password())
        update_password.grid(row=4, column=1, padx=10, pady=10)



class DeletePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.delete_title = lambda: tk.Label(self, text="⛔DELETE ACCOUNT‼🛑", font=(" 25"), fg="red").grid(row=0, column=0, padx=120, pady=24)

        self.delete_yes_btn_redirect = lambda: controller.show_frame("Home")
        self.delete_no_btn_redirect = lambda: controller.show_frame("Home")

        self.delete_page()


    def remove_widgets(self):
        for widget in self.winfo_children():
            widget.grid_forget()


    def recover_delete_page_and_redirect_to_home(self):
        self.remove_widgets()
        self.delete_page()
        self.controller.show_frame("Home")


    def delete_area(self):
        self.remove_widgets()

        self.delete_title()

        self.delete_password_var = tk.StringVar()

        self.row1 = tk.Label(self, text="Password:").grid(row=1, column=0, padx=140, pady=0)

        self.row2 = tk.Entry(self, textvariable=self.delete_password_var, show="*").grid(row=2, column=0, padx=140, pady=4)

        self.row3 = tk.Label(self, text="")
        self.row3.grid(row=3, column=0, padx=140, pady=10)

        self.row4 = ttk.Button(self, text="Submit", command=lambda: self.controller.match_delete_password(self.delete_password_var, self.row3))
        self.row4.grid(row=4, column=0, padx=140, pady=10)
        
        self.row5 = ttk.Button(self, text="Back <-", command=lambda: self.recover_delete_page_and_redirect_to_home())
        self.row5.grid(row=5, column=0, padx=120, pady=10)


    def delete_page(self):
        self.delete_title()
        
        self.row1 = tk.Label(self, text="Do you really want to\ndelete your account. \nThis action CAN'T be UNDONE!.", font=(" 20"), fg="red")
        self.row1.grid(row=1, column=0, padx=120, pady=20)

        self.row2 = ttk.Button(self, text="YES",command=lambda: self.delete_area())
        self.row2.grid(row=2, column=0, padx=120, pady=20)

        self.row3 = ttk.Button(self, text="NO", command=lambda: self.delete_no_btn_redirect())
        self.row3.grid(row=3, column=0, padx=120, pady=20)

        self.row4 = None
        self.row5 = None



if __name__ == "__main__":
    ADD_THE_DATA = False

    DELETE_OPERATION = False

    UPDATE_PASSWORD = False

    _TEMP_UPDATE_PASSWORD_DICT = {"value": str(), "status": None}

    USER_DATA = {
        "username": None,
        "name": None,
        "email": None,
        "password": "Saad"
    }

    SEND_THE_CODE = False

    SHEETY_END_POINT = "<Your-Sheet-endpoint>"   


    SMTP_EMAIL = r"<Your-Email>"
    SMTP_EMAIL_PASSWORD = r"<Email-Password>"
    SMTP_SERVER = "<SMTP-Server>" # This is for gmail: 'Smtp.gmail.com'
    SMTP_SSL_POST = 465    # This is for gmail SSL port
    app = Application()
    
    app.mainloop()

