import tkinter as tk
from tkinter import Checkbutton, filedialog, Text, IntVar
import os
from globals import *
from main import *

root = tk.Tk()
i = IntVar()
g = IntVar()
documents=[]
nkjp = initModel()

def chooseFile():
    global documents
    for widget in frame.winfo_children():
        widget.destroy()

    documents = list(filedialog.askopenfilename(multiple=True ,initialdir="/", title="Select File",
    filetypes=(("PDF","*.pdf"), ("JPG", "*.jpg"), ("Microsoft Docx", "*.docx"), ("PNG", "*.png"))))

    while '' in documents:
        documents.remove('')
    for document in documents:
        label = tk.Label(frame, text = document, bg="gray")
        label.pack() 

def clearFilesList():
    global documents
    documents = []
    for widget in frame.winfo_children():
        widget.destroy()
    for document in documents:
        label = tk.Label(frame, text = document, bg="gray")
        label.pack()
    

def checkTheDocumentList():
    global documents
    flagList = [False, False, False, False]
    #flagList[0] = flag for JPG
    #flagList[1] = flag for PNG
    #flagList[2] = flag for PDF
    #flagList[3] = flag for DOCX
    for document in documents:
        if document.lower().endswith(('.jpg', '.jpeg')):
            flagList[0] = True
        if document.lower().endswith('.png'):
            flagList[1] = True
        if document.lower().endswith('.pdf'):
            flagList[2] = True
        if document.lower().endswith('.docx'):
            flagList[3] = True
    x = 0
    for flag in flagList:
        if flag == True:
            x = x + 1
        if x > 1:
            label = tk.Label(outputFrame, text = "Nie można wybierać dokumentów różnych formatów!", bg = "gray")
            label.pack()
            return False
    if (flagList[2] == True and len(documents) > 1) or (flagList[3] == True and len(documents) > 1):
            label = tk.Label(outputFrame, text = "Dokumenty w formacie .pdf lub .docx muszą być dodawane pojedynczo!", bg = "gray")
            label.pack()
            return False
    if flagList[0] == True:
        return "JPG"
    if flagList[1] == True:
        return "PNG"
    if flagList[2] == True:
        return "PDF"
    if flagList[3] == True:
        return "DOCX"

def fallbackMechanism(string):
    initGloblas()
    NIPlist = findNIPs(string)
    KRSlist = findKRS(string)
    REGONlist = findREGON(string)
    
    if len(REGONlist) >= 2:
        globals.REGON_A.append(REGONlist[0])
        globals.REGON_B.append(REGONlist[1])

    if len(KRSlist) >= 2:
        globals.KRS_A.append(KRSlist[0])
        globals.KRS_B.append(KRSlist[1])

    if len(NIPlist) >= 2:
        globals.NIP_NUMBER_A.append(NIPlist[0])
        globals.NIP_NUMBER_B.append(NIPlist[1])

    downloadAddInformation()

def runExtraction():
    initGloblas()
    global documents
    for widget in outputFrame.winfo_children():
        widget.destroy()
    outputText = ""
    while '' in documents:
        documents.remove('')
    if len(documents) == 0:
        outputText = "Nie wybrano żadnych dokumentów"
        outputLabel = tk.Label(outputFrame, text = outputText, bg = "gray")
        outputLabel.pack()
        return None
    elif checkTheDocumentList() == "JPG" or checkTheDocumentList() == "PNG":
        OCRstring = ""
        for document in documents:
            OCRstring += runOCR(document)
    elif checkTheDocumentList() == "PDF":
        OCRstring = extractTextFromPDF(documents[0])
    elif checkTheDocumentList() == "DOCX":
        OCRstring = extractTextFromDocx(documents[0])
    OCRstring =" ".join(OCRstring.split())
    try:
        listOfStrings = findPatternsAndSplitTheDocument2(OCRstring)
        listOfStringsToFindNames = splitTextToFindPersonNames(OCRstring)
        findNumbers(listOfStrings)
        if i.get() == 1:
            if len(listOfStrings) >= 2:
                initModelAndGatherInformation(listOfStrings, nkjp)
            else: initModelAndGatherInformation(OCRstring, nkjp)
            findNamesAI(listOfStringsToFindNames, nkjp)
            downloadAddInformation()
        elif i.get() == 1 and g.get() == 1:
            downloadAddInformation()
        elif g.get() == 1:
            downloadAddInformation()
        else:
            initModelAndGatherInformation(listOfStrings, nkjp)
            findNamesAI(listOfStringsToFindNames, nkjp)
    except:
        fallbackMechanism(OCRstring)
    outputLabel = tk.Label(outputFrame, text = printInformations(), bg = "gray")
    outputLabel.pack()
        


