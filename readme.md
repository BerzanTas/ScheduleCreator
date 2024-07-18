![](img/ScheduleCreator.png)
# Schedule Creator

## Overview
The Schedule Creator is a Python-based application designed to create and manage employee work schedules. The program reads an Excel file containing employee availability data, processes the information, and generates a work schedule for the entire month. It also includes a graphical user interface (GUI) for managing employee data and work schedules.

## Features
- **Excel File Processing**: Reads and formats Excel files containing employee availability.
- **Database Management**: Uses SQLite3 to manage employee data.
- **Scheduling Algorithm**: Creates a work schedule based on employee availability, ensuring that constraints like maximum work hours and minimum availability are met.
- **GUI**: Built with Tkinter for user-friendly interaction.

## Project Structure
- `main.py`: Main application file that initializes and runs the program.
- `database.py`: Contains the `EmployeeDB` class for managing the SQLite database.
- `gui.py`: Implements the graphical user interface using Tkinter.
- `scheduleCreator.py`: Contains the `ScheduleCreator` class for generating the work schedule.
- `settings.py`: Configuration file with various settings and constraints.

## Installation
1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/schedule-creator.git
    cd schedule-creator
    ```

2. **Create a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. **Prepare the Excel file**: Ensure the Excel file containing employee availability is formatted correctly and placed in the project directory as `schedule.xlsx`.

2. **Run the application**:
    ```bash
    python main.py
    ```

## Detailed Description
### Excel File Processing
The program reads an Excel file using `pandas`, processes it to enhance readability, and extracts employee availability information. The availability data is then used to generate a work schedule.

### Database Management
The SQLite database is used to store employee information, including their work hours and availability. The `database.py` module handles all database operations such as creating tables, adding records, and fetching data.

### Scheduling Algorithm
The scheduling algorithm considers various constraints such as maximum work hours, minimum number of workers per hour, and employee unavailability. It ensures that the generated schedule meets all these constraints.

### GUI
The GUI, built with Tkinter, provides an interface for users to interact with the application. It allows users to manage employee data and view the generated work schedules.

## Settings
The `settings.py` file contains various configuration options:
- `OPEN_HOUR`: The opening hour of the workday.
- `CLOSE_HOUR`: The closing hour of the workday.
- `MIN_WORKERS`: Minimum number of workers per hour.
- `MAX_WORKERS`: Maximum number of workers per hour.
- `MAX_UNAVAILABILITY`: Maximum allowed unavailability for an employee.
- `MAX_HOURS`: Maximum working hours per employee.

## Contribution
Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For any questions or suggestions, please contact [your email](mailto:youremail@example.com).
