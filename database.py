import gspread
from oauth2client.service_account import ServiceAccountCredentials

# YOU'WILL NEED TO US GOOGLE CLOUD ACCCOUNT
SCOPE = ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive.file',
         'https://www.googleapis.com/auth/drive']
CREDS = ServiceAccountCredentials.from_json_keyfile_name('python_sheet_api_key.json', SCOPE)
# GET YOUR OWN API KEY ON GOOGLE CLOUD Console BY CREATING NEW PRPOJECT OR USE THE EXISTING ONE


class DataBase:
    def __init__(self):
        self.client = gspread.authorize(CREDS)
        self.database = self.client.open("Database_Python").worksheet('pass_manager')
        self.records = self.database.get_all_records()
        self.email_menu = [item['Email'] for item in self.records]
        self.website_menu = [item['Website'] for item in self.records]
        self.result = None

    def save(self, input_entries):
        website = input_entries[0]
        email = input_entries[1]
        password = input_entries[2]

        # Reading old data
        row = len(self.records) + 2
        # Put the data in the database
        self.database.update_cell(row, 1, website.lower())
        self.database.update_cell(row, 2, email.lower())
        self.database.update_cell(row, 3, password)

# --------------------------------------------- FIND PASSWORD -------------------------------------------------------- #

    def find_credential(self, search_query):
        self.result = self.database.findall(search_query.lower())
        found_result = []
        if len(self.result) > 0:
            for data in self.result:
                temp_dict = {}
                found_list = self.database.row_values(data.row)
                temp_dict['website'] = found_list[0]
                temp_dict['email'] = found_list[1]
                temp_dict['password'] = found_list[2]
                found_result.append(temp_dict)
            return found_result
        else:
            return self.result
