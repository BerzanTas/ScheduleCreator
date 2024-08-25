![](img/ScheduleCreator.png)
# Schedule Creator

## Overview
The Schedule Creator is a Python-based application designed to create and manage employee work schedules. The program reads an Excel file containing employee availability data, processes the information, and generates a work schedule for the entire month. It also includes a graphical user interface (GUI) for managing employee data and work schedules.

## Features
- **Excel File Processing**: Reads and formats Excel files containing employee availability.
- **Database Management**: The software uses the `requests` library to connect to a Flask API running in Docker on a VPS. The API manages user and employee data in a MySQL server running in Docker.
- **Scheduling Algorithm**: Creates a work schedule based on employee availability, ensuring that constraints like maximum work hours and minimum availability are met.
- **GUI**: Built with PySide6 for user-friendly interaction.

## Project Structure
- `src/main.py`: Main application file that initializes and runs the program.
- `src/database.py`: Contains API requests to the VPS server for user identification and employee data.
- `src/gui.py`: Implements the graphical user interface using PySide6.
- `src/scheduleCreator.py`: Contains the `ScheduleCreator` class for generating the work schedule.
- `src/settings.py`: Configuration file with various settings and constraints.
- `src/sensitive_data.py`: Stores sensitive information required for API communication.
- `schedule.xlsx`: Example Excel file containing employee availability data.
- `user_config.ini`: Configuration file with user-specific settings.
- `requirements.txt`: Lists the Python dependencies required to run the project.

## Detailed Description
### Excel File Processing
The program reads an Excel file using `pandas`, processes it to enhance readability, and extracts employee availability information. The availability data is then used to generate a work schedule.

### Database Management
Change the text here

### Scheduling Algorithm
The scheduling algorithm considers constraints such as maximum work hours, minimum number of workers per hour, and employee unavailability. It ensures that the generated schedule meets all these constraints.

### GUI
The GUI, built with PySide6, provides an interface for users to interact with the application. It allows users to manage employee data and view the generated work schedules.

## Settings
The `settings.py` file contains various configuration options:
- `OPEN_HOUR`: The opening hour of the workday.
- `CLOSE_HOUR`: The closing hour of the workday.
- `MIN_WORKERS`: Minimum number of workers per hour.
- `MAX_WORKERS`: Maximum number of workers per hour.
- `MAX_UNAVAILABILITY`: Maximum allowed unavailability for an employee.
- `MAX_HOURS`: Maximum working hours per employee.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For any questions or suggestions, please contact [contact@berzantas.com](mailto:contact@berzantas.com).
