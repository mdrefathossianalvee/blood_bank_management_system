### Blood Bank Management System

This Python code implements a Blood Bank Management System using Tkinter for the GUI and SQLite for the database. Below is an explanation of its components:

#### Modules Used:
- `sqlite3`: For database management.
- `tkinter`: For GUI development.
- `datetime`: For handling date and time operations.
- `tkinter.messagebox`: For displaying messages.
- `tkinter.simpledialog`: For creating simple dialogs.

#### Database Connection:
- Connects to a SQLite database named `'Blood_bank_by_mayday.db'`.
- Creates a table named `'BloodBank'` if it doesn't exist with columns: `'DONOR_NAME'`, `'DONOR_CONTACT'` (Primary Key), `'BLOOD_GROUP'`, `'BLOOD_STATUS'`, and `'DATE_TIME'`.

#### Functions:
1. `donor_datetime()`: Returns the current date and time in the format `"%Y-%m-%d %H:%M:%S"`.
2. `display_records()`: Fetches records from the database and displays them in the GUI.
3. `clear_fields()`: Clears the input fields in the GUI.
4. `clear_and_display()`: Clears fields and updates the displayed records.
5. `add_record()`: Adds a new record to the database.
6. `view_record()`: Displays details of a selected record.
7. `update_record()`: Updates the selected record in the database.
8. `remove_record()`: Deletes the selected record from the database.
9. `delete_inventory()`: Deletes all records from the database.
10. `change_availability()`: Toggles the availability status of the selected record.

#### GUI Components:
- **Main Window**: Initializes the main GUI window with specified dimensions and title.
- **Frames**: Divides the window into left, right-top, and right-bottom frames.
- **Labels and Entry Widgets**: Input fields for donor name, contact, blood group, and blood status.
- **Buttons**: For adding, updating, deleting records, clearing fields, and changing availability.
- **Treeview**: Displays records from the database with scrollbars for navigation.

#### StringVars:
- `blood_status`: Stores the blood status (Available/Unavailable).
- `donor_name`: Stores the donor's name.
- `donor_contact`: Stores the donor's contact information.
- `blood_group`: Stores the donor's blood group.

#### Initialization:
- Configures fonts, colors, and dimensions for various GUI components.
- Places components in their respective frames and sets up event handling.

#### Execution:
- Updates the main window and starts the event loop.

This code provides a user-friendly interface for managing blood bank records efficiently.
