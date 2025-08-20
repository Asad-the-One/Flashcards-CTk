import json
from random import randint
import os
import customtkinter as ctk
import tkinter.font as tkFont

"""

 ██████╗ ██╗   ██╗██╗
██╔════╝ ██║   ██║██║
██║  ███╗██║   ██║██║
██║   ██║██║   ██║██║
╚██████╔╝╚██████╔╝██║
 ╚═════╝  ╚═════╝ ╚═╝
                                        
This is the GUI implementation of the flashcard system.

Todo:
- Add feature to allow user to make their own cards
- Add checkbox to start with English instead
- Home menu with dropdown - different JSON files to choose from to start with

"""

# ----------------------------------

"""
For writing data. "ensure_ascii=False" lets umlauts work.
json.dump(data, f, indent=4, ensure_ascii=False)
"""

# ----------------------------------

# Load JSON
data = {}
def load_json(file):
    global data
    global ks
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
        ks = list(data.keys()) # Each key is the word in English

# ----------------------------------

# Save scores
def save_json(file):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# ----------------------------------

# Main menu
def main_menu():

    # Grab list of JSON files
    jsons = []
    for i in os.listdir():
        if ".json" in i:
            jsons.append(i.replace(".json", ""))

    # Initialise GUI
    win = ctk.CTk()
    win.defaultFont = tkFont.nametofont("TkDefaultFont")
    win.defaultFont.configure(weight=tkFont.BOLD, family="Segoe UI")
    f1 = ctk.CTkFrame(win)
    f1.pack(padx=30, pady=30)

    # Title
    l1 = ctk.CTkLabel(f1, text="Flashcards")
    l1.grid(column=0, row=0, columnspan=2, padx=20, pady=20)

    # Dropdown for test JSON select if there are JSON files
    cb = ctk.CTkComboBox(f1, values=jsons)
    cb.grid(row=1, column=0, columnspan=2, padx=20, pady=20)
    cb.set("")

    # Button to start testing with selected JSON
    def start_testing(file):
        if file != ".json":
            win.destroy()
            testing_gui(file)
    b1 = ctk.CTkButton(f1, text="Start Testing", command=lambda: start_testing(cb.get() + ".json"))
    b1.grid(row=2, column=0, padx=20, pady=20)

    # Button to make new set
    def new_set():
        win.destroy()
        new_set_gui()
    b2 = ctk.CTkButton(f1, text="New Set", command=new_set)
    b2.grid(row=2, column=1, padx=20, pady=20)

    # Button to edit set
    def edit_set():
        win.destroy()
        #edit_set(cb.get() + ".json")
    b3 = ctk.CTkButton(f1, text="Edit Set", command=edit_set)
    b3.grid(row=3, column=0, padx=20, pady=20)

    # Quit
    b4 = ctk.CTkButton(f1, text="Quit", command=win.destroy)
    b4.grid(row=3, column=1, padx=20, pady=20)

    # Loop GUI
    win.mainloop()

# ----------------------------------

# Flashcard testing 
def testing_gui(file):

    # Load JSON
    load_json(file)

    # Initialise GUI
    win = ctk.CTk()
    win.defaultFont = tkFont.nametofont("TkDefaultFont")
    win.defaultFont.configure(weight=tkFont.BOLD, family="Segoe UI")
    f1 = ctk.CTkScrollableFrame(win, width=300, height=500)
    f1.pack(padx=30,pady=30)

    # Get a word

    global word
    word = ""
    def getWord():
        global word
        index = randint(0,len(ks)-1)
        word = ks[index]

        while randint(0, data[word]["score"]) != 0:
            index = randint(0,len(ks)-1)
            word = ks[index]
    getWord()

    # Text Label

    l1 = ctk.CTkLabel(f1, text=word, wraplength=200)
    l1.pack(padx=20, pady=20)

    # Score label

    l2 = ctk.CTkLabel(f1, text="Score: "+str(data[word]["score"]))
    l2.pack()

    # Flip button

    def flip():
        global word
        if l1.cget("text") == word:
            l1.configure(text=data[word]["t"])
        else:
            l1.configure(text=word)
            l2.configure(text="Score: "+str(data[word]["score"]))
    b1 = ctk.CTkButton(f1, text="Flip", command=flip)
    b1.pack(padx=20, pady=20)

    # Correct button

    def correct():
        global word
        data[word]["score"] += 1
        getWord()
        l1.configure(text=word)
        l2.configure(text="Score: "+str(data[word]["score"]))
    b2 = ctk.CTkButton(f1, text="Correct", command=correct)
    b2.pack(padx=20, pady=20)

    # Wrong button

    def wrong():
        global word
        if data[word]["score"] != 0:
            data[word]["score"] -= 1
        getWord()
        l1.configure(text=word)
    b3 = ctk.CTkButton(f1, text="Wrong", command=wrong)
    b3.pack(padx=20, pady=20)

    # Quit button

    def quit():
        win.destroy()
    b4 = ctk.CTkButton(f1, text="Quit", command=quit)
    b4.pack(padx=20, pady=20)

    # GUI loop
    win.mainloop()

    save_json(file)
    main_menu()

