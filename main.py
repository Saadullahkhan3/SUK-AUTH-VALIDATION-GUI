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
        self.sign_up_accepted = False
        self.sign_in_accepted = False
        
        self.controller.read_data()


    def sign_up(self, username_var, username_status, name_var, name_status, email_var, email_status, password_var, password_status, confirm_password_var, confirm_password_status, controller):


        if self.controller.validate_username(username_var.get()):
            if self.controller.verify_uniqness_of_value_by_key(key="username", value=username_var.get()):
                username_status.config(text="Accepted", fg="green")
                self.sign_up_accepted = True
            else:
                username_status.config(text="Occupied", fg="orange")
                self.sign_up_accepted = False
        else:
            username_status.config(text="Wrong", fg="red")


        if self.controller.validate_name(name_var.get()):
            name_status.config(text="Accepted", fg="green")
            self.sign_up_accepted = True
        else:
            name_status.config(text="Wrong", fg="red")
            self.sign_up_accepted = False


        if self.controller.validate_password(password_var.get()):
            password_status.config(text="Accepted", fg="green")
            if password_var.get() == confirm_password_var.get():
                confirm_password_status.config(text="Matched", fg="green")
                self.sign_up_accepted = True
            else:
                confirm_password_status.config(text="Un-Matched", fg="red")
                self.sign_up_accepted = False
        else:
            password_status.config(text="Wrong", fg="red")
            confirm_password_status.config(text="Correct Password", fg="red")
            self.sign_up_accepted = False


        if self.controller.validate_email(email_var.get()):
            if self.controller.verify_uniqness_of_value_by_key(key="email", value=email_var.get()):
                email_status.config(text="Accepted", fg="green")
                self.sign_up_accepted = True
            else:
                email_status.config(text="Occupied", fg="orange")
                self.sign_up_accepted = False
        else:
            email_status.config(text="Wrong", fg="red")
            self.sign_up_accepted = False


        if self.sign_up_accepted:
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
            controller.show_frame("CodePage")
    
        return self.sign_up_accepted


    def sign_in(self, email_var, email_status, password_var, password_status, code_page):
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

                        self.sign_in_accepted = True
                        code_page()

                    else:
                        password_status.config(text="Not Matched", fg="green")
                else:
                    password_status.config(text="Wrong", fg="red")
            
            else:
                email_status.config(text="Not Found", fg="red")
                password_status.config(text="Correct Email", fg="red")

        else:
            email_status.config(text="Wrong", fg="red")
            password_status.config(text="Correct Email", fg="red")

        return self.sign_in_accepted



class Application(tk.Tk, Status, SheetyCURD, ValidateCredentials, PasswordHash):
    def __init__(self):
        super().__init__()
        SheetyCURD.__init__(self, SHEETY_END_POINT)
        # self.read_data()

        self.title("Sign Up / Sign In")
        self.geometry("500x400")
    
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        
        self.frames = {}
        
        Status.__init__(self, controller=self)
        
        for F in (StartPage, SignUpPage, SignInPage, CodePage, Home):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            
            frame.grid(row=0, column=0, sticky="nsew")

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
        ttk.Button(self, text="i", command=lambda: messagebox.showinfo("Email Info", "Enter a valid email. \n⦿ Unique Email that not previously used for sign up.\nEmails are only sign_up_accepted if from these sources: \n⦿ gmail.com \n⦿ outlook.com \n⦿ hotmail.com \n⦿ yahoo.com \n⦿ icloud.com \n⦿ aol.com")).grid(row=3, column=3, padx=5)

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

        submit_btn = ttk.Button(self, text="Submit", command=lambda: self.controller.sign_up(self.username_var, self.username_status, self.name_var, self.name_status, self.email_var, self.email_status, self.password_var, self.password_status, self.confirm_password_var, self.confirm_password_status, self.controller))
        submit_btn.grid(row=6, column=1, padx=10, pady=10)
        
        # if self.status_class.sign_in_accepted:
        #     self.controller.show_frame["CodePage"]

        self.update_idletasks()
        self.update()

        

class SignInPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        label = tk.Label(self, text="Sign In Page")
        label.grid(row=0, column=1, pady=10)

        self.create_form()
        
        self.code_page = lambda: controller.show_frame("CodePage")

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

        submit_btn = ttk.Button(self, text="Submit", command=lambda: self.controller.sign_in(self.email_var, self.email_status, self.password_var, self.password_status, self.code_page))
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


    def match_code(self, code_var, code_status):
        if self.code == code_var.get():
            code_status.config(text="Accepted", fg="green")
            
            global ADD_THE_DATA
            if ADD_THE_DATA:
                self.add_the_data()
            else:
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

        self.welcome()

    def welcome(self):
        global USER_DATA
        

        tk.Label(self, text="SUK AUTH \nVALIDATION", font=(" 25"), fg="blue").grid(row=0, column=0, padx=10, pady=20)

        tk.Label(self, text="Username: ").grid(row=2, column=0, padx=10, pady=15)
        tk.Label(self, text=USER_DATA['username']).grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self, text="Name: ").grid(row=3, column=0, padx=10, pady=10)
        tk.Label(self, text=USER_DATA['name']).grid(row=3, column=1, padx=10, pady=10)
        
        tk.Label(self, text="Email: ").grid(row=4, column=0, padx=10, pady=10)
        tk.Label(self, text=USER_DATA['email']).grid(row=4, column=1, padx=10, pady=10)

        tk.Label(self, text="Password: ").grid(row=5, column=0, padx=10, pady=10)
        tk.Label(self, text="Due to Hashing we haven't \nyour password in \noriginal form!").grid(row=5, column=1, padx=10, pady=10)

        reload_btn = ttk.Button(self, text="Reload", command=lambda: self.welcome())
        reload_btn.grid(row=7, column=2, padx=10, pady=10)


if __name__ == "__main__":
    ADD_THE_DATA = False

    USER_DATA = {
        "username": None,
        "name": None,
        "email": None,
        "password": None
    }

    SEND_THE_CODE = False

    # Make sure to change it according to you!
    SHEETY_END_POINT = r"https://api.sheety.co/username/projectName/sheetName"

    # You can use gmail for SMTP free service.
    SMTP_EMAIL = r"<Your-SMTP-Email>"
    SMTP_EMAIL_PASSWORD = r"<Your-SMTP-Email-Password>"
    SMTP_SERVER = r"<SMTP-SERVER>"  # for gmail -> Smtp.gmail.com
    SMTP_SSL_POST = 465 # This port for gmail SSL, change it according to you.
    app = Application()
    
    app.mainloop()