def downloadAddInformation():
    for widget in outputFrame.winfo_children():
        widget.destroy()
    if len(globals.REGON_A) != 0:
        try:
            globals.COMP_A_NAMES, globals.NIP_NUMBER_A, globals.REGON_A = searchForACompanyInfo(globals.REGON_A)
        except:
            a = 1
    elif len(globals.KRS_A):
        try:
            globals.COMP_A_NAMES, globals.NIP_NUMBER_A, globals.REGON_A = searchForACompanyInfo(globals.KRS_A)
        except:
            a = 1
    elif len(globals.NIP_NUMBER_A):
        try:
            globals.COMP_A_NAMES, globals.NIP_NUMBER_A, globals.REGON_A = searchForACompanyInfo(globals.NIP_NUMBER_A)
        except:
            a = 1
    else:
        outputText = """Nie znaleziono numeru NIP/REGON/KRS po którym można by znaleźć informacje.
        Jeśli ekstrakcja nie została uruchomiona, niemożliwe jest znalezienie informacji.
        """
        outputLabel = tk.Label(outputFrame, text = outputText, bg = "gray")
        outputLabel.pack()
    
    if len(globals.KRS_B) != 0:
        try:
            globals.COMP_B_NAMES, globals.NIP_NUMBER_B, globals.REGON_B = searchForACompanyInfo(globals.KRS_B)
        except: a = 1
    elif len(globals.REGON_B):
        try:
            globals.COMP_B_NAMES, globals.NIP_NUMBER_B, globals.REGON_B = searchForACompanyInfo(globals.REGON_B)
        except: a = 1
    elif len(globals.NIP_NUMBER_B):
        try:
            globals.COMP_B_NAMES, globals.NIP_NUMBER_B, globals.REGON_B = searchForACompanyInfo(globals.NIP_NUMBER_B)
        except: a = 1
    else:
        outputText ="""Nie znaleziono numeru NIP/REGON/KRS po którym można by znaleźć informacje.
        Jeśli ekstrakcja nie została uruchomiona, niemożliwe jest znalezienie informacji.
        """
        outputLabel = tk.Label(outputFrame, text = outputText, bg = "gray")
        outputLabel.pack()


def updateInformationUsingWeb():
    downloadAddInformation()
    outputLabel = tk.Label(outputFrame, text = printInformations(), bg = "gray")
    outputLabel.pack()



initGloblas()
root.title("Ekstrakcja informacji z umów")
checkBox = Checkbutton(root, text = "Przeszukaj Internet pod kątem sprawdzenia części informacji o znalezionych firmach", variable=i, padx=10, pady=0)
checkBox.pack()
checkBox2 = Checkbutton(root, text = "Pomiń przeszukiwanie tekstu przy pomocy modelu AI (mniejsza il. informacji)", variable=g, padx=10, pady=0)
checkBox2.pack()
canvas = tk.Canvas(root, height = 1024, width=768, bg="#263D42")
canvas.pack()

openFile = tk.Button(root, text="Otwórz dokument", padx=10, pady=0, fg="#263D42", bg="white", command=chooseFile)
openFile.place(relx=0.1, rely=0.28)
extractInfo = tk.Button(root, text="Wyekstraktuj informacje", padx=10, pady=0, fg="#263D42", bg="white", command= runExtraction)
extractInfo.place(relx=0.7, rely=0.28)
clearFile = tk.Button(root, text="Wyczyść listę dokumentów", padx=10, pady=0, fg="#263D42", bg="white", command = clearFilesList)
clearFile.place(relx=0.38, rely=0.28)
getInfoFromTheWeb = tk.Button(root, text="Zaktualizuj informacje przeszukując Internet", padx=10, pady=0, fg="#263D42", bg="white", command = updateInformationUsingWeb)
getInfoFromTheWeb.place(relx=0.32, rely=0.31)

frame = tk.Frame(root, bg="white")
frame.place(relwidth=0.8, relheight=0.2, relx=0.1, rely=0.05)

outputFrame = tk.Frame(root, bg="white")
outputFrame.place(relwidth=0.8, relheight=0.6, relx=0.1, rely=0.35)



root.mainloop()