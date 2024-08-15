import sys, os
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QFormLayout, QLabel,
    QLineEdit, QCheckBox, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, QStackedWidget
)
from PySide6.QtGui import QPainter, QPixmap, QFont, QFontDatabase, QGuiApplication, QPalette, QColor

class LoginWindow(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Schedule Creator")
        self.load_custom_font()
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)  

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
        """)
        form_container.setObjectName("form_container")

        form_layout = QFormLayout()
        form_layout.setContentsMargins(0, 0, 0, 0)  
        form_layout.setSpacing(10)  

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

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("E-mail")
        self.email_input.setFixedSize(QSize(240,34))
        self.email_input.setStyleSheet("color: black;")

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setFixedSize(QSize(240,34))
        
        palette = self.email_input.palette()
        palette.setColor(QPalette.PlaceholderText, QColor(152, 111, 25))  
        palette.setColor(QPalette.Text, Qt.black)  
        self.email_input.setPalette(palette)
        self.password_input.setPalette(palette)

        small_font = QFont("Now", 8)
        small_font.setHintingPreference(QFont.HintingPreference.PreferNoHinting)

        forgot_password_label = QLabel('<a href="#" style="color: black;">Forgot your password?</a>')
        forgot_password_label.setFont(small_font)
        forgot_password_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        forgot_password_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        forgot_password_label.setOpenExternalLinks(False)
        forgot_password_label.linkActivated.connect(self.forgot_password_clicked) 

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

        button_font = QFont("Now", 8)
        button_font.setHintingPreference(QFont.HintingPreference.PreferNoHinting)

        login_button = QPushButton("LOG IN")
        login_button.setFixedSize(155, 45)
        login_button.setFont(button_font)
        login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        # login_button.clicked.connect(self.handle_login)
        centered_button_layout = QVBoxLayout()
        centered_button_layout.addWidget(login_button)
        centered_button_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        register_label = QLabel('<a href="#" style="color: black;">First time? Register</a>')
        register_label.setFont(small_font)
        register_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        register_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        register_label.setOpenExternalLinks(False)
        register_label.linkActivated.connect(self.switch_to_register)  

        spacer_widget = QWidget()
        spacer_widget.setFixedHeight(20)

        centered_fields_layout = QVBoxLayout()
        centered_fields_layout.addWidget(login_label)
        centered_fields_layout.addWidget(self.email_input)
        centered_fields_layout.addWidget(self.password_input)
        centered_fields_layout.addWidget(forgot_password_label)
        centered_fields_layout.addWidget(self.remember_me_checkbox)
        centered_fields_layout.addWidget(spacer_widget)
        centered_fields_layout.addWidget(spacer_widget)
        centered_fields_layout.addLayout(centered_button_layout)
        centered_fields_layout.addWidget(register_label)
        centered_fields_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        form_layout.addRow(centered_fields_layout)
        form_container.setLayout(form_layout)

        horizontal_layout = QHBoxLayout()
        horizontal_layout.addStretch()
        horizontal_layout.addWidget(form_container)
        horizontal_layout.addStretch()

        vertical_layout = QVBoxLayout()
        vertical_layout.setContentsMargins(0, 100, 0, 0)  
        vertical_layout.addLayout(horizontal_layout)  

        main_layout.addLayout(vertical_layout)

        self.setLayout(main_layout)

    def forgot_password_clicked(self):
        """Handle 'Forgot your password?' click"""
        print("Forgot your password clicked!")  
        self.clear_layout()
        self.show_password_reset_form()

    def switch_to_register(self):
        """Switch to the register window"""
        if self.parent():
            self.parent().setCurrentWidget(self.parent().register_window)

    def clear_layout(self):
        """Clears all widgets from the current layout"""
        layout = self.layout()
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

    def show_password_reset_form(self):
        """Show password reset form (for demonstration purposes)"""
        reset_label = QLabel("Password Reset")
        reset_label.setFont(QFont("Now", 31))
        reset_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.layout().addWidget(reset_label)

    def paintEvent(self, event):
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
        self.setWindowTitle("Register")
        self.load_custom_font()
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)  

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
        """)
        form_container.setObjectName("form_container")

        form_layout = QFormLayout()
        form_layout.setContentsMargins(0, 0, 0, 0)  
        form_layout.setSpacing(10)  

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

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFixedSize(QSize(240,34))
        self.username_input.setStyleSheet("color: black;")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("E-mail")
        self.email_input.setFixedSize(QSize(240,34))
        self.email_input.setStyleSheet("color: black;")

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setFixedSize(QSize(240,34))

        palette = self.username_input.palette()
        palette.setColor(QPalette.PlaceholderText, QColor(152, 111, 25))  
        palette.setColor(QPalette.Text, Qt.black)  
        self.username_input.setPalette(palette)
        self.email_input.setPalette(palette)
        self.password_input.setPalette(palette)

        button_font = QFont("Now", 8)
        button_font.setHintingPreference(QFont.HintingPreference.PreferNoHinting)

        register_button = QPushButton("REGISTER")
        register_button.setFixedSize(155, 45)
        register_button.setFont(button_font)
        register_button.setCursor(Qt.CursorShape.PointingHandCursor)

        centered_button_layout = QVBoxLayout()
        centered_button_layout.addWidget(register_button)
        centered_button_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        spacer_widget = QWidget()
        spacer_widget.setFixedHeight(20)

        centered_fields_layout = QVBoxLayout()
        centered_fields_layout.addWidget(register_label)
        centered_fields_layout.addWidget(self.username_input)
        centered_fields_layout.addWidget(self.email_input)
        centered_fields_layout.addWidget(self.password_input)
        centered_fields_layout.addWidget(spacer_widget)
        centered_fields_layout.addLayout(centered_button_layout)
        centered_fields_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        form_layout.addRow(centered_fields_layout)
        form_container.setLayout(form_layout)

        horizontal_layout = QHBoxLayout()
        horizontal_layout.addStretch()
        horizontal_layout.addWidget(form_container)
        horizontal_layout.addStretch()

        vertical_layout = QVBoxLayout()
        vertical_layout.setContentsMargins(0, 100, 0, 0)  
        vertical_layout.addLayout(horizontal_layout)  

        main_layout.addLayout(vertical_layout)

        self.setLayout(main_layout)

    def paintEvent(self, event):
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


class MainWindow(QStackedWidget):
    def __init__(self) -> None:
        super().__init__()

        # create the login window and register window
        self.login_window = LoginWindow(self)
        self.register_window = RegisterWindow(self)

        # add windows to the stacked widget
        self.addWidget(self.login_window)
        self.addWidget(self.register_window)

        # set the initial view
        self.setCurrentWidget(self.login_window)

        # set the window properties
        self.setWindowTitle("Schedule Creator")
        self.setFixedSize(QSize(1400, 800))

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
    main_window = MainWindow()
    main_window.center()
    main_window.show()
    app.exec()
