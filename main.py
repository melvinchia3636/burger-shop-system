from tkinter import*
from tkinter import simpledialog
from tkinter import messagebox
import tkinter.ttk as ttk
import os
import tkinter

class _QueryDialog(simpledialog.Dialog):

    def __init__(self, title, prompt,
                 initialvalue=None,
                 minvalue = None, maxvalue = None,
                 parent = None):

        if not parent:
            parent = tkinter._default_root

        self.prompt   = prompt
        self.minvalue = minvalue
        self.maxvalue = maxvalue

        self.initialvalue = initialvalue

        simpledialog.Dialog.__init__(self, parent, title)

    def destroy(self):
        self.spinbox = None
        simpledialog.Dialog.destroy(self)

    def body(self, master):

        w = Label(master, text=self.prompt, justify=LEFT)
        w.grid(row=0, padx=5, sticky=W)

        self.spinbox = ttk.Spinbox(master, name="spinbox", from_=self.minvalue, to=self.maxvalue)
        self.spinbox.grid(row=1, padx=5, sticky=W+E)

        if self.initialvalue is not None:
            self.spinbox.insert(0, self.initialvalue)

        return self.spinbox

    def validate(self):
        try:
            result = self.getresult()
        except ValueError:
            messagebox.showwarning(
                "Illegal value",
                self.errormessage + "\nPlease try again",
                parent = self
            )
            return 0

        if self.minvalue is not None and result < self.minvalue:
            messagebox.showwarning(
                "Too small",
                "The allowed minimum value is %s. "
                "Please try again." % self.minvalue,
                parent = self
            )
            return 0

        if self.maxvalue is not None and result > self.maxvalue:
            messagebox.showwarning(
                "Too large",
                "The allowed maximum value is %s. "
                "Please try again." % self.maxvalue,
                parent = self
            )
            return 0

        self.result = result

        return 1


class _QueryInteger(_QueryDialog):
    errormessage = "Not an integer."

    def getresult(self):
        return self.getint(self.spinbox.get())


def askinteger(title, prompt, **kw):
    '''get an integer from the user

    Arguments:

        title -- the dialog title
        prompt -- the label text
        **kw -- see SimpleDialog class

    Return value is an integer
    '''
    d = _QueryInteger(title, prompt, **kw)
    return d.result	

