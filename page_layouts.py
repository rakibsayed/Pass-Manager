from customtkinter import *
from tkinter import *

MIDFONT = ("Verdana", 12)
FRAME_BG = '#213140'
LABEL_FONT = ("Century Gothic", 13, "bold")
NOT_FOUND_FONT = ("Century Gothic", 40, "bold")
ENTRY_WIDTH = 600
ENTRY_FONT = ("Courier", 11, 'normal')
PLACEHOLDERS = {
    'search': 'Search by website or email address',
    'website': 'Enter the Website the email is associate to',
    'email': 'Enter the Email Address',
    'password': 'Enter the Password',
}


class HomePage(CTkFrame):

    def __init__(self, parent, app):
        CTkFrame.__init__(self, parent, fg_color=FRAME_BG)
        self.app = app
        # Storing the image as Instance Variable so that the reference of the image doesn't go down to zero
        self.img = PhotoImage(file='img/home.png')

        # Putting Image on the screen as a Label
        self.label = CTkLabel(self, image=self.img)
        self.label.pack(pady=40)

        # Button to Navigate to the Password Generator Page
        self.generate_pass = CTkButton(self, text='Generate Password', width=500, height=40, text_font=MIDFONT,
                                       cursor='hand2')
        self.generate_pass.pack(pady=20)
        self.manage_pass = CTkButton(self, text='Manage Your Password', width=500, height=40, text_font=MIDFONT,
                                     cursor='hand2')
        self.manage_pass.pack(pady=20)


# -------------------------------------------- PASS GENERATOR -------------------------------------------------------- #

class PassGenerator(CTkFrame):

    def __init__(self, parent, app):
        CTkFrame.__init__(self, parent, fg_color=FRAME_BG)

        self.app = app
        self.images = {}

        # Previous Page Button
        back_img = PhotoImage(file='img/button_assets/back.png')
        self.images['Back Image'] = back_img
        back_button = CTkButton(self, text="", image=back_img, hover_color=FRAME_BG, fg_color=FRAME_BG,
                                cursor='hand2')
        back_button.place(relx=0.02, rely=0.05)

        # Top Image
        contaienr_img = PhotoImage(file='img/pass-gen-img.png')
        self.images['Top Image'] = contaienr_img

        self.label = CTkLabel(self, image=contaienr_img)
        self.label.pack(pady=(40, 20))

        self.pass_entry = CTkEntry(self, width=600, height=50, fg_color='whitesmoke', text_color='black',
                                   text_font=("Ubuntu", 15, 'normal'))
        self.pass_entry.pack(pady=20)
        self.copy_button = CTkButton(self, text='Copy', fg_color='#7F8487', hover_color='#92A9BD',
                                     command=lambda: self.copy_button.configure(text='Copied'))
        self.copy_button.pack()

        self.filter_container = CTkFrame(self, fg_color=FRAME_BG)
        self.filter_container.pack(pady=35)
        self.pass_var = IntVar(self.filter_container)
        self.pass_var.set(10)

        self.range_slider = CTkSlider(self.filter_container, from_=6, to=16, width=500, variable=self.pass_var,
                                      cursor='hand2')

        self.range_slider.grid(row=0, column=0, columnspan=2, pady=(20, 10))
        self.range_label = CTkLabel(self, text='', fg='#2596be', text_color='yellowgreen')

        # Checkbox Variable to get the value wheather they are check or uncheck
        self.check_upper = StringVar()
        self.check_lower = StringVar()
        self.check_number = StringVar()
        self.check_symbols = StringVar()


# -------------------------------------------- PASS MANAGER SECTION -------------------------------------------------- #