# ----------------------------------

# Create new set
def new_set_gui():

    # Define globals
    data = {}

    # Initialise GUI    
    win = ctk.CTk()
    #win.resizable(width=False, height=False)
    win.defaultFont = tkFont.nametofont("TkDefaultFont")
    win.defaultFont.configure(weight=tkFont.BOLD, family="Segoe UI")
    f1 = ctk.CTkFrame(win, width=300, height=500)
    f1.pack(padx=30, pady=30)
    
    # Will be a grid of two columns.

    # Tell user to enter file name
    lname = ctk.CTkLabel(f1, text="Enter the file name. Cannot have ' \\ / : * ? \" < > | '.")
    lname.grid(row=0,column=0,columnspan=2,padx=20,pady=20)

    # File name entry box
    name = ctk.CTkEntry(f1)
    name.grid(column=0,row=1,columnspan=2)

    # Tell user about term and answer
    l1 = ctk.CTkLabel(f1, text="Enter the term and answer.")
    l1.grid(column=0, row=2, columnspan=2, padx=20, pady=20)

    # Titles for both columns
    l2 = ctk.CTkLabel(f1, text="Term")
    l2.grid(column=0, row=3, padx=20, pady=20)
    l3 = ctk.CTkLabel(f1, text="Answer")
    l3.grid(column=1,row=3, padx=20, pady=20)

    # Entry boxes for both column
    eterm = ctk.CTkEntry(f1)
    eterm.grid(column=0, row=4, padx=20, pady=20)
    eanswer = ctk.CTkEntry(f1)
    eanswer.grid(column=1, row=4, padx=20, pady=20)

    # Scrollable frame for existing terms
    f2 = ctk.CTkScrollableFrame(f1)
    f2.grid(column=0, row=5, padx=20, pady=20, columnspan=2, rowspan=3, sticky="ew")
    f2.columnconfigure(0, weight=1)
    f2.columnconfigure(1, weight=1)

    # Add data to the scrollable frame
    def create():
        ks = list(data.keys())
        for i in range(len(ks)):
            ctk.CTkLabel(f2, text=ks[i], wraplength=130).grid(row=i, column=0)
            ctk.CTkLabel(f2, text=data[ks[i]]["t"], wraplength=130).grid(row=i, column=1)
    # Add button
    def add():
        t = [eterm.get(), eanswer.get()]
        if not t[0] == "" and not t[1] == "":
            eterm.delete(0, ctk.END)
            eanswer.delete(0, ctk.END)
            data[t[0]] = {"t": t[1], "score": 0}
            create()
    badd = ctk.CTkButton(f1, text="Add", command=add)
    badd.grid(column=0, row=8, padx=20, pady=20, columnspan=2)
    win.bind("<Return>", lambda x: add())

    # Submit button
    def write_file():
        ok = 1
        filename = name.get()
        for i in "\\/:*?\"<>|":
            if i in filename:
                ok = 0
        if ok == 1 and name.get() != "" and data != {}:
            with open(f"{filename}.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
                win.destroy()
    submit = ctk.CTkButton(f1, text="Submit", command=write_file)
    submit.grid(column=0, row=9, padx=20, pady=20, columnspan=2)

    # Quit button
    begone = ctk.CTkButton(f1, text="Quit", command=win.destroy)
    begone.grid(column=0, row=10, padx=20, pady=20, columnspan=2)

    win.mainloop()

    main_menu()

# ----------------------------------

main_menu()
# i test