class main():
	def __init__(self, root):
		self.root = root
		self.root.title('Restaurant Point of Sale System')
		self.root.geometry('1040x500')
		self.root.resizable(0, 0)
		if os.path.exists('items.txt'):
			with open('items.txt', 'r') as file:
				self.data = [[j.strip() for j in i.split(':')] for i in file.readlines()]
		else: raise FileNotFoundError('item.txt not exists!')
		self.menu_frame = Frame(self.root, width=500, height=500)
		self.order_frame = Frame(self.root, width=500, height=500)
		self.menu_scroll = Scrollbar(self.menu_frame, orient=VERTICAL)
		self.order_scroll = Scrollbar(self.order_frame, orient=VERTICAL)
		self.data = [[i[0], float(i[1])] for i in self.data]
		self.title_label = Label(self.root, text='Bert\'s Burgers', font=("calibri",30, 'bold'))
		self.welcome_label = Label(self.root, text='Welcome to Burt\'s Burgers!', font=("calibri",15))
		self.description_label = Label(self.root, anchor='e', text = """Select an item from the right panel and press the Add button to add the item in your order. Your orders will appear on the left panel.
To cancel an order, select the order from the left a and click the Remove button. Press the Proceed button to confirm your order.""", font=("calibri",12))
		self.menu_header_text = ['Item', 'Price']
		self.column_names = ("1", '2')
		self.menu = ttk.Treeview(self.menu_frame, column=self.column_names, selectmode='browse', yscrollcommand=self.menu_scroll.set)
		self.menu.column('#0', width=0, minwidth=0, stretch=NO)
		self.menu_scroll.config(command=self.menu.yview)
		for i in self.column_names:
			self.menu.heading(i, text=self.menu_header_text[int(i)-1])
		self.order_header_text = ['Item', 'Subtotal']
		self.order = ttk.Treeview(self.order_frame, column=self.column_names, selectmode='browse', yscrollcommand=self.order_scroll.set)
		self.order.column('#0', width=0, minwidth=0, stretch=NO)
		self.order_scroll.config(command=self.order.yview)
		for i in self.column_names:
			self.order.heading(i, text=self.order_header_text[int(i)-1])
		for i in self.data:
			self.menu.insert('', END, value=[i[0], 'PHP '+format(i[1], '.2f')])
		self.add_button = Button(self.root, text='Add ->', command=self.add_item)
		self.remove_button = Button(self.root, text='<- Remove', command=self.remove_item)
		self.proceed_button = Button(self.root, text='Proceed', command=self.proceed)

	def widget(self):
		self.title_label.place(relx=0.5, y=50, anchor='center')
		self.welcome_label.place(relx=0.5, y=90, anchor='center')
		self.description_label.place(relx=0.5, y=140, anchor='center')
		self.menu_frame.place(x=30, y=200)
		self.order_frame.place(x=1090, y=200, anchor=NE)
		self.menu.place(x=0, y=0)
		self.order.place(x=0, y=0)
		self.root.update()
		self.menu_scroll.place(x=403, y=0, height=self.menu.winfo_height())
		self.order_scroll.place(x=403, y=0, height=self.order.winfo_height())
		self.add_button.place(relx=0.5, y=250, width=100, anchor='center')
		self.remove_button.place(relx=0.5, y=310, width=100, anchor='center')
		self.proceed_button.place(relx=0.5, y=370, width=100, anchor='center')

	def add_item(self):
		if not self.menu.focus():
			messagebox.showerror('Add Item', 'Please select an item from the left')
			return
		self.cur_item = self.menu.item(self.menu.focus())['values']
		self.amount = simpledialog.askinteger("Add Items","Enter Quantity (1-99)", minvalue=1, maxvalue=99)
		if self.amount:
			self.order.insert('', END, values=[str(self.amount)+' pc(s) '+self.cur_item[0], 'PHP '+str(format(float(self.cur_item[1].replace('PHP ', ''))*self.amount, '.2f'))])

	def remove_item(self):
		if not self.order.selection():
			messagebox.showerror('Remove Order', 'Please select an item from right panel')
			return
		self.order.delete(self.order.selection()[0])

	def proceed(self):
		if not self.order.get_children():
			messagebox.showerror('Confirm Order', 'No orders taken yet. Please take at least one order')
			return
		self.proceed = messagebox.askyesno('Confirm Order', 'Confirm Order?')
		if self.proceed:
			self.show_total_and_discount()
		else:
			return

	def show_total_and_discount(self):
		self.total_amount = sum([float(self.order.item(i)['values'][1].replace('PHP ', '')) for i in self.order.get_children()])
		self.discount_content = ['None', 'Senior (20%)', 'Premium Membership (30%)']
		self.discount_text = 'Total cost is PHP {}\n\nPlease enter which discount code applies:{}\n'.format(format(self.total_amount, '.2f'), ''.join(['\n['+str(i)+'] '+self.discount_content[i] for i in range(len(self.discount_content))]))
		self.discount_code = askinteger('Discount', self.discount_text, minvalue=0, maxvalue=2, initialvalue=0)
		if self.discount_code != None: self.pay(self.discount_code, self.total_amount)

	def pay(self, discount_code, total_amount):
		self.discount = 80 if self.discount_code == 1 else 70 if self.discount_code == 2 else 100
		self.real_amount = total_amount * self.discount / 100
		self.discount_amount = self.total_amount - self.real_amount
		self.paid_money = simpledialog.askinteger('Payment', 'You need to pay PHP {}\nPlease enter your payment:'.format(format(self.real_amount, '.2f')))
		if not self.paid_money:
			messagebox.showerror('Error', 'No payment was given! You need to pay PHP {}'.format(format(self.real_amount, '.2f')))
			self.pay(discount_code, total_amount)
			return
		elif self.paid_money < self.real_amount:
			messagebox.showerror('Error', 'Payment is insuffecient! You need to pay PHP {}'.format(format(self.real_amount, '.2f')))
			self.pay(discount_code, total_amount)

		self.show_receipt(self.discount_code, self.total_amount, self.real_amount, self.paid_money)

	def show_receipt(self, discount_code, total_amount, real_amount, paid_money):
		self.receipt_content = []
		self.receipt_content.append('{:^50}'.format('Bert\'s Burger'))
		self.receipt_content.append('-'*50)
		for i in [self.order.item(i)['values'] for i in self.order.get_children()]:
			self.receipt_content.append(i[0]+' costs '+ i[1])
		self.receipt_content.append('-'*50)
		self.receipt_content.append("Total Cost: PHP {}".format(format(total_amount, '.2f')))
		self.receipt_content.append('Discount: {}'.format(self.discount_content[discount_code]))
		if discount_code != 0:
			self.receipt_content.append('Discounted Price: PHP {}'.format(format(real_amount, '.2f')))
		self.receipt_content.append('Cash Tendered: PHP {}'.format(format(paid_money, '.2f')))
		self.receipt_content.append('Change: PHP {}'.format(format(paid_money-real_amount, '.2f')))
		self.receipt_content.append('-'*50)
		self.receipt_content.append('{:^50}'.format('Thank you for using this facility!'))
		self.receipt_content.append('{:^50}'.format('Come again!'))
		messagebox.showinfo('Receipt', '\n'.join(self.receipt_content))
		self.save_receipt_prompt = messagebox.askyesno('Save Receipt', 'Do you want to save receipt?')
		if self.save_receipt_prompt:
			self.save_receipt(self.receipt_content)

		self.ask_if_again()

	def save_receipt(self, receipt_content):
		with open('receipt.txt', 'w') as file:
			file.write('\n'.join(receipt_content))

	def ask_if_again(self):
		self.again_prompt = messagebox.askyesno('Take Order', 'Thank you for your order! Do you want to use this facility again? Press No to exit this program.')
		if self.again_prompt:
			[self.order.delete(i) for i in self.order.get_children(0)]
		else:
			quit()

	def run(self):
		self.widget()
		self.root.mainloop()

class driver():
	def __init__(self, username, password):
		self.root = Tk()
		self.root.withdraw()
		self.username = simpledialog.askstring('Security Login', 'Enter username:')
		if self.username != username:
			messagebox.showerror('Error', 'Invalid or incorrect username! The program will exit')
			return
		self.password = simpledialog.askstring('Security Login', 'Enter password:', show='*')
		if self.password != password:
			messagebox.showerror('Error', 'Invalid or incorrect password! The program will exit')
			return

		self.root.destroy()

		self.main = main(Tk())
		self.main.run()

app = driver('user1', 'admin123')