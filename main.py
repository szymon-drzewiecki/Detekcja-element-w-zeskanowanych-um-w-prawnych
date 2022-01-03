#from pdf2image import convert_from_path
import os

from poldeepner2 import models

import globals
from rawTextExtraction import *
from regexFunctions import *
from webScraping2 import *

def initModel():
    nkjp = models.load("nkjp-base-sq", device="cpu", resources_path=".\\")
    return nkjp

def findNumbers(sentences):
    globals.NIP_NUMBER_A = findNIPs(sentences[0])
    globals.NIP_NUMBER_B = findNIPs(sentences[1])
    globals.KRS_A = findKRS(sentences[0])
    globals.REGON_A = findREGON(sentences[0])
    globals.KRS_B = findKRS(sentences[1])
    globals.REGON_B = findREGON(sentences[1])

def initModelAndGatherInformation(sentences, nkjp):
    intelList = [nkjp
.process_text(sentences[0][0:200])]
    intelList2 = [nkjp
.process_text(sentences[1][0:200])]
    for intels in intelList:
        findInformationAside(intels)
        printNames(sentences[0], intels)
    for intels in intelList2:
        findInformationBside(intels)
        printNames(sentences[1], intels)



def findNamesAI(stringToFindNames, nkjp):
    if len(stringToFindNames) >= 2:
        namesList = [nkjp
    .process_text(stringToFindNames[0][0:100])]
        namesList2 = [nkjp
    .process_text(stringToFindNames[1][0:100])]
        for name in namesList:
            globals.PERSON_A_NAMES = findNames(name)
        for name in namesList2:
            globals.PERSON_B_NAMES = findNames(name)

def findNames(names):
    listOfNames = []
    for name in names:
        if name.label == "persName":
            listOfNames.append(name.text)
    return listOfNames

def printNames(sentence, names):
    print(sentence)
    print("-"*20)
    for name in names:
        name_range = "%d:%d" % (name.begin, name.end)
        print("%-8s %-20s %s" % (name_range, name.label, name.text))
    print("")

def findInformationAside(names):
    for name in names:
        if globals.PLACE_NAME == "" and name.label == "placeName_settlement":
            globals.PLACE_NAME = name.text
        elif (globals.DATE == "" and name.label == "date") or (len(globals.DATE) > len(name.label) and name.label == "date"):
            globals.DATE = name.text
        elif name.label == "orgName" and "sąd" not in name.text.lower() and "zarząd" not in name.text.lower():
            globals.COMP_A_NAMES.append(name.text)

def findInformationBside(names):
    for name in names:
        if name.label == "orgName" and "sąd" not in name.text.lower() and "zarząd" not in name.text.lower():
            globals.COMP_B_NAMES.append(name.text)


def printInformations():
    stringOfInformation = ""
    if globals.PLACE_NAME != "":
        stringOfInformation = stringOfInformation + "Umowa zawarta w " + globals.PLACE_NAME
    if globals.DATE != "":
        stringOfInformation += " " + globals.DATE 
    stringOfInformation += '\n'
    stringOfInformation = stringOfInformation + globals.SIDE_A_NAME + ":" + '\n'
    if len(globals.COMP_A_NAMES) != 0:
        stringOfInformation += "Nazwa firmy: "
        for name in globals.COMP_A_NAMES:
            stringOfInformation += name + ', '
        stringOfInformation += '\n'
    if len(globals.NIP_NUMBER_A) != 0:
        stringOfInformation += "Numer NIP: "
        for NIP in globals.NIP_NUMBER_A:
            stringOfInformation += NIP + ', '
        stringOfInformation += '\n'
    if len(globals.REGON_A) != 0:
        stringOfInformation += "Numer REGON: "
        for REGON in globals.REGON_A:
            stringOfInformation += REGON + ', '
        stringOfInformation += '\n'
    if len(globals.KRS_A) != 0:
        stringOfInformation += "Numer KRS: "
        for KRS in globals.KRS_A:
            stringOfInformation += KRS + ", "
        stringOfInformation += '\n'
    if len(globals.PERSON_A_NAMES) != 0:
        stringOfInformation += "Strona reprezentowana przez: "
        for name in globals.PERSON_A_NAMES:
            stringOfInformation += name + ', '
        stringOfInformation += '\n'

    stringOfInformation += '\n'*2
    stringOfInformation += '--'*10
    stringOfInformation += '\n'*2

    stringOfInformation += globals.SIDE_B_NAME + ':\n'
    if len(globals.COMP_B_NAMES) != 0:
        stringOfInformation += "Nazwa firmy:"
        for name in globals.COMP_B_NAMES:
            stringOfInformation += name + ', '
        stringOfInformation += '\n'
    if len(globals.NIP_NUMBER_B) != 0:
        stringOfInformation += "Numer NIP:"
        for NIP in globals.NIP_NUMBER_B:
            stringOfInformation += NIP + ', '
        stringOfInformation += '\n'
    if len(globals.REGON_B) != 0:
        stringOfInformation += "Numer REGON:"
        for REGON in globals.REGON_B:
            stringOfInformation += REGON + ', '
        stringOfInformation += '\n'
    if len(globals.KRS_B) != 0:
        stringOfInformation += "Numer KRS:"
        for KRS in globals.KRS_B:
            stringOfInformation += KRS + ", "
        stringOfInformation += '\n'
    if len(globals.PERSON_B_NAMES) != 0:
        stringOfInformation += "Strona reprezentowana przez:"
        for name in globals.PERSON_B_NAMES:
            stringOfInformation += name + ', '
        stringOfInformation += '\n'

    return stringOfInformation