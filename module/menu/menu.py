from item import Item


class Menu:
    #step operation success
    SUC_STEP=0    
    #go back to menu
    BACK_STEP=1
    #ask again step cause option wrong
    ASK_AGAIN_STEP=2
    #last step error
    ERROR_STEP=3

    Error1 = "Please Type A Integer\n"
    Error2 = "Please Type A Integer >=1 and %d\n"
    
    FATHER_MENU_NOTICE = "Back To Previous Menu:"
    
    MENU_STR="\n\n\n---------------menu-----------------------"
    
    def __init__(self):
        self.list_item = []
    
    def display(self):
	while True:
	    print(Menu.MENU_STR)
	    for i in range(0,len(self.list_item)):
		print("%d.%s"%(i+1,self.list_item[i].display_words))
	    option=raw_input("chose step and press enter\n")
	    if not option.isdigit():
		print(Menu.Error1)
		continue
	    option_int = int(option)
	    if option_int <1 or option_int >len(self.list_item):
		print(Menu.Error2%(len(self.list_item)))
		continue
	    
	    result=self.list_item[option_int-1].on_chose()
	    if result==Menu.ASK_AGAIN_STEP:
		result=self.list_item[option_int-1].on_chose()
	    if result==Menu.ERROR_STEP:
		print("\n\n!!!!!!!!Last Process Failed!!!!!!!!!!!\n")
	    elif result==Menu.SUC_STEP:
		print("\n\n--------opration success--------")
		
        
    def register_item(self,item):
        self.list_item.append(item)
	
    
def test_on(string):
    print "abc"+string

def testcase1():
    u=Menu()
    item1=Item("abc","input",test_on)
    u.register_item(item1)
    u.display()
    
def main():
	testcase1()

if __name__ == '__main__':
	main()	    
    
    