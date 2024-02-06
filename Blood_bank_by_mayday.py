# Importing all necessary modules
import sqlite3
from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as mb
import tkinter.simpledialog as sd
from datetime import datetime, timedelta

# Connecting to Database
connector = sqlite3.connect('Blood_bank_by_mayday.db')
cursor = connector.cursor()

connector.execute(
    'CREATE TABLE IF NOT EXISTS BloodBank (DONOR_NAME TEXT, DONOR_CONTACT TEXT PRIMARY KEY NOT NULL, BLOOD_GROUP TEXT, BLOOD_STATUS TEXT, DATE_TIME TEXT)'
)

# Functions
def donor_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def display_records():
    global connector, cursor
    global tree

    tree.delete(*tree.get_children())

    curr = connector.execute('SELECT * FROM BloodBank ORDER BY BLOOD_STATUS ASC')
    data = curr.fetchall()

    for records in data:
        tree.insert('', END, values=records)


def clear_fields():
    global donor_contact, donor_name, blood_group, blood_status

    blood_status.set('Available')
    for i in ['donor_contact', 'donor_name', 'blood_group']:
        exec(f"{i}.set('')")


def clear_and_display():
    clear_fields()
    display_records()


def add_record():
    global connector
    global donor_name, donor_contact, blood_group, blood_status

    if blood_status.get() == 'Unavailable':
        date_time = donor_datetime()
    else:
        date_time = 'N/A'

    surety = mb.askyesno('Are you sure?',
                'Are you sure this is the data you want to enter?\nPlease note that Donor Contact cannot be changed in the future')

    if surety:
        try:
            connector.execute(
                'INSERT INTO BloodBank (DONOR_NAME, DONOR_CONTACT, BLOOD_GROUP, BLOOD_STATUS, DATE_TIME) VALUES (?, ?, ?, ?, ?)',
                (donor_name.get(), donor_contact.get(), blood_group.get(), blood_status.get(), date_time))
            connector.commit()

            clear_and_display()

            mb.showinfo('Record added', 'The new record was successfully added to your database')
        except sqlite3.IntegrityError:
            mb.showerror('Donor Contact already in use!',
                         'The Donor Contact you are trying to enter is already in the database, please alter that donor\'s record or check any discrepancies on your side')


def view_record():
    global donor_name, donor_contact, blood_group, blood_status
    global tree

    if not tree.focus():
        mb.showerror('Select a row!', 'To view a record, you must select it in the table. Please do so before continuing.')
        return

    current_item_selected = tree.focus()
    values_in_selected_item = tree.item(current_item_selected)
    selection = values_in_selected_item['values']

    donor_name.set(selection[0])
    donor_contact.set(selection[1])
    blood_group.set(selection[2])
    blood_status.set(selection[3])


def update_record():
    def update():
        global donor_name, donor_contact, blood_group, blood_status
        global connector, tree

        if blood_status.get() == 'Unavailable':
            date_time = donor_datetime()
            cursor.execute('UPDATE BloodBank SET DONOR_NAME=?, BLOOD_GROUP=?, BLOOD_STATUS=?, DATE_TIME=? WHERE DONOR_CONTACT=?',
                           (donor_name.get(), blood_group.get(), blood_status.get(), date_time, donor_contact.get()))
        else:
            cursor.execute('UPDATE BloodBank SET DONOR_NAME=?, BLOOD_GROUP=?, BLOOD_STATUS=? WHERE DONOR_CONTACT=?',
                           (donor_name.get(), blood_group.get(), blood_status.get(), donor_contact.get()))
        
        connector.commit()

        clear_and_display()

        edit.destroy()

    view_record()

    edit = Button(left_frame, text='Update Record', font=btn_font, bg=btn_hlb_bg, width=20, command=update)
    edit.place(x=50, y=375)


def remove_record():
    if not tree.selection():
        mb.showerror('Error!', 'Please select an item from the database')
        return

    current_item = tree.focus()
    values = tree.item(current_item)
    selection = values["values"]

    cursor.execute('DELETE FROM BloodBank WHERE DONOR_CONTACT=?', (selection[1], ))
    connector.commit()

    tree.delete(current_item)

    mb.showinfo('Done', 'The record you wanted deleted was successfully deleted.')

    clear_and_display()


def delete_inventory():
    if mb.askyesno('Are you sure?', 'Are you sure you want to delete the entire inventory?\n\nThis command cannot be reversed'):
        tree.delete(*tree.get_children())

        cursor.execute('DELETE FROM BloodBank')
        connector.commit()
    else:
        return


def change_availability():
    global donor_contact, tree, connector

    if not tree.selection():
        mb.showerror('Error!', 'Please select a donor from the database')
        return

    current_item = tree.focus()
    values = tree.item(current_item)
    donor_contact = values['values'][1]
    blood_status = values["values"][3]

    if blood_status == 'Available':
        cursor.execute('UPDATE BloodBank SET BLOOD_STATUS=?, DATE_TIME=? WHERE DONOR_CONTACT=?', ('Unavailable', donor_datetime(), donor_contact))
    else:
        cursor.execute('UPDATE BloodBank SET BLOOD_STATUS=?, DATE_TIME=? WHERE DONOR_CONTACT=?', ('Available', 'N/A', donor_contact))

    connector.commit()

    clear_and_display()


