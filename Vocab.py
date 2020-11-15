import tkinter as tk
import numpy as np
import random
import pandas as pd
from openpyxl import load_workbook
import xlsxwriter
# This is code is written by Jiali Liang to benefit 
# GRE/SAT students from reciting their vocabs
# I wish you winner winner chicken dinner!

#=========================================================
# General Names
# The .txt file name 
TXT_file_name = 'Kill_GRE.txt'

# .xlsx file name
EXCEL_file_name = 'Kill_GRE.xlsx'

# Title display on the window
TITLE = "加力的單詞本"

# Defualt setting of only review marked vocab

Review_only_marked = True

# Hightlight format
level1_bg_color = '#9bc5eb'
level1_fg_color = '#78021a'
level2_bg_color = '#ba9ded'
level2_fg_color = '#78021a'
level3_bg_color = '#FFC7CE'
level3_fg_color = '#78021a'
level4_bg_color = '#fa3c54'
level4_fg_color = '#78021a'
#=========================================================

#=========================================================
#                    Functions  
#=========================================================
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def save_vocab():

    word = entry[0].get()
    class_word= entry[1].get()
    define = entry[2].get()
    #Vocab_list = [word, class_word, define]
    with open(TXT_file_name, 'a+') as f:
        f.write("%s\t%s\t%s\n" % (word,class_word,define))

    # clear the entry
    entry[0].delete(0, tk.END)
    entry[1].delete(0, tk.END)
    entry[2].delete(0, tk.END)
    TXT2EXCEL()
    
    
def TXT2EXCEL():
    df = pd.read_table(TXT_file_name, sep='\t')#, error_bad_lines=False)

    writer = pd.ExcelWriter(EXCEL_file_name, engine='xlsxwriter')
    df.to_excel(writer, 'Sheet1')
    
    
    # Light red fill with dark red text.

    workbook  = writer.book

    worksheet = writer.sheets['Sheet1']
    
    # Set up different format background
    format1 = workbook.add_format({'bg_color':   level1_bg_color,\
                                   'font_color': level1_fg_color})
        
    format2 = workbook.add_format({'bg_color':   level2_bg_color,\
                                   'font_color': level2_fg_color})  
        
    format3 = workbook.add_format({'bg_color':   level3_bg_color,\
                                   'font_color': level3_fg_color}) 

    format4 = workbook.add_format({'bg_color':   level4_bg_color,\
                                   'font_color': level4_fg_color}) 


    # The order has to be in this format or it would not work
    worksheet.conditional_format('A1:C20000', {'type':     'text',
                                       'criteria': 'containing',
                                       'value':    '++++',
                                       'format':   format4}) 

    worksheet.conditional_format('A1:C20000', {'type':     'text',
                                       'criteria': 'containing',
                                       'value':    '+++',
                                       'format':   format3})       
        
    worksheet.conditional_format('A1:C20000', {'type':     'text',
                                       'criteria': 'containing',
                                       'value':    '++',
                                       'format':   format2})
        
    worksheet.conditional_format('A1:C20000', {'type':     'text',
                                       'criteria': 'containing',
                                       'value':    '+',
                                       'format':   format1})
    



    writer.save()
    

    
def toggle(tog=[0]):
    '''
    a list default argument has a fixed address
    '''
    tog[0] = not tog[0]
    global Review_only_marked
    if tog[0]:
        btn_review_marked.config(text='Review only Marked? : False')
        Review_only_marked = False
        
    else:
        btn_review_marked.config(text='Review only Marked? : True')
        Review_only_marked = True
        
    #print(Review_only_marked)  


def learn_vocab(): 
    learn_vocab.count_learn +=1   
    lbl_defi["text"] = ""

    # The index of all marked vocab
    marked_inx = review_marked()

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
        if Review_only_marked:
            up_limit = len(marked_inx)
        else:
            up_limit = len(learn_vocab.R_word)

        if learn_vocab.num_learn >= up_limit:
            learn_vocab.num_learn = up_limit
    
    
    # in the case of finishing the review goal
    if learn_vocab.count_learn >= learn_vocab.num_learn:
        lbl_Writein["text"] = "You have done great job!\nPlease take a rest!"
        btn_start.destroy()
        btn_show_def.destroy()
        btn_mark.destroy()
        btn_review_marked.destroy()
        
        return
        
    elif learn_vocab.count_learn == 0:
        print("Review only marked = %s "%Review_only_marked) 

        # Review only marked
        if Review_only_marked:
            learn_vocab.random_num = random.sample(marked_inx,learn_vocab.num_learn)
        
        # review all 
        else:    
            learn_vocab.random_num = random.sample(range(0,len(learn_vocab.R_word)),\
                                    learn_vocab.num_learn)
            # Review sequence
            #print(learn_vocab.random_num)
            
    # display the review content
    lbl_Writein["text"] = learn_vocab.R_word[learn_vocab.random_num][learn_vocab.count_learn]
    lbl_Process["text"] = "%s / %s"%(learn_vocab.count_learn+1,learn_vocab.num_learn)
    #enable the show definition buttom to normal
    btn_show_def["state"] = "normal"
    
