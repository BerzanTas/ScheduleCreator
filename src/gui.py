import sys, os, re
import keyring, configparser
from PySide6.QtCore import QSize, Qt, QEvent, QTimer, Slot, QStandardPaths
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QFormLayout, QLabel,
    QLineEdit, QCheckBox, QPushButton, QHBoxLayout, QStackedWidget,
    QToolTip, QFrame, QSlider, QScrollArea, QMenu, QComboBox, QFileDialog
)
from PySide6.QtGui import (QPainter, QPixmap, QFont, QFontDatabase, QGuiApplication,
                           QPalette, QColor, QIcon, QLinearGradient, QAction, QDragEnterEvent, QDropEvent
)
from database import Login, Register, EmployeeData

class LoginWindow(QWidget):
    """Defines the login window UI and its behavior"""
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.autologin = False
        # if user chose 'remember me', automatically switch to the main program without creating LoginWindow UI
        if self.auto_login():
            self.autologin = True
        else:
            self.load_custom_font()
            self.setup_ui()

    def setup_ui(self):
        """Setup the user interface elements for the login window"""
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
        """Automaticly log in the user from saved credentials"""
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
        """Validate email format and check for duplicate entries"""
        text = self.email_input.text()

        if re.fullmatch(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', text):
            self.email_input.setStyleSheet("border: 1px solid green;")
            self.email_input.setToolTip("")

            # check if email already exists
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
        """Validate password strength"""
        text = self.password_input.text()

        # regex to check for at least 8 characters, one uppercase, and one lowercase letter
        if re.fullmatch(r'(?=.*[a-z])(?=.*[A-Z])[A-Za-z0-9\d@$!%*?&.,]{8,}$', text):
            self.password_input.setStyleSheet("border: 1px solid green;")
            self.password_input.setToolTip("")
            return True
        else:
            self.password_input.setStyleSheet("border: 1px solid red;")
            self.password_input.setToolTip("Password must be:\n- at least 8 characters,\n- one uppercase,\n- one lowercase.")
            return False

    def confirm_password(self):
        """Check if both password fields match"""
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

        # check if all fields are filled correctly
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
        """Clear input fields and show success notification"""
        # clear all input fields after successful registration
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

        # set the timer for notification to disappear after 3 seconds
        QTimer.singleShot(3000, self.notification_label.hide)
    
    def eventFilter(self, source, event):
        """Handle mouse hover events to show tooltip for invalid inputs"""
        if event.type() == QEvent.HoverEnter:
            # show tooltip if the input data is invalid
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
    """Defines the main program UI and behavior after a successful login"""
    def __init__(self, user, parent=None) -> None:
        super().__init__(parent)
        self.employee_data = EmployeeData()
        self.user_mail = user
        # check if user is editing employee record
        self.is_editing = False

        self.load_custom_font()
        
        # creating fonts for different UI elements
        self.button_font = QFont("Now", 13)
        self.button_font.setHintingPreference(QFont.HintingPreference.PreferNoHinting)
        self.head_font = QFont("Now", 14)
        self.head_font.setHintingPreference(QFont.HintingPreference.PreferNoHinting)
        self.paragraph_font = QFont("Now", 12)
        self.paragraph_font.setHintingPreference(QFont.HintingPreference.PreferNoHinting)
        self.font11 = QFont("Now", 11)
        self.font11.setHintingPreference(QFont.HintingPreference.PreferNoHinting)

        self.setup_ui()
        

    def setup_ui(self):
        """Setup the user interface elements for the main program"""
        # create main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # create and add the menu bar
        menubar_widget = self.create_menubar()

        # QStackedWidget allows switching between different screens (e.g., database, schedule)
        self.stacked_widget = QStackedWidget(self)
        
        # database window setup
        self.database_window = QWidget(self)
        self.database_window.setLayout(self.create_database_layout())

        # schedule window setup
        self.schedule_window = QWidget(self)
        self.schedule_window.setLayout(self.create_schedule_layout())

        # add both windows to the stacked widget
        self.stacked_widget.addWidget(self.database_window)
        self.stacked_widget.addWidget(self.schedule_window)

        # check if the employee table exists for the user
        if self.employee_data.checkIfTableExist(self.user_mail) != 200:
            # if no employee table, show the no database window
            self.no_db_window = QWidget()
            self.no_db_window.setLayout(self.no_database_layout())
            self.stacked_widget.addWidget(self.no_db_window)
            self.stacked_widget.setCurrentWidget(self.no_db_window)
        else:
            # if employee table exists, show the schedule window
            self.stacked_widget.setCurrentWidget(self.schedule_window)
        
        # add the menu bar and stacked widget to the main layout
        main_layout.addWidget(menubar_widget)
        main_layout.addWidget(self.stacked_widget)

        # set the main layout to the widget
        self.setLayout(main_layout)
    
    def create_menubar(self):
        """Create the top menu bar with navigation buttons"""
        # create a layout for the menubar
        menubar_layout = QHBoxLayout()
        menubar_layout.setContentsMargins(80, 0, 80, 0)
        menubar_layout.setAlignment(Qt.AlignTop)

        # create buttons for the menubar
        database_button = QPushButton("Database", self)
        database_button.clicked.connect(self.show_database_layout)
        schedule_button = QPushButton("Schedule", self)
        schedule_button.clicked.connect(self.show_schedule_layout)
        self.logout_button = QPushButton("Log out", self)

        # apply styling and setup event handlers for the buttons
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

        # create and add logo to the menu bar
        logo_label = QLabel(self)
        logo_label.setFixedSize(235, 115)
        logo_pixmap = QPixmap("img/logo.png")
        logo_label.setPixmap(logo_pixmap.scaled(logo_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        # handle left side of the logo (database and schedule buttons)
        left_layout = QHBoxLayout()
        left_layout.addWidget(database_button)
        left_layout.addSpacing(50)
        left_layout.addWidget(schedule_button)
        left_layout.addStretch()

        # handle right side of the logo (logout button)
        right_layout = QHBoxLayout()
        right_layout.addStretch()
        right_layout.addWidget(self.logout_button)
        
        # add both left and right layouts to the menubar
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
        The layout that the user will see after the first login post-registration
        or the first login after deleting the database. The user will be asked to create a database.
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

        # add the elements to the layout
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
        """Create the layout for creating and editing employee database"""

        def update_value_label():
            """Update the label that shows the slider value"""
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

        def add_employee():
            """Add an employee to the database using the input form"""
            self.employee_data.addEmployee(self.user_mail, emp_id.text(), emp_name.text(), values[slider.value()-1], student_second_job_checkbox.isChecked())

        # QStackedWidget for changing layout between adding employee and list of employees
        self.stacked_database_widget = QStackedWidget()

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

        self.add_employee_button = QPushButton("ADD EMPLOYEE")
        self.employee_list_button = QPushButton("EMPLOYEE LIST")

        for button in [self.add_employee_button, self.employee_list_button]:
            button.setFixedSize(200,60)
            button.setFont(self.button_font)

        self.add_employee_button.setStyleSheet("""
                                            color: #df9233;
                                            background-color: black;
                                            margin-right: -10px;
                                            border-radius: 0px;
                                            outline: none;
                                          """)
        self.add_employee_button.clicked.connect(self.show_add_emp)
        self.employee_list_button.setStyleSheet("""
                                            color: black;
                                            background-color: transparent;
                                            border-radius: 0px;
                                            margin-left: -10px;
                                            outline: none;
                                           """)
        self.employee_list_button.clicked.connect(self.show_emp_list)

        # add buttons to the layout
        database_switch.addWidget(self.add_employee_button)
        database_switch.addWidget(self.employee_list_button)

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

        ###### creating employee add form ######
        form_layout = QVBoxLayout()
        form_layout.setSpacing(50)
        form_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.form_widget = QWidget()
        self.form_widget.setFixedSize(560, 520)
        self.form_widget.setStyleSheet("""
                                    background-color: rgba(0, 0, 0, 0.15);
                                    border-radius: 15px;
                                """)
        self.form_widget.setLayout(form_layout)

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
        input_field_center_horizontal.setContentsMargins(0,50,0,0)
        input_field_center_horizontal.setSpacing(30)

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
            label.setFont(self.font11)
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
        value_label = QLabel(self.form_widget)
        value_label.setFixedSize(50, 20)
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setFont(self.font11)
        value_label.setStyleSheet("color: black; background: none;")

        # change value_label position to be alway on top of handle
        update_value_label()

        # grouping slider with bottom label
        slider_layout_v.addLayout(slider_layout)
        slider_layout_v.addWidget(slider_label)
        slider_layout_v.setSpacing(0)

        # student/second job checkbox setup
        student_second_job_checkbox = QCheckBox("Student or Second Job")
        # making cursor clickable when checkbox hovered
        student_second_job_checkbox.setCursor(Qt.CursorShape.PointingHandCursor)
        student_second_job_checkbox.setFont(self.font11)
        student_second_job_checkbox.setStyleSheet("""
                                                QCheckBox {
                                                    color: black;
                                                    font-size: 15px;
                                                    background: none;
                                                    outline: none;
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
        # center checkbox
        centered_checkbox = self.center_widget(student_second_job_checkbox)

        # creating ADD button to add employee to database
        add_button = QPushButton("ADD")
        add_button.clicked.connect(add_employee)
        add_button.setFont(self.button_font)
        add_button.setStyleSheet("""
                                 background-color: black;
                                 color: #d47853;
                                 border-radius: 10;
                                 outline: none;
                                 """)
        add_button.setFixedSize(240, 45)
        add_button.setCursor(Qt.CursorShape.PointingHandCursor)
        add_button_center = self.center_widget(add_button)

        # adding widgets and layouts to form layout
        form_layout.addLayout(input_field_center_horizontal)
        form_layout.addLayout(slider_layout_v)
        form_layout.addLayout(centered_checkbox)
        form_layout.addLayout(add_button_center)

        ###### creating employee list layout ######
        emp_list_layout = QVBoxLayout()
        self.emp_list_widget = QWidget()
        self.emp_list_widget.setStyleSheet("""
                                        background-color: rgba(0, 0, 0, 0.15);
                                        border-radius: 15px;
                                    """)
        self.emp_list_widget.setLayout(emp_list_layout)
        
        emp_list_headers = QHBoxLayout()
        emp_list_headers.setContentsMargins(0,30,0,0)
        emp_list_headers.setSpacing(0)

        id_label = QLabel("ID")
        name_label = QLabel("Name")
        wt_label = QLabel("WT")
        student_label = QLabel("Student/SJ")
        
        for label in [id_label, name_label, wt_label, student_label]:
            label.setStyleSheet("""
                                color: black;
                                background: none;
                                """)
            label.setFont(self.font11)
            label.setFixedWidth(100)

        
        emp_list_headers.addSpacing(30)
        emp_list_headers.addWidget(id_label)
        emp_list_headers.addSpacing(20)
        emp_list_headers.addWidget(name_label)
        emp_list_headers.addSpacing(20)
        wt_label.setContentsMargins(10,0,0,0)
        emp_list_headers.addWidget(wt_label)
        emp_list_headers.addWidget(student_label)
        emp_list_headers.addStretch()

        # create a line below headers
        header_line = QFrame()
        header_line.setFrameShape(QFrame.HLine)
        header_line.setFrameShadow(QFrame.Sunken)
        header_line.setStyleSheet("background-color: black;")
        header_line.setFixedSize(527, 1)

        # center that line horizontaly
        line_center = QHBoxLayout()
        line_center.addStretch()
        line_center.addWidget(header_line)
        line_center.addStretch()
        
        # group headers and line together
        header_and_line = QVBoxLayout()
        header_and_line.addLayout(emp_list_headers)
        header_and_line.addLayout(line_center)
        header_and_line.setAlignment(Qt.AlignmentFlag.AlignTop)

        # adding list area with scrollbar for employee list
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedWidth(525)

        scroll_area_centered = QHBoxLayout()
        scroll_area_centered.addStretch()
        scroll_area_centered.addWidget(self.scroll_area)
        scroll_area_centered.addStretch()

        
        
        emp_list_layout.addLayout(header_and_line)
        emp_list_layout.addLayout(scroll_area_centered)


        self.stacked_database_widget.addWidget(self.form_widget)
        self.stacked_database_widget.addWidget(self.emp_list_widget)

        database_layout.addLayout(database_switch)
        database_layout.addWidget(self.stacked_database_widget)
        database_widget.setLayout(database_layout)

        centered_layout = self.center_widget(database_widget)
        centered_layout.setContentsMargins(0,30,0,0)

        return centered_layout
    
    def create_schedule_layout(self):
        """Create the layout for uploading files and generating a schedule"""
        schedule_layout = QVBoxLayout()

        # setup label for file upload
        upload_font = QFont("Now", 18)
        upload_label = QLabel("Upload File")
        upload_label.setFont(upload_font)
        upload_label.setStyleSheet("background: transparent;")
        centered_upload = self.center_widget(upload_label)
        centered_upload.setContentsMargins(0,20,0,0)

        # setup layout for drag-and-drop area
        drag_n_drop_layout = QVBoxLayout()
        drag_n_drop_layout.setSpacing(10)

        upload_icon = QLabel()
        pixmap = QPixmap("img/upload.png")
        scaled_pixmap = pixmap.scaled(45, 45, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        upload_icon.setPixmap(scaled_pixmap)
        upload_icon.setFixedSize(45,45)
        upload_icon.setStyleSheet("""
                                  background: none;
                                  border: none;
                                  border-radius: 0px;
                                  """)
        centered_upload_icon = QHBoxLayout()
        centered_upload_icon.addStretch()
        centered_upload_icon.addWidget(upload_icon)
        centered_upload_icon.addStretch()
        centered_upload_icon.setContentsMargins(0,50,0,0)
        
        # setup drag-and-drop label
        self.drag_n_drop_label = QLabel("Drag and Drop file\nor")
        self.drag_n_drop_label.setFont(self.head_font)
        self.drag_n_drop_label.setStyleSheet("""
                                        background: none;
                                        border: none;
                                        border-radius: 0px;
                                        """)
        self.drag_n_drop_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # setup browse button for file upload
        browse_button = QPushButton("Browse")
        browse_button.setFont(self.head_font)
        browse_button.setFixedSize(140, 37)
        browse_button.setCursor(Qt.CursorShape.PointingHandCursor)
        browse_button.clicked.connect(self.open_file_dialog)
        browse_button.setStyleSheet("""
                                    color: #da8444;
                                    background-color: black;
                                    border: none;
                                    border-radius: 10px;
                                    """)
        center_browse_button = self.center_widget(browse_button)

        # add components to the drag-and-drop layout
        drag_n_drop_layout.addLayout(centered_upload_icon)
        drag_n_drop_layout.addWidget(self.drag_n_drop_label)
        drag_n_drop_layout.addLayout(center_browse_button)

        # setup drag-and-drop area widget
        self.drag_n_drop_widget = QWidget()
        self.drag_n_drop_widget.setLayout(drag_n_drop_layout)
        self.drag_n_drop_widget.setAcceptDrops(True)
        self.drag_n_drop_widget.setFixedSize(370, 250)
        self.drag_n_drop_widget.setStyleSheet("""
                                         background-color: rgba(255,255,255,0.15);
                                         border: 2px dashed black;
                                         border-radius: 15;
                                        """)
        centered_drag_n_drop = self.center_widget(self.drag_n_drop_widget)
        centered_drag_n_drop.setContentsMargins(0,0,0,20)

        # add components to the main layout
        schedule_layout.addLayout(centered_upload)
        schedule_layout.addLayout(centered_drag_n_drop)
        
        schedule_widget = QWidget()
        schedule_widget.setLayout(schedule_layout)
        schedule_widget.setStyleSheet("""
                                      color: black;
                                      background-color: rgba(255,255,255,0.15);
                                      border-radius: 15;
                                      """)
        schedule_widget.setFixedSize(450, 400)
        centered_schedule_widget = self.center_widget(schedule_widget)
        centered_schedule_widget.setContentsMargins(0,70,0,0)

        # create drag and drop events to upload files
        def dragEnterEvent(event: QDragEnterEvent):
            if event.mimeData().hasUrls():
                event.acceptProposedAction()

        def dropEvent(event: QDropEvent):
            files = event.mimeData().urls()
            if files:
                self.file_path = files[0].toLocalFile()
                # accept only Excel files
                if self.file_path.endswith(('.xls', '.xlsx')):
                    print(f"Valid Excel file dropped: {self.file_path}")
                    #if valid file, than change border to green, display file name and enable generate button
                    self.drag_n_drop_label.setText(f"{self.file_path.split("/")[-1]} dropped")
                    self.drag_n_drop_widget.setStyleSheet("""
                                                     background-color: rgba(255,255,255,0.15);
                                                     border: 2px dashed green;
                                                     border-radius: 15;
                                                     """)
                    self.generate_button.setCursor(Qt.CursorShape.PointingHandCursor)
                    self.generate_button.setStyleSheet("""
                                                        color: #da8444;
                                                        background-color: black;
                                                        border: none;
                                                        border-radius: 10px;
                                                        """)
                else:
                    print(f"Ignored non-Excel file: {self.file_path}")
                    self.drag_n_drop_label.setText("Only Excel files are accepted")
                    self.drag_n_drop_widget.setStyleSheet("""
                                                     background-color: rgba(255,255,255,0.15);
                                                     border: 2px dashed red;
                                                     border-radius: 15;
                                                     """)
                    self.generate_button.setCursor(Qt.CursorShape.CustomCursor)
                    self.generate_button.setStyleSheet("""
                                    color: #606060;
                                    background-color: rgba(192,192,192,0.5);
                                    border: none;
                                    border-radius: 10px;
                                    """)

        # bind drag-and-drop events
        self.drag_n_drop_widget.dragEnterEvent = dragEnterEvent
        self.drag_n_drop_widget.dropEvent = dropEvent

        # setup generate button
        self.generate_button = QPushButton("Generate!")
        self.generate_button.setFont(self.head_font)
        self.generate_button.setFixedSize(240, 50)
        # disable the generate button initially
        self.generate_button.setStyleSheet("""
                                    color: #606060;
                                    background-color: rgba(192,192,192,0.5);
                                    border: none;
                                    border-radius: 10px;
                                    """)

        centered_generate_button = self.center_widget(self.generate_button)
        centered_generate_button.setContentsMargins(0, 50, 0, 0)

        # group drag_n_drop and generate button
        main_layout = QVBoxLayout()
        main_layout.addLayout(centered_schedule_widget)
        main_layout.addLayout(centered_generate_button)

        return main_layout
    
    def open_file_dialog(self):
        # get desktop path
        desktop_path = QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)

        # open file dialog and get the selected file path
        self.file_path, _ = QFileDialog.getOpenFileName(self, "Select an Excel file", desktop_path, "Excel  Files (*.xls *.xlsx)")

        if self.file_path:
            # extract the file name from the path
            file_name = os.path.basename(self.file_path)

            # handle valid and invalid file selections
            if self.file_path.endswith(('.xls', '.xlsx')):
                print(f"Valid Excel file dropped: {self.file_path}")
                self.drag_n_drop_label.setText(f"{self.file_path.split("/")[-1]} chosen")
                self.drag_n_drop_widget.setStyleSheet("""
                                                background-color: rgba(255,255,255,0.15);
                                                border: 2px dashed green;
                                                border-radius: 15;
                                                """)
                self.generate_button.setCursor(Qt.CursorShape.PointingHandCursor)
                self.generate_button.setStyleSheet("""
                                color: #da8444;
                                background-color: black;
                                border: none;
                                border-radius: 10px;
                                """)
            else:
                print(f"Ignored non-Excel file: {self.file_path}")
                self.drag_n_drop_label.setText("Only Excel files are accepted")
                self.drag_n_drop_widget.setStyleSheet("""
                                                background-color: rgba(255,255,255,0.15);
                                                border: 2px dashed red;
                                                border-radius: 15;
                                                """)
                self.generate_button.setCursor(Qt.CursorShape.CustomCursor)
                self.generate_button.setStyleSheet("""
                                        color: #606060;
                                        background-color: rgba(192,192,192,0.5);
                                        border: none;
                                        border-radius: 10px;
                                        """)
    
    def show_database_layout(self):
        """Switches the current view to the database layout"""
        self.stacked_widget.setCurrentWidget(self.database_window)

    def show_schedule_layout(self):
        """Switches the current view to the schedule layout"""
        self.stacked_widget.setCurrentWidget(self.schedule_window)

    def show_no_database_layout(self):
        """Switches the current view to the 'no database' layout"""
        self.stacked_widget.setCurrentWidget(self.no_db_window)

    def show_add_emp(self):
        """Shows the add employee form layout"""
        self.stacked_database_widget.setCurrentWidget(self.form_widget)
        self.employee_list_button.setStyleSheet("""
                                          color: black;
                                          background-color: transparent;
                                          border-radius: 0px;
                                          margin-left: -10px;
                                          outline: none;
                                          """)
        self.add_employee_button.setStyleSheet("""
                                           color: #df9233;
                                           background-color: black;
                                           margin-right: -10px;
                                           border-radius: 0px;
                                           outline: none;
                                           """)
        
        
    def show_emp_list(self):
        """Updates and shows the employee list layout"""
        # change button styles to reflect the active view
        self.add_employee_button.setStyleSheet("""
                                          color: black;
                                          background-color: transparent;
                                          border-radius: 0px;
                                          margin-right: -10px;
                                          outline: none;
                                          """)
        self.employee_list_button.setStyleSheet("""
                                           color: #df9233;
                                           background-color: black;
                                           margin-left: -10px;
                                           border-radius: 0px;
                                           outline: none;
                                           """)
        # set employee list as the current widget in the stacked widget
        self.stacked_database_widget.setCurrentWidget(self.emp_list_widget)
        
        self.update_scroll_area()

        
    def update_scroll_area(self):
        """Creates and updates the employee list in the scroll area"""
        # get employee data from database
        employee_list = self.employee_data.getEmployeeTable(self.user_mail)
        # remove user_id (first column) as it is not needed in the display
        employee_list = [row[1:] for row in employee_list]
        
        list_area_widget = QWidget()
        list_area_widget.setStyleSheet("background: none;")
        list_area_layout = QVBoxLayout(list_area_widget)
        
        if len(employee_list) > 0:
            # iterate over employee data and create rows
            for data in employee_list:
                row_layout = QHBoxLayout()
                config_button = QPushButton()
                config_button.setIcon(QIcon(QPixmap("img/more.png")))
                config_button.setCursor(Qt.CursorShape.PointingHandCursor)
                config_button.setStyleSheet("""
                                            background: none;
                                            border: none;
                                            outline: none;
                                            """)
                # set the employee ID as the button's property for later use
                config_button.setProperty("employee_id", data[0])
                config_button.clicked.connect(self.show_context_menu)

                # create labels for each employee's data (ID, name, working time, student status)
                emp_list_id = QLabel(data[0])
                emp_list_name = QLabel(data[1])
                emp_list_wt = QLabel(data[2])
                emp_list_student = QLabel("Yes" if data[3] == 1 else "No")

                # assign properties to each QLabel for reference during editing
                emp_list_id.setProperty('employee_id', data[0])
                emp_list_id.setProperty('type', 'id')

                emp_list_name.setProperty('employee_id', data[0])
                emp_list_name.setProperty('type', 'name')

                emp_list_wt.setProperty('employee_id', data[0])
                emp_list_wt.setProperty('type', 'wt')

                emp_list_student.setProperty('employee_id', data[0])
                emp_list_student.setProperty('type', 'student')

                # style labels and set their fixed size
                for label in [emp_list_id, emp_list_name, emp_list_wt, emp_list_student]:
                    label.setStyleSheet("color: black; background: none;")
                    label.setFont(self.font11)
                    label.setFixedWidth(100)
                
                # add labels and config button to the row layout
                row_layout.addSpacing(10)
                row_layout.addWidget(emp_list_id)
                row_layout.addSpacing(15)
                row_layout.addWidget(emp_list_name)
                row_layout.addSpacing(25)
                row_layout.addWidget(emp_list_wt)
                row_layout.addWidget(emp_list_student)
                row_layout.addWidget(config_button)
                row_layout.addStretch()

                # add a horizontal line between rows
                row_line = QFrame()
                row_line.setFrameShape(QFrame.HLine)
                row_line.setFrameShadow(QFrame.Sunken)
                row_line.setStyleSheet("background-color: rgba(0,0,0,0.10);")
                row_line.setFixedHeight(1)

                # add the row layout and line to the main layout
                list_area_layout.addLayout(row_layout)
                list_area_layout.addWidget(row_line)

            # add a stretch at the end to avoid cutting off the last row
            list_area_layout.addStretch()

        # add the list of employees to the scroll area
        self.scroll_area.setWidget(list_area_widget)
        self.scroll_area.setStyleSheet("""
                                    QScrollArea {
                                        background-color: rgba(255,255,255,0.15);
                                        border-radius: 5;
                                    }
                                    QScrollBar:vertical {
                                        background-color: rgba(0,0,0,0.15);
                                        width: 6px;
                                    }
                                    QScrollBar::handle:vertical {
                                        background-color: black;
                                        min-height: 20px;
                                    }
                                    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                                        background: none;
                                        height: 0px;
                                        width: 4px;
                                    }
                                    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                                        background: none;
                                        height: 0px;
                                        width: 4px;
                                    }
                                """)
    
    @Slot()
    def show_context_menu(self):
        """Show a context menu with options to edit or delete an employee"""
        # retrieve the employee ID from the button's property
        button = self.sender()
        employee_id = button.property('employee_id')

        # create the context menu
        menu = QMenu(self)

        if not self.is_editing:
            # if not currently editing, show options to edit or delete the employee
            edit_action = QAction("Edit", self)
            delete_action = QAction("Delete", self)
            menu.addAction(edit_action)
            menu.addAction(delete_action)
            # connect actions to their respective methods
            edit_action.triggered.connect(lambda: self.edit_employee(employee_id))
            delete_action.triggered.connect(lambda: self.delete_employee(employee_id))
        else:
            # if editing, show options to save or cancel the changes
            save_action = QAction("Save", self)
            cancel_action = QAction("Cancel", self)
            save_action.triggered.connect(lambda: self.save_changes(employee_id))
            cancel_action.triggered.connect(lambda: self.cancel_edit(employee_id))
            menu.addAction(save_action)
            menu.addAction(cancel_action)
        
        # set margins and size for the context menu
        menu.setContentsMargins(-30,0,0,0)
        menu.setFixedSize(70, 55)
        
        # display the context menu at the button's position
        menu.exec(button.mapToGlobal(button.rect().bottomRight()))

    def delete_employee(self, employee_id):
        """Delete an employee from the database"""
        print(f"Delete employee with ID: {employee_id}")
        self.employee_data.deleteEmployee(self.user_mail, employee_id)

        # refresh the employee list
        self.update_scroll_area()

    def edit_employee(self, employee_id):
        """Edit the details of an existing employee"""
        print(f"Edit employee with ID: {employee_id}")
        self.is_editing = True

        for label in self.findChildren(QLabel):
            # find the QLabel that matches the employee ID and replace it with editable widgets
            if label.property("employee_id") == employee_id:
                text = label.text()
                layout = label.parentWidget().layout()
                
                if label.property('type') == 'id':
                    # convert QLabel to QLineEdit for editing employee ID
                    id_line_edit = QLineEdit(text)
                    id_line_edit.setFont(self.font11)
                    id_line_edit.setFixedWidth(100)
                    layout.replaceWidget(label, id_line_edit)
                    label.deleteLater()
                    id_line_edit.setStyleSheet("""
                                            color: black;
                                            background-color: rgba(255,255,210,0.40);
                                            border: 1px solid black;
                                            """)
                    
                elif label.property('type') == 'name':
                    # convert QLabel to QLineEdit for editing employee name
                    name_line_edit = QLineEdit(text)
                    name_line_edit.setFont(self.font11)
                    name_line_edit.setFixedWidth(100)
                    layout.replaceWidget(label, name_line_edit)
                    label.deleteLater()
                    name_line_edit.setStyleSheet("""
                                            color: black;
                                            background-color: rgba(255,255,210,0.40);
                                            border: 1px solid black;
                                            """)

                elif label.property('type') == 'wt':
                    # convert QLabel to QComboBox for editing work time
                    wt_combo_box = QComboBox()
                    wt_combo_box.addItems(["0.25", "0.5", "0.75", "1"])
                    wt_combo_box.setCurrentText(text)
                    wt_combo_box.setFont(self.font11)
                    wt_combo_box.setFixedWidth(100)
                    wt_combo_box.setStyleSheet("""
                                            QComboBox {
                                                background-color: rgba(255,255,210,0.40);
                                                border: 1px solid black;
                                                color: black;
                                            }
                                            QComboBox QAbstractItemView {
                                                background-color: rgba(255,255,210,0.40);
                                                border: 1px solid black;
                                                border-radius: 2px;
                                                color: black;
                                            }
                                            """)
                    layout.replaceWidget(label, wt_combo_box)
                    label.deleteLater()

                elif label.property('type') == 'student':
                    # convert QLabel to QComboBox for editing student status
                    st_combo_box = QComboBox()
                    st_combo_box.addItems(["Yes", "No"])
                    st_combo_box.setCurrentText(text)
                    st_combo_box.setFont(self.font11)
                    st_combo_box.setFixedWidth(100)
                    st_combo_box.setStyleSheet("""
                                            QComboBox {
                                                background-color: rgba(255,255,210,0.40);
                                                border: 1px solid black;
                                                color: black;
                                            }
                                            QComboBox QAbstractItemView {
                                                background-color: rgba(255,255,210,0.40);
                                                border: 1px solid black;
                                                border-radius: 2px;
                                                color: black;
                                            }
                                            """)
                    layout.replaceWidget(label, st_combo_box)
                    label.deleteLater()
        
        # store the new data in a list for later use when saving
        self.new_data = [id_line_edit, name_line_edit, wt_combo_box, st_combo_box]

    def save_changes(self, old_employee_id):
        """Save the changes made to an employee's details"""
        print(f"Save changes for employee with ID: {old_employee_id}")
        self.is_editing = False
        # retrieve updated values from the editing widgets
        id = self.new_data[0].text()
        name = self.new_data[1].text()
        wt = self.new_data[2].currentText()
        student_sj = 1 if self.new_data[3].currentText() == "Yes" else 0
        
        # update the employee data in the database
        self.employee_data.updateEmployeeData(self.user_mail, old_employee_id, id, name, wt, student_sj)
        # refresh the employee list
        self.update_scroll_area()
        
    def cancel_edit(self, employee_id):
        """Cancel editing and revert back to the original data"""
        print(f"Cancel editing for employee with ID: {employee_id}")
        self.is_editing = False
        # revert any changes and refresh the employee list
        self.update_scroll_area()

    def center_widget(self, widget:QWidget) -> QVBoxLayout:
        """Helper method to center a widget both horizontally and vertically"""
        # create horizontal layout to center the widget
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addStretch()
        horizontal_layout.addWidget(widget)
        horizontal_layout.addStretch()

        # create vertical layout for overall placement in the window
        vertical_layout = QVBoxLayout()
        vertical_layout.addLayout(horizontal_layout)  
        vertical_layout.addStretch()

        return vertical_layout
    
    def paintEvent(self, event):
        """Override paintEvent to draw the gradient background"""
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
        """Log out the user and clear saved login information"""
        self.clear_login_info()
    
    def clear_login_info(self):
        """Delete saved credentials from keyring and the config file"""
        config_file = "user_config.ini"
        if os.path.exists(config_file):
            config = configparser.ConfigParser()
            config.read(config_file)

            if 'USER' in config:
                email = config['USER']['Email']
                # delete password from keyring
                keyring.delete_password("schedule_creator", email)
                print("Login info cleared from keyring.")

            # delete the config file
            os.remove(config_file)
            print("Login info file deleted.")


class WindowControl(QStackedWidget):
    def __init__(self) -> None:
        super().__init__()
        # set the window properties
        self.setWindowTitle("Schedule Creator")
        self.setFixedSize(QSize(1400, 800)) # window size
        self.setWindowIcon(QIcon("img/icon.png")) # window icon
        self.center()
        self.email = None

        # automatically log in if credentials are saved
        if self.auto_login():
            self.show_main_program()
        else:
            self.show_login_window()
    
    def show_main_program(self):
        """Switches to the main program view after login"""
        # create main program window
        self.main_program = MainProgram(self.email, self)
        self.addWidget(self.main_program)

        # switch to the main program
        self.setCurrentWidget(self.main_program)

        # connect the logout button to the method that switches back to the login window
        self.main_program.logout_button.clicked.connect(self.show_login_window)

        # remove registration and login windows from the stacked widget if they exist
        if hasattr(self, "register_window"):
            self.removeWidget(self.register_window)
            self.register_window.deleteLater()
            self.register_window = None
        
        if hasattr(self, "login_window"):
            self.email = self.login_window.email_input.text()
            self.removeWidget(self.login_window)
            self.login_window.deleteLater()
            self.login_window = None
    
    def show_login_window(self):
        """Switches to the login window view"""
        # create a new login window
        self.login_window = LoginWindow(self)
        self.addWidget(self.login_window)

        # switch to the login window
        self.setCurrentWidget(self.login_window)

        # remove the main program view if it exists
        if hasattr(self, 'main_program'):
            self.removeWidget(self.main_program)
            self.main_program.deleteLater()
            self.main_program = None

        # connect the login button and register label to their respective methods
        self.login_window.login_button.clicked.connect(self.show_main_program)
        self.login_window.register_label.linkActivated.connect(self.show_registration_window)

    def show_registration_window(self):
        """Switches to the registration window view"""
        # create new registration window
        self.register_window = RegisterWindow(self)
        self.addWidget(self.register_window)

        # switch to the registration window
        self.setCurrentWidget(self.register_window)

        # connect the back button to return to the login window
        self.register_window.go_back_button.clicked.connect(self.show_login_window)
    
    def auto_login(self):
        """Automatically log in if saved credentials are found"""
        config_file = "user_config.ini"
        if os.path.exists(config_file):
            config = configparser.ConfigParser()
            config.read(config_file)

            if 'USER' in config:
                self.email = config['USER']['Email']

                # retrieve the password from keyring
                password = keyring.get_password("schedule_creator", self.email)
                if password:
                    login = Login()
                    login.connect(self.email, password)
                    print(f"Automatically logged in as {self.email}")
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