import datetime
import sqlite3
from tkcalendar import DateEntry

from tkinter import *
import tkinter.messagebox as mb
import tkinter.ttk as ttk

# Connecting to the Database
connector = sqlite3.connect("Expense Tracker.db")
cursor = connector.cursor()

connector.execute(
	'CREATE TABLE IF NOT EXISTS ExpenseTracker (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Date DATETIME, Payee TEXT, Description TEXT, Amount FLOAT, ModeOfPayment TEXT)'
)
connector.commit()

# Functions
def list_all_expenses():
	global connector, table

	table.delete(*table.get_children())

	all_data = connector.execute('SELECT * FROM ExpenseTracker')
	data = all_data.fetchall()

	for values in data:
		table.insert('', END, values=values)


def view_expense_details():
	global table
	global date, payee, desc, amnt, MoP

	if not table.selection():
		mb.showerror('No expense selected', 'Please select an expense from the table to view its details')

	current_selected_expense = table.item(table.focus())
	values = current_selected_expense['values']

	expenditure_date = datetime.date(int(values[1][:4]), int(values[1][5:7]), int(values[1][8:]))

	date.set_date(expenditure_date) ; payee.set(values[2]) ; desc.set(values[3]) ; amnt.set(values[4]) ; MoP.set(values[5])


def clear_fields():
	global desc, payee, amnt, MoP, date, table

	today_date = datetime.datetime.now().date()

	desc.set('') ; payee.set('') ; amnt.set(0.0) ; MoP.set('Cash'), date.set_date(today_date)
	table.selection_remove(*table.selection())


def remove_expense():
	if not table.selection():
		mb.showerror('No record selected!', 'Please select a record to delete!')
		return

	current_selected_expense = table.item(table.focus())
	values_selected = current_selected_expense['values']

	surety = mb.askyesno('Are you sure?', f'Are you sure that you want to delete the record of {values_selected[2]}')

	if surety:
		connector.execute('DELETE FROM ExpenseTracker WHERE ID=%d' % values_selected[0])
		connector.commit()

		list_all_expenses()
		mb.showinfo('Record deleted successfully!', 'The record you wanted to delete has been deleted successfully')


def remove_all_expenses():
	surety = mb.askyesno('Are you sure?', 'Are you sure that you want to delete all the expense items from the database?', icon='warning')

	if surety:
		table.delete(*table.get_children())

		connector.execute('DELETE FROM ExpenseTracker')
		connector.commit()

		clear_fields()
		list_all_expenses()
		mb.showinfo('All Expenses deleted', 'All the expenses were successfully deleted')
	else:
		mb.showinfo('Ok then', 'The task was aborted and no expense was deleted!')


def add_another_expense():
	global date, payee, desc, amnt, MoP
	global connector

	if not date.get() or not payee.get() or not desc.get() or not amnt.get() or not MoP.get():
		mb.showerror('Fields empty!', "Please fill all the missing fields before pressing the add button!")
	else:
		connector.execute(
		'INSERT INTO ExpenseTracker (Date, Payee, Description, Amount, ModeOfPayment) VALUES (?, ?, ?, ?, ?)',
		(date.get_date(), payee.get(), desc.get(), amnt.get(), MoP.get())
		)
		connector.commit()

		clear_fields()
		list_all_expenses()
		mb.showinfo('Expense added', 'The expense whose details you just entered has been added to the database')


def edit_expense():
	global table

	def edit_existing_expense():
		global date, amnt, desc, payee, MoP
		global connector, table

		current_selected_expense = table.item(table.focus())
		contents = current_selected_expense['values']

		connector.execute('UPDATE ExpenseTracker SET Date = ?, Payee = ?, Description = ?, Amount = ?, ModeOfPayment = ? WHERE ID = ?',
		                  (date.get_date(), payee.get(), desc.get(), amnt.get(), MoP.get(), contents[0]))
		connector.commit()

		clear_fields()
		list_all_expenses()

		mb.showinfo('Data edited', 'We have updated the data and stored in the database as you wanted')
		edit_btn.destroy()
		return

	if not table.selection():
		mb.showerror('No expense selected!', 'You have not selected any expense in the table for us to edit; please do that!')
		return

	view_expense_details()

	edit_btn = Button(data_entry_frame, text='Edit expense', font=btn_font, width=30,
	                  bg=hlb_btn_bg, command=edit_existing_expense)
	edit_btn.place(x=10, y=395)


def selected_expense_to_words():
	global table

	if not table.selection():
		mb.showerror('No expense selected!', 'Please select an expense from the table for us to read')
		return

	current_selected_expense = table.item(table.focus())
	values = current_selected_expense['values']

	message = f'Your expense can be read like: \n"You paid {values[4]} to {values[2]} for {values[3]} on {values[1]} via {values[5]}"'

	mb.showinfo('Here\'s how to read your expense', message)


def expense_to_words_before_adding():
	global date, desc, amnt, payee, MoP

	if not date or not desc or not amnt or not payee or not MoP:
		mb.showerror('Incomplete data', 'The data is incomplete, meaning fill all the fields first!')

	message = f'Your expense can be read like: \n"You paid {amnt.get()} to {payee.get()} for {desc.get()} on {date.get_date()} via {MoP.get()}"'

	add_question = mb.askyesno('Read your record like: ', f'{message}\n\nShould I add it to the database?')

	if add_question:
		add_another_expense()
	else:
		mb.showinfo('Ok', 'Please take your time to add this record')


