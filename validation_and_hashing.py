import re
import bcrypt 


class ValidateCredentials:
    # Define the regular expressions
    name_regex = r"^[a-zA-Z0-9 ]{3,32}$"
    username_regex = r"^[a-zA-Z0-9]{3,32}$"
    email_regex = r"^[a-zA-Z0-9._%+-]+@(gmail\.com|outlook\.com|hotmail\.com|yahoo\.com|icloud\.com|aol\.com)$"
    password_regex = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,64}$"


    def validate_name(self, name: str) -> bool:
        return bool(re.match(ValidateCredentials.name_regex, name))
    

    def validate_username(self, username: str) -> bool:
        return bool(re.match(ValidateCredentials.username_regex, username))


    def validate_email(self, email: str) -> bool:
        return bool(re.match(ValidateCredentials.email_regex, email))


    def validate_password(self, password: str) -> bool:
        return bool(re.match(ValidateCredentials.password_regex, password))



class PasswordHash:
    def generate_password_hash(self, password: str) -> str:
        # converting password to array of bytes 
        bytes = password.encode('utf-8') 

        # generating the salt 
        salt = bcrypt.gensalt() 

        # Hashing the password 
        pw_hash = bcrypt.hashpw(bytes, salt) 

        return pw_hash 
    

    def match_password_hash(self, hashed: str, user_input: str) -> str:
        # checking password 
        return bcrypt.checkpw(user_input.encode('utf-8'), bytes(hashed.encode("utf-8"))) 

