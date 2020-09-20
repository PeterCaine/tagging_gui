from tkinter import *
import tkinter.font as font
import tkinter.scrolledtext as tkscrolled
import pickle
import nltk


def lazy_load(file):
    df =  pickle.load(open(file, 'rb'))
    df=df[['joined_col', 'rating']]
    for text_block, rate in zip(df.joined_col, df.rating):
        sents = nltk.sent_tokenize(text_block)
        out_tups.append([(s, rate) for s in sents])
    return out_tups


def next_sent(sent_rate): 
    global COUNTER
    global SENTENCE
    global RATING
    COUNTER +=1
    SENTENCE = sent_rate[0]
    RATING = sent_rate[1]
    display_window.delete(1.0, END )
    display_window.insert(1.0, SENTENCE)
    temp_list.append(list_o_sents[COUNTER-1])
    

def tag_funct(tag):
    out=((RATING, SENTENCE, tag))
    list_out.append(out)
    display_processed.insert(END, '\n'+str(out[1])+' - '+out[2])
    
    
def back():
    global COUNTER
    global SENTENCE
    if COUNTER>0:
        COUNTER-=1
        sent_rate = list_o_sents[COUNTER-1]
        SENTENCE = sent_rate[0]
        display_window.delete(1.0, END)
        display_window.insert(1.0, SENTENCE)
    
    
def delete_last():
    if len (list_out) > 0:
        del list_out[-1]
    display_processed.delete('end-1l', 'end')
    

def close(list_o_sents, list_out):
    save_out = list(list_o_sents[COUNTER:])  
    pickle.dump(save_out, open("./pick_up.pkl", 'wb'))
    with open('./saved_labelled_texts.txt', 'a') as outfile:
        for tup in list_out:
            tup_to_line = str(tup[0]) + ', '+ str(tup[1]) + ', ' + str(tup[2]) +'\n'
            outfile.write(tup_to_line)
    root.destroy()

####################################################
root = Tk()

# define font
myFont = font.Font(family='Helvetica', size=10, weight='bold')


COUNTER=0

list_out = []
temp_list = []
list_o_sents=pickle.load(open('./pick_up.pkl', 'rb'))

# instantiate the text frames
main_frame = Frame(root, padx=20, pady=20, bg="#d3d8de")
text_frame = LabelFrame(main_frame, text="Text to label", bg="#d3d8de")
start_frame = LabelFrame(main_frame, pady=20, text="Closing will save all entries and prune these sentences from the original dataset (no going back!).", bg="#d3d8de")
frm_jrny=LabelFrame(main_frame, text="Use below to add tags", bg="#d3d8de")
frm_pre=LabelFrame(frm_jrny, text="Extrinsic", bg="#d3d8de")
frm_airport=LabelFrame(frm_jrny, text="Airport", bg="#d3d8de")
frm_on_board=LabelFrame(frm_jrny, text="In Air", bg="#d3d8de")
frm_processed=LabelFrame(main_frame, text="Your selections", bg="#d3d8de")

#layout the frames
main_frame.pack()
text_frame.grid(row=0, columnspan=4)
start_frame.grid(row=1, columnspan=4, padx=15, pady=30)
frm_jrny.grid(row=2)
frm_pre.grid(row=2)
frm_airport.grid(row=2, column=1)
frm_on_board.grid(row=2, column=2)
frm_processed.grid(row=3, columnspan=6)

# widgets
display_window = Text(text_frame, height = 6, width = 66,  wrap=WORD, font=myFont)
but_start = Button(start_frame, text=">>", bg='#76936c', fg='black', width = 20, command=lambda: next_sent(list_o_sents[COUNTER]), font=myFont)
but_back = Button(start_frame, text="<<", bg='#76936c', fg='black', width = 20, command=back, font=myFont)
but_close=Button(start_frame, text="Close", bg='#333333', fg='white', width = 20, command=lambda: close(list_o_sents, list_out), font=myFont)

