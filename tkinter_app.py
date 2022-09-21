from customtkinter import *
from tkinter import *
from page_layouts import HomePage, PassManager, PassGenerator, ResultPage, MessagBox, FRAME_BG, PLACEHOLDERS
from database import DataBase
from pass_gen_algorithm import *
import pyperclip
import time
from threading import Thread

BG = '#213140'
WIN_WIDTH = 900
WIN_HEIGHT = 600
MESSAGE = {
    'SEARCH': "Please Enter Your Site/Email To Fetch The Credentials",
    'ERROR': "Please Don't Leave Any of the Fields Empty",
    '@DDRESS_MISS': "Please make sure you entered the email correctly ,\n"
                    "it suppose to have an address'@'"
}


class App(CTk):

    def __init__(self, *args, **kwargs):
        CTk.__init__(self, *args, **kwargs)
        self.extra_color = self.cget('background')
        # Window
        self.title("Pass Manager")
        self.config(bg=BG)
        self.resizable(False, False)

        # -------------------------------- WIN SIZE AND PLACE WINDOW AT THE CENTER OF THE SCREEN
        # ------------------------- # get the screen dimension
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        # find the center point
        center_x = int(self.screen_width / 2 - WIN_WIDTH / 2)
        center_y = int(self.screen_height / 2 - WIN_HEIGHT / 2)

        # set size of window and the position of the window to the center of the screen
        self.geometry(f'{WIN_WIDTH}x{WIN_HEIGHT}+{center_x}+{center_y}')

        # container to contain the Pages
        self.container = CTkFrame(self)
        self.container.pack(side='top', fill='both', expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # dictionary of Pages(Frames) you want to navigate to
        self.frames = {}

    #
    def navigate_to(self, page):
        layout_frame = self.frames[page]
        layout_frame.tkraise()


# -------------------------------- APP MAIN LOOP ---------------------------------------------------------- #

if __name__ == "__main__":
    # Iniatialize an instance of the App
    app = App()

    # Initialize an instance of the Starting Page
    home_page = HomePage(app.container, app)

    # Initialize an instance of the Pass Generator Page
    pass_generate_page = PassGenerator(app.container, app)

    #  Initialize an instance of the Manager Page
    pass_manager_page = PassManager(app.container, app)

    # Initializa an insatnce of Result Page
    result_page = ResultPage(app.container, app)

    # Database
    database = DataBase()

    app.frames = {
        'homepage': home_page,
        'pass_generator_page': pass_generate_page,
        'pass_manager_page': pass_manager_page,
        'result_page': result_page
    }
    # Store the Pages in App Dict
    home_page.grid(row=0, column=0, sticky='nsew')
    pass_manager_page.grid(row=0, column=0, sticky='nsew')
    pass_generate_page.grid(row=0, column=0, sticky='nsew')
    result_page.grid(row=0, column=0, sticky='nsew')

    # -------------------------------------- Creating Previuos Page Functionailty ----------------------------------- #

    # On Every Page Except HomePage
    for frame in (pass_manager_page, pass_generate_page, result_page):
        # Previous Page Button
        back_img = PhotoImage(file='img/button_assets/back.png')
        frame.images['Back Image'] = back_img
        back_button = CTkButton(frame, text="", image=back_img, hover_color=FRAME_BG, fg_color=FRAME_BG,
                                cursor='hand2')
        back_button.place(relx=0.02, rely=0.05)
        if frame == result_page:
            back_button.configure(command=lambda: app.navigate_to('pass_manager_page'))
        else:
            back_button.configure(command=lambda: app.navigate_to('homepage'))

    # -------------------------------------------- Starting Page -----------------------------------------------------#

    # Adding command on the Homepage Buttons
    home_page.generate_pass.configure(command=lambda: app.navigate_to('pass_generator_page'))
    home_page.manage_pass.configure(command=lambda: app.navigate_to('pass_manager_page'))

    # --------------------------------------- PASS GENERTAOR PAGE FUNCTIONALITY ------------------------------------- #

    def password_filter():
        division = 0
        filtered_keys = []

        pass_generate_page.pass_entry.delete(0, END)
        if pass_generate_page.check_upper.get() == 'on' or pass_generate_page.check_lower.get() == 'on' or \
                pass_generate_page.check_number.get() == 'on' or \
                pass_generate_page.check_symbols.get() == 'on':
            if pass_generate_page.check_upper.get() == 'on':
                division += 1
                filtered_keys.append(upper_case)
            if pass_generate_page.check_lower.get() == 'on':
                division += 1
                filtered_keys.append(lower_case)
            if pass_generate_page.check_number.get() == 'on':
                division += 1
                filtered_keys.append(numbers)
            if pass_generate_page.check_symbols.get() == 'on':
                division += 1
                filtered_keys.append(symbols)

            generate_pass(pass_range=pass_generate_page.range_slider.get(), all_keys=filtered_keys,
                          password_entry=pass_generate_page.pass_entry, division=division)
        else:
            filtered_keys = [upper_case, lower_case, numbers, symbols]
            generate_pass(pass_range=pass_generate_page.range_slider.get(), all_keys=filtered_keys,
                          password_entry=pass_generate_page.pass_entry)
        pass_generate_page.copy_button.configure(text="Copy")

    # ------------------------------------- Range Silder ---------------------------------------------#
    def leave(event):
        pass_generate_page.range_label.configure(text='')


    def slider_event(value):
        pass_generate_page.range_label.configure(text=math.floor(value))
        new_x = (value - 6) * 48 + 140
        pass_generate_page.range_label.place(x=new_x, y=320)


    # adding slider behaviour
    pass_generate_page.range_slider.configure(command=slider_event)
    pass_generate_page.range_slider.bind('<Leave>', leave)

    # ------------------------------------------- Checkbox --------------------------------------------------------- #
    upper_checkbox = CTkCheckBox(pass_generate_page.filter_container, width=20, height=20,
                                 text="upper case alphabet(A-Z)",
                                 variable=pass_generate_page.check_upper, onvalue="on", offvalue="off")
    upper_checkbox.deselect()
    upper_checkbox.grid(row=1, column=0, pady=5, sticky=W)

    lower_checkbox = CTkCheckBox(pass_generate_page.filter_container, width=20, height=20, text="lower case "
                                                                                                "alphabet(a-z)",
                                 variable=pass_generate_page.check_lower, onvalue="on", offvalue="off")
    lower_checkbox.deselect()
    lower_checkbox.grid(row=1, column=1, sticky=E)

    num_checkbox = CTkCheckBox(pass_generate_page.filter_container, width=20, height=20, text="numbers(1, 2, 3,...)",
                               variable=pass_generate_page.check_number, onvalue="on", offvalue="off")
    num_checkbox.deselect()
    num_checkbox.grid(row=2, column=0, sticky=W)

    symbols_checkbox = CTkCheckBox(pass_generate_page.filter_container, width=20, height=20, text="symbols(!, #, "
                                                                                                  "$, %,...)",
                                   variable=pass_generate_page.check_symbols, onvalue="on", offvalue="off")
    symbols_checkbox.deselect()
    symbols_checkbox.grid(row=2, column=1, sticky=E)

    pass_generate_page.range_slider.bind('<Leave>', leave)
    generate_pass_button = CTkButton(pass_generate_page.filter_container, width=550, height=40, text='Generate '
                                                                                                     'Password',
                                     fg_color='#EB4747', hover_color='#f54545', text_font='Ariel 15 normal',
                                     command=password_filter
                                     )
    generate_pass_button.grid(row=3, column=0, columnspan=2, pady=25)

    # ----------------------------------------- PASS MANAGER BUTTON FUNCTIONS --------------------------------------- #

    # ------------------------------------------ Find Result Function -------------------------------- #
    # This func also use Result Page Layout to show the found result
    def search(search_query):
        result_page.websites = []
        result_page.emails = []
        result_page.passwords = []
        result_page.not_found.lower()
        if search_query == "" or search_query == PLACEHOLDERS['search']:
            MessagBox(app, message=MESSAGE['SEARCH'])
        else:
            found_info = database.find_credential(search_query)
            if not found_info:
                result_page.logo_img = PhotoImage(file=f"img/logo/not_found.png")
                result_page.logo.configure(image=result_page.logo_img)
                result_page.not_found.tkraise()
                result_page.result_frame.lower()
                result_page.result_comboBox.lower()
            elif len(found_info) > 1:
                result_page.result_frame.lower()
                result_page.result_comboBox.lift()
                for data in found_info:
                    result_page.websites.append(data['website'])
                    result_page.emails.append(data['email'])
                    result_page.passwords.append(data['password'])

                result_page.choice_var = StringVar(master=result_page, value=f'Found {len(found_info)} Results')
                result_page.logo_img = PhotoImage(file=f"img/logo/email.png")
                result_page.logo.configure(image=result_page.logo_img)
                if search_query in result_page.emails:
                    result_page.result_comboBox.configure(variable=result_page.choice_var, values=result_page.websites,
                                                          command=selected)
                    print(result_page.websites)
                else:
                    result_page.result_comboBox.configure(variable=result_page.choice_var, values=result_page.emails,
                                                          command=selected)
            else:
                result_page.result_comboBox.lower()
                display_result(found_info[0]['website'], found_info[0]['email'], found_info[0]['password'])
            app.navigate_to('result_page')
            app.focus()
            pass_manager_page.search_entry.delete(0, END)
            pass_manager_page.search_entry.insert(0, PLACEHOLDERS['search'])
            pass_manager_page.search_entry.configure(text_color='grey')


    def display_result(website, email, password):
        result_page.result_frame.lift()
        result_page.logo_img = PhotoImage(file=f"img/logo/{website}.png")
        result_page.logo.configure(image=result_page.logo_img)
        result_page.email_found.configure(text=email)
        result_page.pass_found.configure(text=password)
        # Adding command To Result Page copy button to copy Password
        result_page.copy_button.configure(command=pyperclip.copy(password))


    def selected(event):
        selected_one = result_page.choice_var.get()
        if selected_one in result_page.websites:
            selected_password = result_page.passwords[result_page.websites.index(selected_one)]
            selected_email = result_page.emails[result_page.websites.index(selected_one)]
            display_result(website=selected_one, email=selected_email, password=selected_password)
        else:
            selected_password = result_page.passwords[result_page.emails.index(selected_one)]
            selected_website = result_page.websites[result_page.emails.index(selected_one)]
            display_result(website=selected_website, email=selected_one, password=selected_password)

        # -------------------------------------- Save Details Function ------------------------------- #


    def add_credential():
        # Check wheather any of the fileds are empty or not
        info = [pass_manager_page.website_entry.get(), pass_manager_page.email_entry.get(),
                pass_manager_page.password_entry.get()]
        for field in info:
            if len(field) == 0:
                MessagBox(app, message=MESSAGE['ERROR'])
                break
        else:
            if '@' not in pass_manager_page.email_entry.get():
                MessagBox(app, message=MESSAGE['@DDRESS_MISS'])
            else:
                database.save(info)
                pass_manager_page.website_entry.delete(0, END)
                pass_manager_page.email_entry.delete(0, END)
                pass_manager_page.password_entry.delete(0, END)
                app.focus()

                pass_manager_page.website_entry.insert(0, PLACEHOLDERS['website'])
                pass_manager_page.website_entry.configure(text_color='grey')

                pass_manager_page.email_entry.insert(0, PLACEHOLDERS['email'])
                pass_manager_page.email_entry.configure(text_color='grey')

                pass_manager_page.password_entry.insert(0, PLACEHOLDERS['password'])
                pass_manager_page.password_entry.configure(text_color='grey', show='')

                pass_manager_page.added_label.place(relx=0.57, rely=0.15)
                time.sleep(1.5)
                pass_manager_page.added_label.destroy()


    # BUttons
    pass_manager_page.pass_generate_btn.configure(command=lambda: [pass_manager_page.password_entry.delete(0, END),
                                                                   generate_pass(
                                                                       pass_range=pass_manager_page.pass_range.get(),
                                                                       all_keys=[upper_case, lower_case, numbers,
                                                                                 symbols],
                                                                       password_entry=pass_manager_page.password_entry)])

    # Use threading so the tkinter mainloop won't stop for the command function to finish
    pass_manager_page.search_button.configure(
        command=lambda: Thread(target=lambda: search(pass_manager_page.search_entry.get())).start() if True else None)

    pass_manager_page.add_to_database.configure(command=lambda: Thread(target=add_credential).start() if True else None)

    # Navigate to HomePage
    app.navigate_to('homepage')

    app.mainloop()