# Variables
lf_bg = 'LightSkyBlue'  # Left Frame Background Color
rtf_bg = 'DeepSkyBlue'  # Right Top Frame Background Color
rbf_bg = 'DodgerBlue'  # Right Bottom Frame Background Color
btn_hlb_bg = 'SteelBlue'  # Background color for Head Labels and Buttons

lbl_font = ('Georgia', 13)  # Font for all labels
entry_font = ('Times New Roman', 12)  # Font for all Entry widgets
btn_font = ('Gill Sans MT', 13)

# Initializing the main GUI window
root = Tk()
root.title('Blood Bank Management System')
root.geometry('1010x530')
root.resizable(0, 0)

Label(root, text='BLOOD BANK MANAGEMENT SYSTEM', font=("Noto Sans CJK TC", 15, 'bold'), bg=btn_hlb_bg, fg='White').pack(side=TOP, fill=X)

# StringVars
blood_status = StringVar()
donor_name = StringVar()
donor_contact = StringVar()
blood_group = StringVar()

# Frames
left_frame = Frame(root, bg=lf_bg)
left_frame.place(x=0, y=30, relwidth=0.3, relheight=0.96)

RT_frame = Frame(root, bg=rtf_bg)
RT_frame.place(relx=0.3, y=30, relheight=0.2, relwidth=0.7)

RB_frame = Frame(root)
RB_frame.place(relx=0.3, rely=0.24, relheight=0.785, relwidth=0.7)

# Left Frame
Label(left_frame, text='Donor Name', bg=lf_bg, font=lbl_font).place(x=98, y=25)
Entry(left_frame, width=25, font=entry_font, text=donor_name).place(x=45, y=55)

Label(left_frame, text='Donor Contact', bg=lf_bg, font=lbl_font).place(x=75, y=105)
Entry(left_frame, width=25, font=entry_font, text=donor_contact).place(x=45, y=135)

Label(left_frame, text='Blood Group', bg=lf_bg, font=lbl_font).place(x=95, y=185)
Entry(left_frame, width=25, font=entry_font, text=blood_group).place(x=45, y=215)

Label(left_frame, text='Status of the Blood', bg=lf_bg, font=lbl_font).place(x=65, y=265)
dd = OptionMenu(left_frame, blood_status, *['Available', 'Unavailable'])
dd.configure(font=entry_font, width=12)
dd.place(x=75, y=300)

submit = Button(left_frame, text='Add new record', font=btn_font, bg=btn_hlb_bg, width=20, command=add_record)
submit.place(x=50, y=375)

clear = Button(left_frame, text='Clear fields', font=btn_font, bg=btn_hlb_bg, width=20, command=clear_fields)
clear.place(x=50, y=435)

# Right Top Frame
Button(RT_frame, text='Delete blood record', font=btn_font, bg=btn_hlb_bg, width=17, command=remove_record).place(x=8, y=30)
Button(RT_frame, text='Delete full inventory', font=btn_font, bg=btn_hlb_bg, width=17, command=delete_inventory).place(x=178, y=30)
Button(RT_frame, text='Update blood details', font=btn_font, bg=btn_hlb_bg, width=17,
       command=update_record).place(x=348, y=30)
Button(RT_frame, text='Change Blood Availability', font=btn_font, bg=btn_hlb_bg, width=19,
       command=change_availability).place(x=518, y=30)

# Right Bottom Frame
Label(RB_frame, text='BLOOD INVENTORY', bg=rbf_bg, font=("Noto Sans CJK TC", 15, 'bold')).pack(side=TOP, fill=X)

tree = ttk.Treeview(RB_frame, selectmode=BROWSE, columns=('Donor Name', 'Donor Contact', 'Blood Group', 'Blood Status', 'Date and Time'))

XScrollbar = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
YScrollbar = Scrollbar(tree, orient=VERTICAL, command=tree.yview)
XScrollbar.pack(side=BOTTOM, fill=X)
YScrollbar.pack(side=RIGHT, fill=Y)

tree.config(xscrollcommand=XScrollbar.set, yscrollcommand=YScrollbar.set)

tree.heading('Donor Name', text='Donor Name', anchor=CENTER)
tree.heading('Donor Contact', text='Donor Contact', anchor=CENTER)
tree.heading('Blood Group', text='Blood Group', anchor=CENTER)
tree.heading('Blood Status', text='Status of the Blood', anchor=CENTER)
tree.heading('Date and Time', text='Date and Time', anchor=CENTER)

tree.column('#0', width=0, stretch=NO)
tree.column('#1', width=225, stretch=NO)
tree.column('#2', width=130, stretch=NO)
tree.column('#3', width=100, stretch=NO)
tree.column('#4', width=150, stretch=NO)
tree.column('#5', width=150, stretch=NO)

tree.place(y=30, x=0, relheight=0.9, relwidth=1)

clear_and_display()

# Finalizing the window
root.update()
root.mainloop()
