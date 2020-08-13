import tkinter as tk
import numpy as np
import random
import pandas as pd

# This is code is written by Jiali Liang to benefit 
# GRE/SAT students from reciting their vocabs
# I wish you winner winner chicken dinner!

#=========================================================
# General Names
TXT_file_name = 'Kill_GRE.txt'
EXCEL_file_name = 'Kill_GRE.xlsx'
TITLE = "加力的單詞本"
#=========================================================

#=========================================================
#                    Functions  
#=========================================================
def save_vocab():

    word = entry[0].get()
    class_word= entry[1].get()
    define = entry[2].get()
    #Vocab_list = [word, class_word, define]
    sp = "    "
    with open(TXT_file_name, 'a+') as f:
        f.write("%s %s %s %s %s\n" % (word,sp,class_word,sp,define))

    # clear the entry
    entry[0].delete(0, tk.END)
    entry[1].delete(0, tk.END)
    entry[2].delete(0, tk.END)
    df = pd.read_table(TXT_file_name, sep='    ')
    df.to_excel(EXCEL_file_name, 'Sheet1')



def learn_vocab():    
    lbl_defi["text"] = ""
    
    # Entering the function first time, we do this:
    if learn_vocab.count_learn == 0:
        # Get the entry of the number of words to review
        learn_vocab.num_learn = int(ent_numtolearn.get())
        if learn_vocab.num_learn == "":
            print("NO")
        # remove the entry window
        ent_numtolearn.destroy()
        btn_start['text'] = 'Next'

        # Read the file that contains the vocab
        learn_vocab.R_word,learn_vocab.R_class,learn_vocab.R_define = \
        np.genfromtxt(TXT_file_name,usecols=(0,1,2),unpack=True,dtype=None,\
                      encoding=None)

        # Case if the num to learn bigger than the actual vocab capacity
        if learn_vocab.num_learn >= len(learn_vocab.R_word):
            learn_vocab.num_learn = len(learn_vocab.R_word)
    
    
    # in the case of finishing the review goal
    if learn_vocab.count_learn >= learn_vocab.num_learn:
        lbl_Writein["text"] = "You have done great job!\nPlease take a rest!"
        btn_start.destroy()
        btn_show_def.destroy()
        return
        
    elif learn_vocab.count_learn == 0:
            learn_vocab.random_num = random.sample(range(0,len(learn_vocab.R_word)),\
                                    learn_vocab.num_learn)
            # Review sequence
            #print(learn_vocab.random_num)
            
    # display the review content
    lbl_Writein["text"] = learn_vocab.R_word[learn_vocab.random_num][learn_vocab.count_learn]
    #enable the show definition buttom to normal
    btn_show_def["state"] = "normal"
    
def show_def():
    # Display the class and definition
    lbl_defi["text"] = learn_vocab.R_class[learn_vocab.random_num][learn_vocab.count_learn] \
    + "   " + learn_vocab.R_define[learn_vocab.random_num][learn_vocab.count_learn]
        # adding the count so we can review the next vocab
    learn_vocab.count_learn +=1
    #disable the show definition so people won't press accidentally
    btn_show_def["state"] = "disabled"
    
    
#=========================================================
#               Save Vocab Frame
#=========================================================
# Create a new window with the title
window = tk.Tk()
window.title(TITLE)
window['background']='#FFC0CB'

# Create a new frame `frm_form` to contain the Label
# and Entry widgets for entering address information.
frm_form = tk.Frame(relief=tk.SUNKEN, borderwidth=3)
# Pack the frame into the window
frm_form.pack()

# List of field labels
labels = [
    "單詞",
    "詞性",
    "翻譯",
]

# Create an Entry widget
entry = [0,0,0]
# Loop over the list of field labels
for idx, text in enumerate(labels):
    # Create a Label widget with the text from the labels list
    label = tk.Label(master=frm_form, text=text)
    # Create an Entry widget
    entry[idx] = tk.Entry(master=frm_form, width=20)
    # Use the grid geometry manager to place the Label and
    # Entry widgets in the row whose index is idx
    label.grid(row=idx, column=0, sticky="e")
    entry[idx].grid(row=idx, column=1)
    
    
#=========================================================
#                    Save Bottom Frame
#=========================================================
# Create a new frame `frm_buttons` to contain the
# Submit and Clear buttons. This frame fills the
# whole window in the horizontal direction and has
# 5 pixels of horizontal and vertical padding.
frm_buttons = tk.Frame(bg='#FFC0CB')
frm_buttons.pack(fill=tk.X, ipadx=5, ipady=5)

# Create the "Save" button and pack it to the
# right side of `frm_buttons`
btn_save = tk.Button(master=frm_buttons, text="Save",\
    command = save_vocab, fg='#66CDAA', highlightbackground='#FFC0CB')
btn_save.pack(side=tk.RIGHT, ipadx=10)



#=========================================================
#                   Review Frame
#=========================================================
# Create a new frame `frm_learn` to learn the vocab
frm_learn = tk.Frame(relief=tk.SUNKEN, width=20,bg='#FFC0CB')
# Pack the frame into the window
frm_learn.pack()

lbl_Writein = tk.Label(master=frm_learn, \
    text="Number of word to review",bg='#FFC0CB')
lbl_Writein.grid(row=0, column=0, padx=10,sticky="ew")

# Entry of how many vocabs to learn 
ent_numtolearn = tk.Entry(master=frm_learn, width=5, highlightbackground='#FFC0CB')
ent_numtolearn.grid(row=1, column=0)

frm_button_learn = tk.Frame(bg='#FFC0CB')
frm_button_learn.pack(fill=tk.X, ipadx=5, ipady=5)
# Create the "Clear" button and pack it to the
# right side of `frm_buttons`
btn_start = tk.Button(master=frm_button_learn,\
    text="Start Learning", fg="#20B2AA",command=learn_vocab, highlightbackground='#FFC0CB')
btn_start.pack(side=tk.RIGHT, ipadx=10)
learn_vocab.count_learn = 0

btn_show_def = tk.Button(master=frm_button_learn, text="Show Definition"\
                         ,command=show_def,fg='#87CEFA', highlightbackground='#FFC0CB')
btn_show_def.pack(side=tk.RIGHT, ipadx=10)

# create a label for the showing of definition
lbl_defi = tk.Label(master=frm_learn, text="",bg='#FFC0CB')
lbl_defi.grid(row=2, column=0, padx=10,sticky="ew")

#=========================================================


# Start the application
window.mainloop()