def show_def():
    # Display the class and definition
    lbl_defi["text"] = learn_vocab.R_class[learn_vocab.random_num][learn_vocab.count_learn] \
    + "   " + learn_vocab.R_define[learn_vocab.random_num][learn_vocab.count_learn]
        # adding the count so we can review the next vocab
     
    #disable the show definition so people won't press accidentally
    btn_show_def["state"] = "disabled"

def search_vocab(data,vocab):
    for i in range(len(data)):
        if vocab in str(data[i]) :
            return str(data[i])

def mark():
    with open(TXT_file_name) as f:
        lines = [line.rstrip() for line in f]
    #print(lines.index(learn_vocab.R_word+"    "+learn_vocab.R_word,learn_vocab.R_class,learn_vocab.R_define))

    word2search = learn_vocab.R_word[learn_vocab.random_num][learn_vocab.count_learn]
    #print("here is word to search %s \n"%word2search)
    sentence_found = search_vocab(lines,word2search)
    inx = lines.index(sentence_found)
    
    #print(lines[inx][0])
    Word,Def = lines[inx].split("\t", 1)[0],lines[inx].split("\t", 1)[1]
    lines[inx] = Word+"+\t"+Def
    #print(lines)
    with open(TXT_file_name, 'w') as f:
        for line in lines:
            f.write(line+'\n')
    f.close()
    TXT2EXCEL()
    
 
    
def review_marked():
    # inx used to store marked vocab's index
    inx = []
    with open(TXT_file_name) as f:
        lines = [line.rstrip() for line in f]
        
    for line in lines:
        if "+" in line:
            inx.append(lines.index(line)-1)
    #print(inx)     
    return inx
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
    entry[idx] = tk.Entry(master=frm_form, width=30)
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
    text="Number of word to review",bg='#FFC0CB',font=("Arial", 20))
lbl_Writein.grid(row=1, column=0, padx=10,sticky="ew")

lbl_Process = tk.Label(master=frm_learn, \
    text="",bg='#FFC0CB',font=("Times", 15))
lbl_Process.grid(row=0, column=0, padx=10,sticky="ew")

# Entry of how many vocabs to learn 
ent_numtolearn = tk.Entry(master=frm_learn, width=10, highlightbackground='#FFC0CB')
ent_numtolearn.grid(row=2, column=0)

frm_button_learn = tk.Frame(bg='#FFC0CB')
frm_button_learn.pack(fill=tk.X, ipadx=5, ipady=5)

frm_button_2nd = tk.Frame(bg='#FFC0CB')
frm_button_2nd.pack(fill=tk.X, ipadx=5, ipady=5)

btn_mark = tk.Button(master=frm_button_2nd, text="Mark"\
                         ,command=mark,fg='#FF9933', highlightbackground='#FFC0CB',width=10)
btn_mark.pack(side=tk.RIGHT, ipadx=5)

btn_review_marked = tk.Button(master=frm_button_2nd,text="Review only Marked? : %s"%(Review_only_marked),\
                  command=toggle,fg='#FF9933', highlightbackground='#FFC0CB',width=18)
btn_review_marked.pack(side=tk.LEFT, ipadx=5)

# Create the "Clear" button and pack it to the
# right side of `frm_buttons`
btn_start = tk.Button(master=frm_button_learn,\
    text="Start Learning", fg="#20B2AA",command=learn_vocab, highlightbackground='#FFC0CB',width=10)
btn_start.pack(side=tk.RIGHT, ipadx=5)
learn_vocab.count_learn = -1

btn_show_def = tk.Button(master=frm_button_learn, text="Show Definition"\
                         ,command=show_def,fg='#87CEFA', highlightbackground='#FFC0CB',width=18)
btn_show_def.pack(side=tk.LEFT, ipadx=5)



'''
frm_button_2nd.columnconfigure(0, weight=1)
frm_button_2nd.columnconfigure(1, weight=1)
btn_review_marked.grid(row=0, column=0, sticky=tk.W+tk.E)
btn_mark.grid(row=0, column=1, sticky=tk.W+tk.E)
'''
# create a label for the showing of definition
lbl_defi = tk.Label(master=frm_learn, text="",bg='#FFC0CB')
lbl_defi.grid(row=3, column=0, padx=10,sticky="ew")

#=========================================================


# Start the application
window.mainloop()
TXT2EXCEL()