# Backgrounds anf Fonts
dataentery_frame_bg = 'Red'
buttons_frame_bg = 'Tomato'
hlb_btn_bg = 'IndianRed'

lbl_font = ('Georgia', 13)
entry_font = 'Times 13 bold'
btn_font = ('Gill Sans MT', 13)

# Initializing the GUI window
root = Tk()
root.title('PythonGeeks Expense Tracker')
root.geometry('1200x550')
root.resizable(0, 0)

Label(root, text='EXPENSE TRACKER', font=('Noto Sans CJK TC', 15, 'bold'), bg=hlb_btn_bg).pack(side=TOP, fill=X)

# StringVar and DoubleVar variables
desc = StringVar()
amnt = DoubleVar()
payee = StringVar()
MoP = StringVar(value='Cash')

# Frames
data_entry_frame = Frame(root, bg=dataentery_frame_bg)
data_entry_frame.place(x=0, y=30, relheight=0.95, relwidth=0.25)

buttons_frame = Frame(root, bg=buttons_frame_bg)
buttons_frame.place(relx=0.25, rely=0.05, relwidth=0.75, relheight=0.21)

tree_frame = Frame(root)
tree_frame.place(relx=0.25, rely=0.26, relwidth=0.75, relheight=0.74)

# Data Entry Frame
Label(data_entry_frame, text='Date (M/DD/YY) :', font=lbl_font, bg=dataentery_frame_bg).place(x=10, y=50)
date = DateEntry(data_entry_frame, date=datetime.datetime.now().date(), font=entry_font)
date.place(x=160, y=50)

Label(data_entry_frame, text='Payee\t             :', font=lbl_font, bg=dataentery_frame_bg).place(x=10, y=230)
Entry(data_entry_frame, font=entry_font, width=31, text=payee).place(x=10, y=260)

Label(data_entry_frame, text='Description           :', font=lbl_font, bg=dataentery_frame_bg).place(x=10, y=100)
Entry(data_entry_frame, font=entry_font, width=31, text=desc).place(x=10, y=130)

Label(data_entry_frame, text='Amount\t             :', font=lbl_font, bg=dataentery_frame_bg).place(x=10, y=180)
Entry(data_entry_frame, font=entry_font, width=14, text=amnt).place(x=160, y=180)

Label(data_entry_frame, text='Mode of Payment:', font=lbl_font, bg=dataentery_frame_bg).place(x=10, y=310)
dd1 = OptionMenu(data_entry_frame, MoP, *['Cash', 'Cheque', 'Credit Card', 'Debit Card', 'Paytm', 'Google Pay', 'Razorpay'])
dd1.place(x=160, y=305)     ;     dd1.configure(width=10, font=entry_font)

Button(data_entry_frame, text='Add expense', command=add_another_expense, font=btn_font, width=30,
       bg=hlb_btn_bg).place(x=10, y=395)
Button(data_entry_frame, text='Convert to words before adding', font=btn_font, width=30, bg=hlb_btn_bg).place(x=10,y=450)

# Buttons' Frame
Button(buttons_frame, text='Delete Expense', font=btn_font, width=25, bg=hlb_btn_bg, command=remove_expense).place(x=30, y=5)

Button(buttons_frame, text='Clear Fields in DataEntry Frame', font=btn_font, width=25, bg=hlb_btn_bg,
       command=clear_fields).place(x=335, y=5)

Button(buttons_frame, text='Delete All Expenses', font=btn_font, width=25, bg=hlb_btn_bg, command=remove_all_expenses).place(x=640, y=5)

Button(buttons_frame, text='View Selected Expense\'s Details', font=btn_font, width=25, bg=hlb_btn_bg,
       command=view_expense_details).place(x=30, y=65)

Button(buttons_frame, text='Edit Selected Expense', command=edit_expense, font=btn_font, width=25, bg=hlb_btn_bg).place(x=335,y=65)

Button(buttons_frame, text='Convert Expense to a sentence', font=btn_font, width=25, bg=hlb_btn_bg,
       command=selected_expense_to_words).place(x=640, y=65)

# Treeview Frame
table = ttk.Treeview(tree_frame, selectmode=BROWSE, columns=('ID', 'Date', 'Payee', 'Description', 'Amount', 'Mode of Payment'))

X_Scroller = Scrollbar(table, orient=HORIZONTAL, command=table.xview)
Y_Scroller = Scrollbar(table, orient=VERTICAL, command=table.yview)
X_Scroller.pack(side=BOTTOM, fill=X)
Y_Scroller.pack(side=RIGHT, fill=Y)

table.config(yscrollcommand=Y_Scroller.set, xscrollcommand=X_Scroller.set)

table.heading('ID', text='S No.', anchor=CENTER)
table.heading('Date', text='Date', anchor=CENTER)
table.heading('Payee', text='Payee', anchor=CENTER)
table.heading('Description', text='Description', anchor=CENTER)
table.heading('Amount', text='Amount', anchor=CENTER)
table.heading('Mode of Payment', text='Mode of Payment', anchor=CENTER)

table.column('#0', width=0, stretch=NO)
table.column('#1', width=50, stretch=NO)
table.column('#2', width=95, stretch=NO)  # Date column
table.column('#3', width=150, stretch=NO)  # Payee column
table.column('#4', width=325, stretch=NO)  # Title column
table.column('#5', width=135, stretch=NO)  # Amount column
table.column('#6', width=125, stretch=NO)  # Mode of Payment column

table.place(relx=0, y=0, relheight=1, relwidth=1)

list_all_expenses()

# Finalizing the GUI window
root.update()
root.mainloop()
