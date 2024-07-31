import requests as rq



class SheetyCURD():
    def __init__(self, 
                 sheety_endpoint: str,
                 ) -> None:
        self.SHEETY_END_POINT = sheety_endpoint
        self.HEADERS = {"Content-Type" : "application/json"}


    # ------------------- UTILITIES -------------------------------
    def check_status_code(self, status_code: int) -> bool:
        '''
        Check status code, status code should be fall in 200, if yes return True, otherwise False.
        '''
        if 200 <= status_code <= 299:
            return True
        return False


    def formatted_str(self, string: str) -> str:
        return "~"*50 + "\n" + string + "\n" + "~"*50


    def get_data_by_email(self, email: str) -> int:
        try:
            data = None
            for row in self.READED_DATA["emails"]:
                try:
                    fetched_email = (row["email"]).lower()
                    if fetched_email == email.lower():
                        data = row
                        break
                except:
                    continue

            if data:
                print(self.formatted_str("SUCCESSFULLY!, get the data by email."))
                return data
            else:
                print(self.formatted_str("BAD!, email not found for the data OR email does not exists."))
                return False            
            
        except Exception as e:
            print(self.formatted_str(f"Unexpected Error Occured! \nError: {e}"))


    def verify_uniqness_of_value_by_key(self, key: str, value: str) -> str:
        try:
            key_lst = list()
            for row in self.READED_DATA["emails"]:
                try:
                    item = row[key]
                    key_lst.append(item.lower())
                except:
                    continue

            if value.lower() in key_lst:
                print(self.formatted_str(f"BAD!, '{key}' is matched to another or user may be enter same '{key}'."))
                return False
            
            return True
            
        except Exception as e:
            print(self.formatted_str(f"Unexpected Error Occured! \nError: {e}"))
   

    # ------------------- READ -------------------------------
    def read_data(self) -> dict:
        try:

            get = rq.get(self.SHEETY_END_POINT, headers=self.HEADERS)

            if self.check_status_code(get.status_code):
                print(self.formatted_str(f"SUCCESSFULLY!, Get the data from google sheet."))
                self.READED_DATA = get.json()
                return self.READED_DATA
        
            if get.status_code == 402:
                print(self.formatted_str("WORST, reach the free limit while reading data."))
                return

            print(self.formatted_str(f"FAILED!, To GET the data from google sheet."))
    
        except ConnectionError as ce:
            print(self.formatted_str(f"Connection Error Occured! \nDetails: {ce}"))

        except Exception as e:
            print(self.formatted_str(f"Unexpected Error Occured! \nError: {e}"))


    # ------------------- CREATE -------------------------------
    def add_new_row(self,
                    username, name: str, 
                    email: str, 
                    password: str) -> bool:
        '''
        Use Regex for validing email
        '''
        try:
            post = rq.post(
                url=self.SHEETY_END_POINT,
                headers=self.HEADERS,
                json={
                    "email": {
                        "username": username,
                        "name": name,
                        "email": email,
                        "password": password
                        }
                    }
                )
            
            if self.check_status_code(post.status_code):
                print(self.formatted_str(f"SUCCESSFULLY!, Add the data in google sheet."))
                return True
            
            if post.status_code == 402:
                print(self.formatted_str("WORST, reach the free limit while adding the data."))
                return
            
            print(self.formatted_str(f"FAILED!, To ADD the data in google sheet."))

        except ConnectionError as ce:
            print(self.formatted_str(f"Connection Error Occured! \nDetails: {ce}"))

        except Exception as e:
            print(self.formatted_str(f"Unexpected Error Occured! \nError: {e}"))


    # ------------------- UPDATE -------------------------------
    def update_data(self,
                   _id: int,
                   name: str = None,
                   username: str = None,
                   password: str = None,
                   is_name: bool = False,
                   is_username: bool = False,
                   is_password: bool = False) -> bool:
        try:

            put_data = {}

            if is_name:
                put_data["name"] = name
            
            elif is_username:
                put_data["username"] = username
            
            elif is_password:
                put_data["password"] = password

            put = rq.put(
                url=f"{self.SHEETY_END_POINT}/{_id}",
                json=put_data,
                headers=self.HEADERS)
            
            if self.check_status_code(put.status_code):
                # Update the readed data
                self.read_data()
                
                print(self.formatted_str(f"SUCCESSFULLY!, UPDATE the data in google sheet."))
                return True
            
            if put.status_code == 402:
                print(self.formatted_str("WORST, reach the free limit while updating data."))
                return

            
            print(self.formatted_str(f"FAILED!, To UPDATE the data in google sheet."))
            return False

        except ConnectionError as ce:
            print(self.formatted_str(f"Connection Error Occured! \nDetails: {ce}"))

        except Exception as e:
            print(self.formatted_str(f"Unexpected Error Occured! \nError: {e}"))


    # ------------------- DELETE -------------------------------
    def delete_row(self,
                   _id: int,) -> bool:
        try:

            delete = rq.delete(
                url=f"{self.SHEETY_END_POINT}/{_id}",
                headers=self.HEADERS)

            if self.check_status_code(delete.status_code):
                print(self.formatted_str(f"SUCCESSFULLY!, DELETE the data from google sheet."))
                
                # Update the readed data
                self.read_data()
                
                return True  

            if delete.status_code == 402:
                print(self.formatted_str("WORST, reach the free limit while deleting data."))
                return

            print(self.formatted_str(f"FAILED!, to DELETE the data from google sheet."))
            return False

        except ConnectionError as ce:
            print(self.formatted_str(f"Connection Error Occured! \nDetails: {ce}"))

        except Exception as e:
            print(self.formatted_str(f"Unexpected Error Occured! \nError: {e}"))


