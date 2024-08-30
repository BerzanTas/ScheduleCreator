import sys, os, re
import keyring, configparser
from PySide6.QtCore import QSize, Qt, QEvent, QTimer
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QFormLayout, QLabel,
    QLineEdit, QCheckBox, QPushButton, QHBoxLayout, QStackedWidget,
    QToolTip, QFrame, QSlider
)
from PySide6.QtGui import (QPainter, QPixmap, QFont, QFontDatabase, QGuiApplication,
                           QPalette, QColor, QIcon, QLinearGradient, QAction, QBrush
)
from database import Login, Register, EmployeeData

class LoginWindow(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.autologin = False
        # if user choosed 'remember me' than automaticly change to main program without creating LoginWindow UI
        if self.auto_login():
            self.autologin = True
        else:
            self.load_custom_font()
            self.setup_ui()

    def setup_ui(self):
        # main layout for the login window
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)  

        # container for the login form
        form_container = QWidget()
        form_container.setFixedSize(340, 460)
        form_container.setStyleSheet("""
            QWidget#form_container {
                background-color: rgba(152, 111, 25, 0.6);
                border-radius: 20px;
            }
            QLineEdit {
                font-size: 14px;
                background-color: rgba(255, 255, 255, 0.3);
                border-radius: 8px;
                padding: 5px;
                color: black;
            }
            QPushButton {
                background-color: black;
                color: #f1b903;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: transparent;
                border: 2px solid black;
                color: black;
            }
            QPushButton:focus {
                outline: none;
            }
        """)
        form_container.setObjectName("form_container")

        # layout for form elements
        form_layout = QFormLayout()
        form_layout.setContentsMargins(0, 0, 0, 0)  
        form_layout.setSpacing(10)  

        # login label setup
        login_label = QLabel("Log In")
        login_font = QFont("Now", 31)
        login_font.setHintingPreference(QFont.HintingPreference.PreferNoHinting)
        login_label.setFont(login_font)
        login_label.setStyleSheet("""
                                  color: black;
                                  padding-top: 40px;
                                  padding-bottom: 30px;
                                  """)
        login_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # email input field setup
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("E-mail")
        self.email_input.setFixedSize(QSize(240,34))
        self.email_input.setStyleSheet("color: black;")

        # password input field setup
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setFixedSize(QSize(240,34))
        
        # setting placeholder and text color for email and password inputs
        palette = self.email_input.palette()
        palette.setColor(QPalette.PlaceholderText, QColor(152, 111, 25))  
        palette.setColor(QPalette.Text, Qt.black)  
        self.email_input.setPalette(palette)
        self.password_input.setPalette(palette)

        # small font for additional labels
        small_font = QFont("Now", 8)
        small_font.setHintingPreference(QFont.HintingPreference.PreferNoHinting)

        # forgot password label setup
        forgot_password_label = QLabel('<a href="#" style="text-decoration:none; color: black; outline: none;">Forgot your password?</a>')
        forgot_password_label.setFont(small_font)
        forgot_password_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        forgot_password_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        forgot_password_label.setOpenExternalLinks(False)
        forgot_password_label.linkActivated.connect(self.forgot_password_clicked)

        # remember me checkbox setup
        self.remember_me_checkbox = QCheckBox("Remember me")
        self.remember_me_checkbox.setCursor(Qt.CursorShape.PointingHandCursor)
        self.remember_me_checkbox.setStyleSheet("""
                                                QCheckBox {
                                                    color: black;
                                                    font-size: 15px;
                                                }
                                                QCheckBox::indicator {
                                                    width: 20px;
                                                    height: 20px;
                                                    background-color: transparent;
                                                    border: 2px solid black;
                                                    border-radius: 5px;
                                                }
                                                QCheckBox::indicator:checked {
                                                    background: url(img/checkmark.png) no-repeat center center;
                                                }
        """)

        # button font setup
        button_font = QFont("Now", 8)
        button_font.setHintingPreference(QFont.HintingPreference.PreferNoHinting)

        # login button setup
        self.login_button = QPushButton("LOG IN")
        self.login_button.setFixedSize(155, 45)
        self.login_button.setFont(button_font)
        self.login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_button.clicked.connect(self.handle_login)
        centered_button_layout = QVBoxLayout()
        centered_button_layout.addWidget(self.login_button)
        centered_button_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # register label setup (link to switch to register window)
        self.register_label = QLabel('<a href="#" style="color: black;">First time? Register</a>')
        self.register_label.setFont(small_font)
        self.register_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.register_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.register_label.setOpenExternalLinks(False) 

        # spacer widget for spacing between elements
        spacer_widget = QWidget()  
        spacer_widget.setFixedHeight(20)

        # layout for center-aligned fields (email, password, buttons, etc.)
        centered_fields_layout = QVBoxLayout()
        centered_fields_layout.addWidget(login_label)
        centered_fields_layout.addWidget(self.email_input)
        centered_fields_layout.addWidget(self.password_input)
        centered_fields_layout.addWidget(forgot_password_label)
        centered_fields_layout.addWidget(self.remember_me_checkbox)
        centered_fields_layout.addWidget(spacer_widget)
        centered_fields_layout.addWidget(spacer_widget)
        centered_fields_layout.addLayout(centered_button_layout)
        centered_fields_layout.addWidget(self.register_label)
        centered_fields_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # adding centered fields layout to form layout
        form_layout.addRow(centered_fields_layout)
        form_container.setLayout(form_layout)

        # horizontal layout to center the form container
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addStretch()
        horizontal_layout.addWidget(form_container)
        horizontal_layout.addStretch()

        # vertical layout for overall placement in the window
        vertical_layout = QVBoxLayout()
        vertical_layout.setContentsMargins(0, 100, 0, 0)  
        vertical_layout.addLayout(horizontal_layout)  

        # adding vertical layout to main layout
        main_layout.addLayout(vertical_layout)

        self.setLayout(main_layout)

    def handle_login(self):
        """Handles the login logic"""
        email = self.email_input.text()
        password = self.password_input.text()

        if email and password:
            # instantiate login and connect with given credentials
            login = Login()
            status = login.connect(email, password)

            if status == 200 and self.remember_me_checkbox.isChecked():
                self.save_login_info(email, password)
            #except:
            #    print("Unable to connect to database!")
    
    # if user selects 'remember me' than this method will be runned
    def save_login_info(self, email, password):
        """Save login credentials using keyring"""
        # save password using keyring
        keyring.set_password("schedule_creator", email, password)
        print("Login info saved in keyring.")

        # save email address in ini file
        with open("user_config.ini", "w") as configfile:
            configfile.write(f"[USER]\nEmail={email}\n")

    def auto_login(self):
        """Automaticly login the user from saved credentials"""
        config_file = "user_config.ini"
        if os.path.exists(config_file):
            config = configparser.ConfigParser()
            config.read(config_file)

            if 'USER' in config:
                email = config['USER']['Email']

                # Pobierz hasło z keyring
                password = keyring.get_password("schedule_creator", email)
                if password:
                    login = Login()
                    login.connect(email, password)
                    print(f"Automatically logged in as {email}")
                    return True
                else:
                    print("No password found in keyring.")
                    return False

    def forgot_password_clicked(self):
        """Handle 'Forgot your password?' click"""
        pass

    def paintEvent(self, event):
        """Custom background painting for the login window"""
        painter = QPainter(self)
        pixmap = QPixmap("img/schedulecreatorbg.png")
        painter.drawPixmap(self.rect(), pixmap)

    def load_custom_font(self):
        """Load a custom font from file"""
        font_id = QFontDatabase.addApplicationFont("img/Now.otf")
        if font_id != -1:
            print("Custom font loaded successfully.")
        else:
            print("Failed to load custom font.")

