import sys, os, re
import keyring, configparser
from PySide6.QtCore import QSize, Qt, QEvent, QTimer
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QFormLayout, QLabel,
    QLineEdit, QCheckBox, QPushButton, QHBoxLayout, QStackedWidget,
    QToolTip, QGridLayout
)
from PySide6.QtGui import (QPainter, QPixmap, QFont, QFontDatabase, QGuiApplication,
                           QPalette, QColor, QIcon, QLinearGradient, QAction, QBrush
)
from database import Login, Register

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
        self.setup_ui()
        self.load_custom_font()

    def setup_ui(self):
        # Create main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Create and add the menu bar
        toolbar_widget = self.create_menubar()
        main_layout.addWidget(toolbar_widget)

        # Create and add main content widget
        content_widget = QWidget(self)
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # add a test widget to ensure the layout works


        # Add the content widget to the main layout
        main_layout.addWidget(content_widget)

        # Set the main layout to the widget
        self.setLayout(main_layout)
    
    def create_menubar(self):
        # create a layout for the toolbar
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setContentsMargins(80, 0, 80, 0)
        toolbar_layout.setAlignment(Qt.AlignTop)

        # Create buttons for the toolbar
        database_button = QPushButton("Database", self)
        schedule_button = QPushButton("Schedule", self)
        self.logout_button = QPushButton("Log out", self)

        button_font = QFont("Now", 13)
        button_font.setHintingPreference(QFont.HintingPreference.PreferNoHinting)
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
            button.setFont(button_font)
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
        toolbar_layout.addLayout(left_layout)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(logo_label)
        toolbar_layout.addStretch()
        toolbar_layout.addLayout(right_layout)

        # create a widget to hold the toolbar layout
        toolbar_widget = QWidget(self)
        toolbar_widget.setLayout(toolbar_layout)
        toolbar_widget.setStyleSheet("background-color: transparent;")

        return toolbar_widget
    
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
        self.setFixedSize(QSize(1400, 800))

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
            print("Jest login window!")
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