but_na = Button(frm_jrny, text = "n/a ", bg='#acb9d2', width = 20, command=lambda: tag_funct("na"), font=myFont).grid(row=0, column=0, ipadx=60)

but_buy = Button(frm_pre, text = "Buying",  bg = '#b3d1ff', fg='#005ce6', height = 2, width = 20, command=lambda: tag_funct("Buying")).grid(row=1, column=0, padx=5, pady=5)
but_price = Button(frm_pre, text = "Price",  bg = '#b3d1ff', fg='#005ce6',height = 2, width = 20, command=lambda: tag_funct("Price")).grid(row=2, column=0, padx=5, pady=5)
but_dest = Button(frm_pre, text = "Destination",  bg = '#b3d1ff', fg='#005ce6', height = 2, width = 20, command=lambda: tag_funct("Destination")).grid(row=1, column=1, padx=5, pady=5)
but_supt = Button(frm_pre, text = "Customer support",  bg = '#b3d1ff', fg='#005ce6', height = 2, width = 20, command=lambda: tag_funct("Customer support")).grid(row=2, column=1, padx=5, pady=5)

but_airp = Button(frm_airport, text = "Airport ",  bg = '#66a3ff', fg='white', height = 2, width = 20, command=lambda: tag_funct("Airport ")).grid(row=1, column=0, padx=5, pady=5)
but_loun = Button(frm_airport, text = "Lounge",  bg = '#66a3ff', fg='white', height = 2, width = 20, command=lambda: tag_funct("Lounge")).grid(row=2, column=0, padx=5, pady=5)
but_delays = Button(frm_airport, text = "Flight Delays",  bg = '#66a3ff', fg='white', height = 2, width = 20, command=lambda: tag_funct("Flight Delays")).grid(row=1, column=1, padx=5, pady=5)
but_lugg = Button(frm_airport, text = "Luggage",  bg = '#66a3ff', fg='white', height = 2, width = 20, command=lambda: tag_funct("Luggage")).grid(row=2, column=1, padx=5, pady=5)

but_flight = Button(frm_on_board, text = "Flight",  bg = '#005ce6', fg='white', height = 2, width = 20, command=lambda: tag_funct("Flight")).grid(row=1, column=0, padx=5, pady=5)
but_staff = Button(frm_on_board, text = "Personnel/Service/Staff",  fg='white', bg = '#005ce6', height = 2, width = 20, command=lambda: tag_funct("Personnel/Service/Staff")).grid(row=2, column=0, padx=5, pady=5)
but_asst = Button(frm_on_board, text = "Assistance",  bg = '#005ce6', fg='white', height = 2, width = 20, command=lambda: tag_funct("Assistance")).grid(row=1, column=1, padx=5, pady=5)
but_ovrhd = Button(frm_on_board, text = "Overhead luggage",  bg = '#005ce6', fg='white', height = 2, width = 20, command=lambda: tag_funct("Overhead luggage")).grid(row=2, column=1, padx=5, pady=5)
but_seat = Button(frm_on_board, text = "Seat",  bg = '#005ce6', fg='white', height = 2, width = 20, command=lambda: tag_funct("Seat")).grid(row=1, column=2, padx=5, pady=5)
but_ovrhd = Button(frm_on_board, text = "Food",  bg = '#005ce6', fg='white', height = 2, width = 20, command=lambda: tag_funct("Food")).grid(row=2, column=2, padx=5, pady=5)

display_processed= tkscrolled.ScrolledText(frm_processed, height = 15, width = 100, wrap=WORD, font = ("ariel",11))
but_del = Button(frm_processed, text="Delete last entry", bg='#ff8080', fg='black', width = 20, command=delete_last, font=myFont)


# layout widgets
display_window.grid()
but_back.grid(row=0,column=0, ipadx=30, padx=5)
but_start.grid(row=0,column=1, ipadx=30, padx=5)
but_del.grid(row=0, column=3, ipadx=30, padx=5)
but_close.grid(row=0, column=4, ipadx=30, padx=5)
display_processed.grid(row=0, column=1, ipadx=5, padx=5)
    
root.mainloop()