class PassManager(CTkFrame):

    def __init__(self, parent, app):
        CTkFrame.__init__(self, parent, fg_color=FRAME_BG)

        self.app = app
        self.images = {}
        # Search Bar Container
        search_frame = CTkFrame(self, height=30)
        search_frame.grid(row=0, column=0, columnspan=3, pady=(20, 10), sticky=E)

        # Search Entry
        self.search_entry = CTkEntry(search_frame, width=ENTRY_WIDTH, text_font=ENTRY_FONT, text_color='grey',
                                     fg_color='whitesmoke', height=40)
        self.search_entry.insert(0, PLACEHOLDERS['search'])
        self.search_entry.grid(row=0, column=0, columnspan=3, sticky=E)
        self.search_entry.bind("<FocusIn>", self.search_foc_in)
        self.search_entry.bind("<FocusOut>", self.search_foc_out)

        # Search Button
        search_ = PhotoImage(file='img/button_assets/search_logo.png')
        self.images['search_icon'] = search_

        self.search_button = CTkButton(self, text='', width=30, image=search_, fg_color='whitesmoke',
                                       hover_color='whitesmoke', bg_color='whitesmoke', cursor='hand2')

        self.search_button.grid(in_=self.search_entry, row=0, column=0, sticky=E, padx=10)

        # Page Title Image (pack on screen as a label)
        img = PhotoImage(file='img/pass_manager.png')
        self.images['logo'] = img
        page_logo = CTkLabel(self, image=img)
        page_logo.grid(row=2, column=1, columnspan=2)

        # ------------------------------ LABELS -------------------------------- #
        fetch_label = CTkLabel(self, text='', text_font='Ariel 10 italic')
        fetch_label.grid(row=1, column=0, columnspan=3)

        # Website Label
        website_label = CTkLabel(self, text="Website:", text_font=LABEL_FONT)
        website_label.grid(row=3, column=0, sticky=E, padx=(40, 0))

        # Email Label
        email_label = CTkLabel(self, text="Email:", text_font=LABEL_FONT)
        email_label.grid(row=4, column=0, sticky=E, padx=(40, 0))

        # Pass Label
        pass_label = CTkLabel(self, text="Password:", text_font=LABEL_FONT)
        pass_label.grid(row=5, column=0, sticky=E, padx=(40, 0))

        # ---------------------------------- ENTRIES -----------------------------------

        self.website_entry = CTkEntry(self, width=ENTRY_WIDTH, text_font=ENTRY_FONT, text_color='grey',
                                      fg_color='whitesmoke', height=35)
        self.website_entry.insert(0, PLACEHOLDERS['website'])
        self.website_entry.grid(row=3, column=1, columnspan=2, sticky=W, pady=(20, 10))
        self.website_entry.bind("<FocusIn>", self.website_foc_in)
        self.website_entry.bind("<FocusOut>", self.website_foc_out)

        self.email_entry = CTkEntry(self, width=ENTRY_WIDTH, text_font=ENTRY_FONT, text_color='grey',
                                    fg_color='whitesmoke', height=35)
        self.email_entry.insert(0, PLACEHOLDERS['email'])
        self.email_entry.grid(row=4, column=1, columnspan=2, sticky=W, pady=10)
        self.email_entry.bind("<FocusIn>", self.email_foc_in)
        self.email_entry.bind("<FocusOut>", self.email_foc_out)

        self.password_entry = CTkEntry(self, width=ENTRY_WIDTH, text_font=ENTRY_FONT, text_color='grey',
                                       fg_color='whitesmoke', show='',
                                       height=35)
        self.password_entry.insert(0, PLACEHOLDERS['password'])
        self.password_entry.grid(row=5, column=1, columnspan=2, sticky=W, pady=10)
        self.password_entry.bind("<FocusIn>", self.pass_foc_in)
        self.password_entry.bind("<FocusOut>", self.pass_foc_out)

        # ------------------------------------- BUTTONS -------------------------------- #

        # Pass Range Slider
        self.pass_range = CTkSlider(self, from_=6, to=16, width=ENTRY_WIDTH, height=18)
        self.pass_range.grid(row=6, column=1, columnspan=2, sticky=W, pady=10)

        # Pass Generate Button
        self.pass_generate_btn = CTkButton(self, text='Generate a Random Password', text_font=LABEL_FONT,
                                           width=ENTRY_WIDTH,
                                           height=35, cursor='hand2')
        self.pass_generate_btn.grid(row=7, column=1, columnspan=2, sticky=W, pady=5)

        # Image for the Save Button
        add = PhotoImage(file='img/button_assets/add_to_database.png')
        self.images['add_icon'] = add

        # Save your Credentials
        self.add_to_database = CTkButton(self, image=add, text="", width=ENTRY_WIDTH, text_font=ENTRY_FONT,
                                         text_color='black', height=35, cursor='hand2')
        self.add_to_database.grid(row=8, column=0, columnspan=3, sticky=E, pady=(15, 0))
        self.added_label = CTkLabel(text="Successfully Added!", text_color="#3bceb1", text_font=ENTRY_FONT)

        # Password Hide and Show Toggle
        self.is_pass_visible = False
        hide_icon = PhotoImage(file='img/button_assets/hide.png')
        self.images['hide_icon'] = hide_icon

        self.show_hide_btn = Button(self, image=hide_icon, width=20, borderwidth=0, bg='whitesmoke',
                                    activebackground='whitesmoke',
                                    command=lambda: self.hide_password() if self.is_pass_visible else self.show_password())
        self.show_hide_btn.grid(in_=self.password_entry, row=0, column=0, sticky=E, padx=5)

    def search_foc_in(self, event):
        if self.search_entry.get() == PLACEHOLDERS["search"]:
            self.search_entry.delete(0, END)
        self.search_entry.configure(text_color='black')

    def search_foc_out(self, event):
        if self.search_entry.get() == '':
            self.search_entry.insert(0, PLACEHOLDERS["search"])
            self.search_entry.configure(text_color='grey')

    def website_foc_in(self, event):
        if self.website_entry.get() == PLACEHOLDERS["website"]:
            self.website_entry.delete(0, END)
        self.website_entry.configure(text_color='black')

    def website_foc_out(self, event):
        if self.website_entry.get() == '':
            self.website_entry.insert(0, PLACEHOLDERS["website"])
            self.website_entry.configure(text_color='grey')

    def email_foc_in(self, event):
        if self.email_entry.get() == PLACEHOLDERS["email"]:
            self.email_entry.delete(0, END)
        self.email_entry.configure(text_color='black')

    def email_foc_out(self, event):
        if self.email_entry.get() == '':
            self.email_entry.insert(0, PLACEHOLDERS["email"])
            self.email_entry.configure(text_color='grey')

    def pass_foc_in(self, event):
        if self.password_entry.get() == PLACEHOLDERS["password"]:
            self.password_entry.delete(0, END)
        self.password_entry.configure(text_color='black', show='*')

    def pass_foc_out(self, event):
        if self.password_entry.get() == '':
            self.password_entry.insert(0, PLACEHOLDERS["password"])
            self.password_entry.configure(text_color='grey', show='')

    def show_password(self):
        show_icon = PhotoImage(file='img/button_assets/show.png')
        self.images['show_icon'] = show_icon
        self.password_entry.configure(show='')
        self.show_hide_btn.config(image=show_icon)
        self.is_pass_visible = True

    def hide_password(self):
        self.password_entry.configure(show='*')
        self.show_hide_btn.config(image=self.images['hide_icon'])
        self.is_pass_visible = False


