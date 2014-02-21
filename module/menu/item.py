import menu

class Item:
    def __init__(self,display_words,onchose_method):
        self.display_words=display_words
        self.onchose_method=onchose_method
    
    def on_chose(self):
        option_str=raw_input("are sure or not:y/n\n")
	y_or_n=option_str.lower()
	if y_or_n == "n":
		return menu.Menu.BACK_STEP
	elif y_or_n!="y":
		return menu.Menu.ASK_AGAIN_STEP        
        return self.onchose_method()
    
    