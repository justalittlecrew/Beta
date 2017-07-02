try:
    # for Python2
	from Tkinter import *   ## notice capitalized T in Tkinter 
except ImportError:
    # for Python3
	from tkinter import *   ## notice here too
import easygui
import sys

class Window(Tk):
	def __init__(self, parent):
		Tk.__init__(self, parent)
		self.parent = parent
		self.initialize()

	def initialize(self):
		reload(sys)
		sys.setdefaultencoding("utf-8") 
		self.scrollbar = Scrollbar(self)



		self.mylist = Text(self, yscrollcommand = self.scrollbar.set )
		self.mylist.focus_set()

		self.mylist.insert(END,  "*************** reading list ***************\n")
		self.mylist.insert(END, "No.\tDate\tTitle\tReflection\n")

		with open("a.txt") as f:
			content = f.readlines()	
		count =1

#========================================================== start displaying item
		for p in content: 

			items =  p.split("\t")
			displayReflectionString=  items[2]
			if (len(displayReflectionString)>50):
				displayReflectionString= displayReflectionString[:49] + "...\n"
		
			displayString=items[0] + "\t" + items[1] + "\t" + displayReflectionString.replace("[newLine]"," ")

			self.mylist.insert(END,  "%d\t%s" % (count, displayString))
			count+=1