# ---------------------------------------------- RESULT PAGE  -------------------------------------------------------- #

class ResultPage(CTkFrame):

    def __init__(self, parent, app):
        CTkFrame.__init__(self, parent, fg_color=FRAME_BG)

        self.images = {}
        self.emails = []
        self.websites = []
        self.passwords = []
        # Images Instaance
        self.logo_img = None

        self.logo = CTkLabel(self, text="")
        self.logo.pack(pady=35)

        # Bottom Container
        self.bottom_frame = CTkFrame(self, width=800, height=300, fg_color=app.extra_color)
        self.bottom_frame.pack(side=BOTTOM, pady=(0, 50))
        self.bottom_frame.pack_propagate(False)
        # Result Container
        self.result_frame = CTkFrame(self.bottom_frame)
        self.result_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.email_label = CTkLabel(self.result_frame, text="Email:", text_font=MIDFONT, text_color='greenyellow')
        self.email_label.grid(row=1, column=0, padx=(50, 0), pady=(20, 0))

        self.pass_label = CTkLabel(self.result_frame, text="Password:", text_font=MIDFONT, text_color='greenyellow')
        self.pass_label.grid(row=2, column=0, padx=(50, 0), pady=(0, 20))

        self.email_found = CTkLabel(self.result_frame, text="", text_font=MIDFONT, text_color='white')
        self.email_found.grid(row=1, column=1, padx=(0, 50), pady=(20, 0))

        self.pass_found = CTkLabel(self.result_frame, text="", text_font=MIDFONT, text_color='white')
        self.pass_found.grid(row=2, column=1, padx=(0, 50), pady=(0, 20))

        copy_img = PhotoImage(file="img/button_assets/copy.png")
        self.images['copy_img'] = copy_img

        self.copy_button = CTkButton(self.result_frame, text="", image=copy_img, width=20,
                                     fg_color=self.email_found["background"],
                                     hover_color=self.email_found["background"], cursor='hand2')
        self.copy_button.place(relx=0.88, rely=0.5)

        self.choice_var = StringVar(master=self.bottom_frame)
        # self.choice_var.trace('w', chosen)
        self.result_comboBox = CTkOptionMenu(self.bottom_frame, variable=self.choice_var, text_font=MIDFONT)
        self.result_comboBox.pack(pady=(20, 0))

        # Not Found Label
        self.not_found = CTkLabel(self.bottom_frame, text="NOT FOUND", text_font=NOT_FOUND_FONT, text_color='red')
        self.not_found.pack(pady=(50, 0))


# -------------------------------------------- MESSAGE BOX ----------------------------------------------------------  #
class MessagBox(CTkToplevel):

    def __init__(self, app, message):
        CTkToplevel.__init__(self)

        self.app = app
        center_x = int(self.app.screen_width / 2 - 400 / 2)
        center_y = int(self.app.screen_height / 2 - 200 / 2)
        # Images Dict
        self.images = {}

        # Pop up Title and Size
        self.title('Testing')
        self.geometry(f'400x200+{center_x}+{center_y}')
        self.attributes('-topmost', 'true')  # this window will be top of the parent window as it should be
        self.app.bell()
        self.grab_set()

        # All Images
        error_img = PhotoImage(file='img/logo/message_info.png')
        self.images['error'] = error_img

        # Error Icon Image As Label
        error_label = CTkLabel(self, image=error_img, width=40, height=40)
        error_label.place(relx=0.5, rely=0.2, anchor=CENTER)

        # Message Container
        message_frame = CTkFrame(self, fg_color='#213140', width=400, height=50)
        message_frame.pack(side=BOTTOM)

        # Information Warning Label Text
        self.label = CTkLabel(self, text=message, text_font=('Ubuntu', 12, 'normal'))
        self.label.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.button = CTkButton(message_frame, text='Ok', width=70, height=30, command=self.destroy)
        self.button.place(relx=0.8, rely=0.2)

        self.resizable(False, False)