class RegisterWindow(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        # window settings
        self.setWindowTitle("Register")
        self.load_custom_font()
        self.setup_ui()
        self.registration = Register()

    def setup_ui(self):
        # main layout for the register window
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)  

        # container for the register form
        form_container = QWidget()
        form_container.setFixedSize(340, 460)
        form_container.setStyleSheet("""
            QWidget#form_container {
                background-color: rgba(152, 111, 25, 0.6);
                border-radius: 20px;
            }
            QLineEdit {
                font-size: 14px;
                background-color: rgba(255, 255, 255, 0.3);
                border-radius: 8px;
                padding: 5px;
                color: black;
            }
            QPushButton:focus {
                outline: none;
            }
        """)
        form_container.setObjectName("form_container")

        # layout for form elements
        form_layout = QFormLayout()
        form_layout.setContentsMargins(0, 0, 0, 0)  
        form_layout.setSpacing(10)  

        # register label setup
        register_label = QLabel("Register")
        register_font = QFont("Now", 31)
        register_font.setHintingPreference(QFont.HintingPreference.PreferNoHinting)
        register_label.setFont(register_font)
        register_label.setStyleSheet("""
                                    color: black;
                                    padding-top: 40px;
                                    padding-bottom: 30px;
                                    """)
        register_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # name input field setup
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFixedSize(QSize(240,34))
        self.username_input.setStyleSheet("color: black;")
        self.username_input.editingFinished.connect(self.check_username)

        # email input field setup
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("E-mail")
        self.email_input.setFixedSize(QSize(240,34))
        self.email_input.setStyleSheet("color: black;")
        self.email_input.editingFinished.connect(self.check_email)

        # password input field setup
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setFixedSize(QSize(240,34))
        self.password_input.editingFinished.connect(self.check_password)

        # confirm password input field setup
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setPlaceholderText("Confirm Password")
        self.confirm_password_input.setFixedSize(QSize(240,34))
        self.confirm_password_input.editingFinished.connect(self.confirm_password)

        # install event filters for all input fields to handle mouse hover events
        self.username_input.installEventFilter(self)
        self.email_input.installEventFilter(self)
        self.password_input.installEventFilter(self)
        self.confirm_password_input.installEventFilter(self)

        palette = self.username_input.palette()
        palette.setColor(QPalette.PlaceholderText, QColor(152, 111, 25))  
        palette.setColor(QPalette.Text, Qt.black)  
        self.username_input.setPalette(palette)
        self.email_input.setPalette(palette)
        self.password_input.setPalette(palette)
        self.confirm_password_input.setPalette(palette)

        button_font = QFont("Now", 8)
        button_font.setHintingPreference(QFont.HintingPreference.PreferNoHinting)

        # register button setup
        register_button = QPushButton("REGISTER")
        register_button.setFixedSize(155, 45)
        register_button.setFont(button_font)
        register_button.setCursor(Qt.CursorShape.PointingHandCursor)
        register_button.clicked.connect(self.handle_registration)
        register_button.setStyleSheet("""
                                    QPushButton {
                                        background-color: black;
                                        color: #f1b903;
                                        border-radius: 20px;
                                    }
                                    QPushButton:hover {
                                        background-color: transparent;
                                        border: 2px solid black;
                                        color: black;
                                    }""")

        # layout for center-aligned register button
        centered_button_layout = QVBoxLayout()
        centered_button_layout.addWidget(register_button)
        centered_button_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.go_back_button = QPushButton(self)
        pixmap = QPixmap("img/arrow.png")
        icon = QIcon(pixmap)
        self.go_back_button.setIcon(icon)
        self.go_back_button.setIconSize(QSize(50,50))
        self.go_back_button.setFixedSize(50,50)
        self.go_back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.go_back_button.setStyleSheet("""
                                    QPushButton {
                                        background-color: transparent;
                                        border: none;
                                    }
                                    """)

        spacer_widget = QWidget()
        spacer_widget.setFixedHeight(20)
        
        # layout for center-aligned fields (name, email, password, etc.)
        centered_fields_layout = QVBoxLayout()
        centered_fields_layout.addWidget(register_label)
        centered_fields_layout.addWidget(self.username_input)
        centered_fields_layout.addWidget(self.email_input)
        centered_fields_layout.addWidget(self.password_input)
        centered_fields_layout.addWidget(self.confirm_password_input)
        centered_fields_layout.addWidget(spacer_widget)
        centered_fields_layout.addLayout(centered_button_layout)
        centered_fields_layout.addWidget(self.go_back_button)
        centered_fields_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # adding centered fields layout to form layout
        form_layout.addRow(centered_fields_layout)
        form_container.setLayout(form_layout)

        # horizontal layout to center the form container
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addStretch()
        horizontal_layout.addWidget(form_container)
        horizontal_layout.addStretch()

        # vertical layout for overall placement in the window
        vertical_layout = QVBoxLayout()
        vertical_layout.setContentsMargins(0, 100, 0, 0)  
        vertical_layout.addLayout(horizontal_layout)  

        # adding vertical layout to main layout
        main_layout.addLayout(vertical_layout)

        self.setLayout(main_layout)

    def check_username(self):
        """Validate the username to ensure it contains at least 3 letters, optionally with digits."""
        text = self.username_input.text()

        # regex to match at least 3 letters and allow digits
        if re.fullmatch(r'^(?=(?:[^a-zA-Z]*[a-zA-Z]){3})[a-zA-Z0-9]*$', text):
            self.username_input.setStyleSheet("border: 1px solid green;")
            self.username_input.setToolTip("")

            # check if username already exists
            if self.registration.check_if_exists("username", text):
                self.username_input.setStyleSheet("border: 1px solid red;")
                self.username_input.setToolTip("Username already exists.")
                return False
            
            return True
        else:
            self.username_input.setStyleSheet("border: 1px solid red;")
            self.username_input.setToolTip("Username must contain at least 3 letters!")
            return False

    def check_email(self):
        # e-mail validation
        text = self.email_input.text()

        if re.fullmatch(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', text):
            self.email_input.setStyleSheet("border: 1px solid green;")
            self.email_input.setToolTip("")

            if self.registration.check_if_exists("email", text):
                self.email_input.setStyleSheet("border: 1px solid red;")
                self.email_input.setToolTip("E-mail already in use.")
                return False
            
            return True
        else:
            self.email_input.setStyleSheet("border: 1px solid red;")
            self.email_input.setToolTip("Enter a valid email address (e.g., example@domain.com).")
            return False

    def check_password(self):
        # password validation
        text = self.password_input.text()

        if re.fullmatch(r'(?=.*[a-z])(?=.*[A-Z])[A-Za-z0-9\d@$!%*?&.,]{8,}$', text):
            self.password_input.setStyleSheet("border: 1px solid green;")
            self.password_input.setToolTip("")
            return True
        else:
            self.password_input.setStyleSheet("border: 1px solid red;")
            self.password_input.setToolTip("Password must be:\n- at least 8 characters,\n- one uppercase,\n- one lowercase.")
            return False

    def confirm_password(self):
        # confirm password
        password1 = self.password_input.text()
        password2 = self.confirm_password_input.text()

        if password1 == password2:
            self.confirm_password_input.setStyleSheet("border: 1px solid green;")
            self.confirm_password_input.setToolTip("")
            return True
        else:
            self.confirm_password_input.setStyleSheet("border: 1px solid red;")
            self.confirm_password_input.setToolTip("Passwords are different.")
            return False
    
    def handle_registration(self):
        """Handles the registration logic"""
        username = self.username_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        all_fields_correct = False

        # all_fields_correct == True if all the fields are correctly filled
        if self.check_username():
            if self.check_email():
                if self.check_password():
                    if self.confirm_password():
                        all_fields_correct = True

        if all_fields_correct:
            # instantiate registration and connect with given credentials
            status = self.registration.register(username, email, password)
            if status == 201:
                self.account_created()
        
    def account_created(self):
        # delete text in fields
        self.username_input.clear()
        self.username_input.setStyleSheet("border: none;")

        self.email_input.clear()
        self.email_input.setStyleSheet("border: none;")

        self.password_input.clear()
        self.password_input.setStyleSheet("border: none;")

        self.confirm_password_input.clear()
        self.confirm_password_input.setStyleSheet("border: none;")

        # creating a success notification
        self.notification_label = QLabel("Account successfuly created!", self)
        self.notification_label.setStyleSheet("""
            background-color: green;
            border: 1px solid green;
            color: white;
            padding: 5px;
            border-radius: 5px;
        """)
        self.notification_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.notification_label.setGeometry(self.width() - 225, 25, 200, 50)
        self.notification_label.show()

        # set the timer for notification
        QTimer.singleShot(3000, self.notification_label.hide)
    
    def eventFilter(self, source, event):
        """Handle mouse hover events to show tooltip for invalid inputs."""
        if event.type() == QEvent.HoverEnter:
            # Pokaż tooltipa, jeśli dane są niepoprawne
            if source == self.username_input:
                QToolTip.showText(source.mapToGlobal(event.pos()), source.toolTip(), source)
            elif source == self.email_input:
                QToolTip.showText(source.mapToGlobal(event.pos()), source.toolTip(), source)
            elif source == self.password_input and not re.fullmatch(r'(?=.*[a-z])(?=.*[A-Z])[A-Za-z\d@$!%*?&]{8,}$', source.text()):
                QToolTip.showText(source.mapToGlobal(event.pos()), source.toolTip(), source)
            elif source == self.confirm_password_input and self.confirm_password_input.text() != self.password_input.text():
                QToolTip.showText(source.mapToGlobal(event.pos()), source.toolTip(), source)
        return super().eventFilter(source, event)

    def paintEvent(self, event):
        """Custom background painting for the register window"""
        painter = QPainter(self)
        pixmap = QPixmap("img/schedulecreatorbg.png")
        painter.drawPixmap(self.rect(), pixmap)

    def load_custom_font(self):
        """Load a custom font from file"""
        font_id = QFontDatabase.addApplicationFont("img/Now.otf")
        if font_id != -1:
            print("Custom font loaded successfully.")
        else:
            print("Failed to load custom font.")

class MainProgram(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.load_custom_font()
        
        # creating fonts
        self.button_font = QFont("Now", 13)
        self.button_font.setHintingPreference(QFont.HintingPreference.PreferNoHinting)
        self.head_font = QFont("Now", 14)
        self.head_font.setHintingPreference(QFont.HintingPreference.PreferNoHinting)
        self.paragraph_font = QFont("Now", 12)
        self.paragraph_font.setHintingPreference(QFont.HintingPreference.PreferNoHinting)
        self.slider_font = QFont("Now", 11)
        self.slider_font.setHintingPreference(QFont.HintingPreference.PreferNoHinting)

        self.setup_ui()
        

    def setup_ui(self):
        # create main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Create and add the menu bar
        menubar_widget = self.create_menubar()

        self.stacked_widget = QStackedWidget(self)

        #if not EmployeeData.employeelistexists
        self.no_db_window = QWidget()
        self.no_db_window.setLayout(self.no_database_layout())
        
        self.database_window = QWidget(self)
        self.database_window.setLayout(self.create_database_layout())

        self.schedule_window = QWidget(self)
        self.schedule_window.setLayout(self.create_schedule_layout())

        self.stacked_widget.addWidget(self.no_db_window)
        self.stacked_widget.addWidget(self.database_window)
        self.stacked_widget.addWidget(self.schedule_window)

        main_layout.addWidget(menubar_widget)
        main_layout.addWidget(self.stacked_widget)

        # Set the main layout to the widget
        self.setLayout(main_layout)
    
    def create_menubar(self):
        # create a layout for the menubar
        menubar_layout = QHBoxLayout()
        menubar_layout.setContentsMargins(80, 0, 80, 0)
        menubar_layout.setAlignment(Qt.AlignTop)

        # Create buttons for the menubar
        database_button = QPushButton("Database", self)
        database_button.clicked.connect(self.show_database_layout)
        schedule_button = QPushButton("Schedule", self)
        schedule_button.clicked.connect(self.show_schedule_layout)
        self.logout_button = QPushButton("Log out", self)

        for button in [database_button, schedule_button, self.logout_button]:
            button.setStyleSheet("""
                                 QPushButton {
                                    color: black;
                                    border: none;
                                    padding: 5px 10px;
                                    outline: none;
                                 }
                                 QPushButton:hover {
                                    border: 1px solid black;
                                    border-radius: 10px;
                                 }
                                 """)
            button.setFont(self.button_font)
            button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.logout_button.clicked.connect(self.logout)

        # create and add logo
        logo_label = QLabel(self)
        logo_label.setFixedSize(235, 115)
        logo_pixmap = QPixmap("img/logo.png")
        logo_label.setPixmap(logo_pixmap.scaled(logo_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        # handle left side of the logo
        left_layout = QHBoxLayout()
        left_layout.addWidget(database_button)
        left_layout.addSpacing(50)
        left_layout.addWidget(schedule_button)
        left_layout.addStretch()

        # handle rigth side of the logo
        right_layout = QHBoxLayout()
        right_layout.addStretch()
        right_layout.addWidget(self.logout_button)
        
        # add the logout button to the right
        menubar_layout.addLayout(left_layout)
        menubar_layout.addStretch()
        menubar_layout.addWidget(logo_label)
        menubar_layout.addStretch()
        menubar_layout.addLayout(right_layout)

        # create a widget to hold the toolbar layout
        menubar_widget = QWidget(self)
        menubar_widget.setLayout(menubar_layout)
        menubar_widget.setStyleSheet("background-color: transparent;")

        return menubar_widget
    
    def no_database_layout(self):
        """
            The layout that the user will see after first login after registering
            or first login after deleting database. User will be asked to create
            a database.
        """
        first_login_layout = QVBoxLayout()
        first_login_layout.setContentsMargins(0,0,0,0)
        first_login_layout.setAlignment(Qt.AlignTop)
        
        first_login_widget = QWidget(self)
        first_login_widget.setFixedSize(500, 400)
        first_login_widget.setStyleSheet("""
                                         background-color: rgba(255, 255, 255, 0.15);
                                         border-radius: 20px;
                                         """)

        # creating labels
        


        head_label = QLabel("Hmm...\nSeems like you don't have a database!")
        head_label.setFont(self.head_font)
        head_label.setStyleSheet("""
                                 color: black;
                                 background: none;
                                 padding-top: 70px;
                                 """)
        
        paragraph_label = QLabel("To use this program, you need a list of your employees with their working hours. Worry not! It is a very easy task, just click the button below:)")
        paragraph_label.setFont(self.paragraph_font)
        paragraph_label.setStyleSheet("""
                                 color: black;
                                 background: none;
                                 padding: 0px 60px;
                                 """)
        
        # wrap the text so it is not in one line
        paragraph_label.setWordWrap(True) 

        # center the labels
        head_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        paragraph_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # create button directing to Database window
        create_database_button = QPushButton("Create!", self)
        create_database_button.setFont(self.button_font)
        create_database_button.setCursor(Qt.CursorShape.PointingHandCursor)
        create_database_button.setFixedSize(200, 50)
        create_database_button.setStyleSheet("""
                                             QPushButton {
                                                color: #da8641;
                                                border: none;
                                                padding: 5px 10px;
                                                outline: none;
                                                background-color: black;
                                                border-radius: 10px;
                                            }
                                            QPushButton:hover {
                                                color: black;
                                                background-color: #da8641;
                                                border: 1px solid black;
                                            }
                                             """)
        create_database_button.clicked.connect(self.show_database_layout)

        # centering the button
        centered_button_layout = QVBoxLayout()
        centered_button_layout.addWidget(create_database_button)
        centered_button_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        first_login_layout.addWidget(head_label)
        first_login_layout.addSpacing(30)
        first_login_layout.addWidget(paragraph_label)
        first_login_layout.addSpacing(50)
        first_login_layout.addLayout(centered_button_layout)

        first_login_widget.setLayout(first_login_layout)

        # horizontal layout to center the form container
        centered_widget = self.center_widget(first_login_widget)
        centered_widget.setContentsMargins(0, 100, 0, 0)
        
        return centered_widget
    
    def create_database_layout(self):
        """Layout for creating and editing employee database"""

        def show_add_emp():
            stacked_database_widget.setCurrentWidget(form_widget)
            employee_list_button.setStyleSheet("""
                                              color: black;
                                              background-color: transparent;
                                              border-radius: 0px;
                                              """)
            add_employee_button.setStyleSheet("""
                                               color: #df9233;
                                               background-color: black;
                                               margin-right: -10px;
                                               border-radius: 0px;
                                               """)

        def show_emp_list():
            add_employee_button.setStyleSheet("""
                                              color: black;
                                              background-color: transparent;
                                              border-radius: 0px;
                                              """)
            employee_list_button.setStyleSheet("""
                                               color: #df9233;
                                               background-color: black;
                                               margin-left: -10px;
                                               border-radius: 0px;
                                               """)
            stacked_database_widget.setCurrentWidget(emp_list_widget)
        
        def update_value_label():
            value = slider.value()
            if value < 2:
                slider.setValue(2)
                value = 2

            # map the slider value to the corresponding value from the list
            if value != 5:
                selected_value = values[value - 1]
                value_label.setText(f"{selected_value:.2f}")

                # calculate the position of the handle
                slider_pos = slider.pos()
                slider_width = slider.width()

                # calculate the relative position of the handle
                slider_range = slider.maximum() - slider.minimum()
                relative_pos = (slider.value() - slider.minimum()) / slider_range

                # move the label above the handle
                handle_x = slider_pos.x() + relative_pos * slider_width
                value_label.move(handle_x - value_label.width() // 2, slider_pos.y() - 30)
            else:
                value_label.setText("")



        # QStackedWidget for changing layout between adding employee and list of employees
        stacked_database_widget = QStackedWidget()

        database_layout = QVBoxLayout()
        database_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        database_layout.setSpacing(0)

        database_widget = QWidget(self)
        database_widget.setFixedSize(560, 584)
        database_widget.setStyleSheet("""
                                      background: none;
                                      """)
        database_layout.setContentsMargins(0,4,0,0)
        
        # layout for buttons switching between adding an employee and list of employees
        database_switch = QHBoxLayout()
        database_switch.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        database_switch.setSpacing(0)

        add_employee_button = QPushButton("ADD EMPLOYEE")
        employee_list_button = QPushButton("EMPLOYEE LIST")

        for button in [add_employee_button, employee_list_button]:
            button.setFixedSize(200,60)
            button.setFont(self.button_font)

        add_employee_button.setStyleSheet("""
                                            color: #df9233;
                                            background-color: black;
                                            margin-right: -10px;
                                            border-radius: 0px;
                                          """)
        add_employee_button.clicked.connect(show_add_emp)
        employee_list_button.setStyleSheet("""
                                            color: black;
                                            background-color: transparent;
                                            border-radius: 0px;
                                           """)
        employee_list_button.clicked.connect(show_emp_list)

        database_switch.addWidget(add_employee_button)
        database_switch.addWidget(employee_list_button)

        # creating a line in between two buttons
        line = QFrame(database_widget)
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("""
                           color: black;
                           background-color: black;
                           """)
        line.setFixedSize(4,70)
        line.move((database_widget.width()/2)-4, 0)
        line.raise_()

        # creating employee add form
        form_layout = QVBoxLayout()
        form_layout.setSpacing(30)
        form_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        form_widget = QWidget()
        form_widget.setFixedSize(560, 520)
        form_widget.setStyleSheet("""
                                    background-color: rgba(0, 0, 0, 0.15);
                                    border-radius: 15px;
                                """)
        form_widget.setLayout(form_layout)

        # creating QLineEdits for employee id and employee name
        emp_id = QLineEdit()
        emp_id.setPlaceholderText("Employee ID")
        emp_id.setFont(self.button_font)

        emp_name = QLineEdit()
        emp_name.setPlaceholderText("Employee name")
        emp_name.setFont(self.button_font)

        # setting placeholder and text color for email and password inputs
        palette = emp_id.palette()
        palette.setColor(QPalette.PlaceholderText, Qt.black)  
        palette.setColor(QPalette.Text, Qt.black)

        emp_id.setPalette(palette)
        emp_name.setPalette(palette)

        # new layout to group input fields
        input_field_center = QVBoxLayout()

        for input_field in [emp_id, emp_name]:
            input_field.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            input_field.setFixedSize(240,45)
            input_field.setStyleSheet("""
                                      background-color: transparent;
                                      border: 1px solid black;
                                      border-radius: 10px;
                                      """)
            # add QLineEdit to new layout
            input_field_center.addWidget(input_field)

        # new layout to horizontaly center the input fields
        input_field_center_horizontal = QHBoxLayout()
        input_field_center_horizontal.addStretch()
        input_field_center_horizontal.addLayout(input_field_center)
        input_field_center_horizontal.addStretch()
        input_field_center_horizontal.setContentsMargins(0,50,0,30)

        # creating a slider for working time
        slider_layout = QHBoxLayout()
        slider_layout_v = QVBoxLayout()
        
        slider = QSlider(Qt.Horizontal)
        slider.setFixedWidth(350)
        
        values = [0, 0.25, 0.5, 0.75, 1] # allowed values for slider

        # slider settings
        slider.setMinimum(1)
        slider.setMaximum(5)
        slider.setValue(5)
        slider.setTickInterval(1)
        slider.valueChanged.connect(update_value_label)

        # changing slider style
        slider.setStyleSheet("""
                             QSlider {
                                background: none;
                             }
                            QSlider::groove:horizontal {
                                height: 2px;
                                background: black;
                            }
                            QSlider::handle:horizontal {
                                background: black;
                                width: 15px;
                                height: 15px;
                                border-radius: 7px;
                                margin: -7px 0; /* to center the handle */
                            }
                            QSlider::sub-page:horizontal {
                                background: black;
                                height: 2px;
                            }
                            """)
        
        # adding label on left and right side of the slider and the bottom label
        label_left = QLabel("0")
        label_right = QLabel("1")
        slider_label = QLabel("Working Time")
        
        for label in [label_left, label_right, slider_label]:
            label.setFont(self.slider_font)
            label.setStyleSheet("""
                                background: none;
                                color: black;
                                """)
            label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # grouping left/right labels with slider
        slider_layout.addStretch()
        slider_layout.addWidget(label_left)
        slider_layout.addWidget(slider)
        slider_layout.addWidget(label_right)
        slider_layout.addStretch()
        slider_layout.setSpacing(5)

        # value label above the slider that will follow the handle
        value_label = QLabel(form_widget)
        value_label.setFixedSize(50, 20)
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setFont(self.slider_font)
        value_label.setStyleSheet("color: black; background: none;")

        # change value_label position to be alway on top of handle
        update_value_label()

        # grouping slider with bottom label
        slider_layout_v.addLayout(slider_layout)
        slider_layout_v.addWidget(slider_label)
        slider_layout_v.setSpacing(0)

        # adding widgets and layouts to form layout
        form_layout.addLayout(input_field_center_horizontal)
        form_layout.addLayout(slider_layout_v)

        # creating employee list layout
        emp_list_layout = QVBoxLayout()
        emp_list_widget = QWidget()
        emp_list_widget.setLayout(emp_list_layout)

        stacked_database_widget.addWidget(form_widget)
        stacked_database_widget.addWidget(emp_list_widget)

        database_layout.addLayout(database_switch)
        database_layout.addWidget(stacked_database_widget)
        database_widget.setLayout(database_layout)

        centered_layout = self.center_widget(database_widget)
        centered_layout.setContentsMargins(0,30,0,0)

        return centered_layout
    
    def create_schedule_layout(self):
        # Placeholder: utwórz i zwróć layout do widoku grafiku
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Schedule Page Content"))
        return layout
    
    def show_database_layout(self):
        self.stacked_widget.setCurrentWidget(self.database_window)

    def show_schedule_layout(self):
        self.stacked_widget.setCurrentWidget(self.schedule_window)

    def show_no_database_layout(self):
        self.stacked_widget.setCurrentWidget(self.no_db_window)

    def center_widget(self, widget:QWidget) -> QVBoxLayout:
        # horizontal layout to center the form container
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addStretch()
        horizontal_layout.addWidget(widget)
        horizontal_layout.addStretch()

        # vertical layout for overall placement in the window
        vertical_layout = QVBoxLayout()
        vertical_layout.addLayout(horizontal_layout)  
        vertical_layout.addStretch()

        return vertical_layout
    
    def paintEvent(self, event):
        # override paintEvent to draw the gradient background
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor("#f1b903"))
        gradient.setColorAt(1, QColor("#c6587c"))
        painter.fillRect(self.rect(), gradient)
        super().paintEvent(event)

    def load_custom_font(self):
        """Load a custom font from file"""
        font_id = QFontDatabase.addApplicationFont("img/Now.otf")
        if font_id != -1:
            print("Custom font loaded successfully.")
        else:
            print("Failed to load custom font.")

    def logout(self):
        self.clear_login_info()
    
    # clears all saved data form 'remember me'
    def clear_login_info(self):
        """Delete saved credentials"""
        config_file = "user_config.ini"
        if os.path.exists(config_file):
            config = configparser.ConfigParser()
            config.read(config_file)

            if 'USER' in config:
                email = config['USER']['Email']
                # delete password from keyring
                keyring.delete_password("schedule_creator", email)
                print("Login info cleared from keyring.")

            # delete conf file
            os.remove(config_file)
            print("Login info file deleted.")


class WindowControl(QStackedWidget):
    def __init__(self) -> None:
        super().__init__()
        # set the window properties
        self.setWindowTitle("Schedule Creator")
        self.setFixedSize(QSize(1400, 800)) # window size
        self.setWindowIcon(QIcon("img/icon.png")) # window icon

        if self.auto_login():
            self.show_main_program()
        else:
            self.show_login_window()
    
    def show_main_program(self):
        # create main program window
        self.main_program = MainProgram(self)
        self.addWidget(self.main_program)

        # switch to the main program
        self.setCurrentWidget(self.main_program)

        self.main_program.logout_button.clicked.connect(self.show_login_window)

        # if object has register_window attribute then remove it  from the stacked widget
        if hasattr(self, "register_window"):
            self.removeWidget(self.register_window)
            self.register_window.deleteLater()
            self.register_window = None
        
        # if object has login_window attribute then remove it  from the stacked widget
        if hasattr(self, "login_window"):
            self.removeWidget(self.login_window)
            self.login_window.deleteLater()
            self.login_window = None
    
    def show_login_window(self):
        # create new login window
        self.login_window = LoginWindow(self)

        # add it to the stack
        self.addWidget(self.login_window)

        # switch to login window
        self.setCurrentWidget(self.login_window)

        if hasattr(self, 'main_program'):
            self.removeWidget(self.main_program)
            self.main_program.deleteLater()
            self.main_program = None

        # connect the login button with show main program
        self.login_window.login_button.clicked.connect(self.show_main_program)
        self.login_window.register_label.linkActivated.connect(self.show_registration_window)

    def show_registration_window(self):
        # create new registration window
        self.register_window = RegisterWindow(self)

        # add it to the stack
        self.addWidget(self.register_window)

        # show regisration window
        self.setCurrentWidget(self.register_window)

        # switch to login window
        self.register_window.go_back_button.clicked.connect(self.show_login_window)
    
    def auto_login(self):
        # check if user_config.ini exists
        config_file = "user_config.ini"
        if os.path.exists(config_file):
            config = configparser.ConfigParser()
            config.read(config_file)

            if 'USER' in config:
                email = config['USER']['Email']

                # get password from keyring
                password = keyring.get_password("schedule_creator", email)
                if password:
                    login = Login()
                    login.connect(email, password)
                    print(f"Automatically logged in as {email}")
                    return True
                else:
                    print("No password found in keyring.")
                    return False

    def center(self):
        """Center the window on the screen"""
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        window_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window_controller = WindowControl()
    window_controller.center()
    window_controller.show()
    app.exec()