#========================================================== end displaying item
		self.mylist.config(yscrollcommand=self.scrollbar.set)
		self.mylist.config(state="disabled")

		self.scrollbar.pack( side = RIGHT, fill=Y )
		self.mylist.pack(side=TOP, fill=Y)
		self.scrollbar.config( command = self.mylist.yview )
		#self.geometry("600x400+30+30")

		self.wButton = Button(self, text='Exit', command = self.destroy, bg="red")
		self.wButton.pack(side = RIGHT)


		self.wButton = Button(self, text='Add', command = lambda: self.OnButtonClick(content,"[add]","",self.mylist) )
		self.wButton.pack(side = LEFT)


		self.paddinglabel = Label(self,text="             " ,anchor="w")

		self.paddinglabel.pack(side = LEFT)
		self.wButton = Button(self, text='Edit', command =lambda: self.OnButtonClick(content,"[edit]",self.editNo.get("1.0", "end-1c"),self.mylist))
		
		self.wButton.pack(side = LEFT)

		self.editNo = Text( height=1,width=10)
		self.editNo.pack(side = LEFT)


	def OnButtonClick(self,content,addOrEdit,Num,mylist ):

		#========================================== start input validation
		#print ', '.join(mylist)
		#print("%d",1);
	
		if (addOrEdit =="[edit]" and not Num.isdigit()):
			print("leave")
			easygui.msgbox("Please give a correct input!", title="Warning")
			return
	
		maxNum = len(content)

		if (addOrEdit =="[edit]" and int(Num)>maxNum):
			print("leave")

		#========================================== end input validation
		self.top = Toplevel()
		if (addOrEdit == "[add]"):
	       		self.top.title("Add a new record")
		else:
	       		self.top.title("edit a record")	

		#self.top.geometry("300x150+30+30")
		self.top.transient(self)
		#print Num
	
		'''self.topButton = Button(self.top, text="CLOSE", command = self.OnChildClose)
		self.topButton.pack()'''

		if (addOrEdit == "[add]"):
	   		self.top.l1 = Label(self.top,text="Record Number: %d\n" % (len(content)+1) ,anchor="w")
	   		self.top.l1.pack(fill="x")  
		else:
		   	self.top.l1 = Label(self.top,text="Record Number: %s\n" % (Num) ,anchor="w")
	   		self.top.l1.pack(fill="x")  

		self.top.l2 = Label(self.top,text="Date to read" ,anchor="w")
		self.top.l2.pack(fill="x")  
	
		self.top.t1 = Text(self.top,  height=1,width=40)
		self.top.t1.pack()


		self.top.l3 = Label(self.top, text="Book Name" ,anchor="w")
		self.top.l3.pack(fill="x")  

		self.top.t2 = Text(self.top,  height=1,width=40)
		self.top.t2.pack()

		self.top.l4 = Label(self.top, text="Reflection" ,anchor="w")
		self.top.l4.pack(fill="x")  

		self.top.t3 = Text(self.top,  height=10,width=40)
		self.top.t3.pack()
		if addOrEdit=="[add]":
			self.top.button = Button(self.top, text="Confirm",  bg="green",command = lambda: self.addNewBook(content,self.mylist) ,font=("Arial", 12))
			self.top.button.pack(side=LEFT)
		else:
			self.top.button = Button(self.top, text="Confirm",  bg="green",command = lambda: self.editBook(content,Num,self.mylist) ,font=("Arial", 12))
			self.top.button.pack(side=LEFT)

		self.top.button = Button(self.top, text="Cancel",command = lambda: self.top.destroy(),font=("Arial", 12))
		self.top.button.pack(side=RIGHT)	
	  	

		if addOrEdit=="[edit]":
			count =0
			for p in content: 
				count+=1
				if str(count) == Num:
					items =  p.split("	")
					self.top.t1.insert( 4.0,items[0])
					self.top.t2.insert( 4.0,items[1])
					self.top.t3.insert( 4.0,items[2].replace("[newLine]","\n"))
	

	def addNewBook(self,content,mylist):
		text1 = self.top.t1.get("1.0", "end-1c").replace("\t"," ")
		text2 = self.top.t2.get("1.0", "end-1c").replace("\t"," ")
		text3 = self.top.t3.get("1.0", "end-1c").replace("\t"," ").replace("\n","[newLine]")

		addString = text1 +"\t" + text2+"\t" +  text3.rstrip()+"\n"
	
		#content.append("\n" + addString)
		thefile = open('a.txt', 'w')
		for item in content:
	  		thefile.write("%s" % item)
		thefile.close()
		self.mylist.config(state="normal")
		self.mylist.delete(1.0, END)

		with open("a.txt") as f:
			content = f.readlines()	
		self.mylist.insert(END,  "*************** reading list ***************\n")
		self.mylist.insert(END, "No.\tDate\tTitle\tReflection\n")
		count =1
		for p in content: 
			self.mylist.insert(END,  "%d\t%s" % (count, p))
			count+=1
		self.wButton.config(state='normal')
		self.mylist.config(state="disabled")
		self.OnChildClose()

	def editBook(self,content,Num,mylist):
		text1 = self.top.t1.get("1.0", "end-1c")
		text2 = self.top.t2.get("1.0", "end-1c")
		text3 = self.top.t3.get("1.0", "end-1c").rstrip()
		text3 = self.top.t3.get("1.0", "end-1c").replace("\n","[newLine]")

		while (text3.endswith("[newLine]")):
	   		text3=text3[0:(len(text3)-9)]

		editString = text1 +"\t" + text2+"\t" +  text3 +"\n"

		content[int(Num)-1] = editString
		#print content[int(Num)-1]

		

		thefile = open('a.txt', 'w')
		for item in content:
	  		thefile.write("%s" % item.decode('utf-8').encode('utf-8') )
		thefile.close()
		self.mylist.config(state="normal")
		self.mylist.delete(1.0, END)
		#print "%s" % (mylist.get("1.0", "end-1c"))
		with open("a.txt") as f:
			content = f.readlines()	
		self.mylist.insert(END,  "*************** reading list ***************\n")
		self.mylist.insert(END, "No.\tDate\tTitle\tReflection\n")
		count =1
		for p in content: 

#========================================== debug
			items =  p.split("\t")
			displayReflectionString=  items[2]
			if (len(displayReflectionString)>50):
				displayReflectionString= displayReflectionString[:49] + "...\n"
		
			displayString=items[0] + "\t" + items[1] + "\t" + displayReflectionString.replace("[newLine]"," ")

			self.mylist.insert(END,  "%d\t%s" % (count, displayString.decode("utf-8").encode("utf-8")))
			count+=1
	#========================================== debug

	 	 	#self.mylist.insert(END,  "%d\t%s" % (count, p))
	     	       # count+=1

		self.wButton.config(state='normal')
		self.mylist.config(state="disabled")

		self.OnChildClose()
  

	def OnChildClose(self):

		self.top.destroy()



if __name__ == "__main__":

	window = Window(None)

	window.title("Book Reflection Management System")
 
	w = 600 # width for the Tk root
   
	h = 400 # height for the Tk root
	ws = window.winfo_screenwidth() # width of the screen

	hs = window.winfo_screenheight() # height of the screen
	x = (ws/2) - (w/2)
	y = (hs/2) - (h/2)

	window.geometry('%dx%d+%d+%d' % (w, h, x, y))

	window.mainloop()
