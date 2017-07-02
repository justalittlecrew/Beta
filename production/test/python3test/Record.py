def some_func():
	print ("in test 1, unproductive")

def writeRecordToLog(dateAndTime,recordNo,title,type):
	with open("record.log", 'a') as out:
		out.write(dateAndTime +"\t"+ recordNo +"\t" + title + "\t" + type + "\n")
