import collections
import re
from posixpath import splitdrive
from typing import OrderedDict
from math import fabs

import globals
from numpy import unique

def findNIPs(text):
    NIPs =  re.findall('NIP+[:\d\-\s]+[;,\d.]', text)
    formNIPs = []
    for NIP in NIPs:
        formNIPs.append(re.sub('[\D\n]', '', NIP))
    print(formNIPs)
    formNIPs = unique(formNIPs)
    return formNIPs

def findKRS(text):
    KRSs =  re.findall('KRS+[:\d\-\s]+[;,\d.]', text)
    formKRS = []
    for KRS in KRSs:
        formKRS.append(re.sub('[\D\n]', '', KRS))
    formKRS = unique(formKRS)
    return formKRS

def findREGON(text):
    REGONs =  re.findall('REGON+[:\d\-\s]+[;,\d.]', text)
    formREGON = []
    for REGON in REGONs:
        formREGON.append(re.sub('[\D\n]', '', REGON))
    formREGON = unique(formREGON)
    return formREGON

def findPatternsAndSplitTheDocument2(stringToBeSplitted):
    sideAPossibleKeyWords = ["Zleceniodawcą", "Klientem", "Zamawiającym", "Kontrahentem"]
    sideBPossibleKeyWords = ["Zleceniobiorcą", "Dostawcą", "Wykonawcą"]
    sideAKeyWord = ""
    sideBKeyWord = ""
    splittedText = []
    globals.SIDE_A_NAME = "Zleceniodawca"
    globals.SIDE_B_NAME = "Zleceniobiorca"

    for keyWord in sideAPossibleKeyWords:
        if keyWord in stringToBeSplitted:
            sideAKeyWord = keyWord
            break
    for keyWord in sideBPossibleKeyWords:
        if keyWord in stringToBeSplitted:
            sideBKeyWord = keyWord
            break

    dictionary = {}
    splittingKeyWords = ["zwanym", "zwana", "zwaną"]
    for keyWord in splittingKeyWords:
        x = 0
        while x != -1:
            x = stringToBeSplitted.find(keyWord, x+5)
            if x != -1:
                dictionary[x] = keyWord
    od = collections.OrderedDict(sorted(dictionary.items()))
    
    if sideAKeyWord != "":
        if fabs(stringToBeSplitted.find(sideAKeyWord) - list(od.items())[0][0]) > fabs(stringToBeSplitted.find(sideAKeyWord) - list(od.items())[1][0]):
            globals.SIDE_A_NAME = "Zleceniobiorca"
            globals.SIDE_B_NAME = "Zleceniodawca"
        elif sideBKeyWord != "":
            if fabs(stringToBeSplitted.find(sideBKeyWord) - list(od.items())[0][0]) < fabs(stringToBeSplitted.find(sideBKeyWord) - list(od.items())[1][0]):
                globals.SIDE_A_NAME = "Zleceniobiorca"
                globals.SIDE_B_NAME = "Zleceniodawca"

    tmpSplit = stringToBeSplitted.split(list(od.items())[0][1])
    splittedText.append(tmpSplit[0])
    tmpSplit = tmpSplit[1].split(list(od.items())[1][1])
    splittedText.append(tmpSplit[0])
    return splittedText

def splitTextToFindPersonNames(stringToBeSplitted):
    dictionary = {}
    splittedText = []
    keyWordList = ["reprezentowaną przez", "reprezentowanym przez"]
    for keyWord in keyWordList:
        x = 0
        while x != -1:
            x = stringToBeSplitted.find(keyWord, x+1)
            if x != -1:
                dictionary[x] = keyWord
    od = collections.OrderedDict(sorted(dictionary.items()))
    print(od)
    if len(od) >= 2:
        tmpSplit = stringToBeSplitted.split(list(od.items())[0][1], 1)
        splittedText.append(tmpSplit[1])
        tmpSplit = tmpSplit[1].split(list(od.items())[1][1], 1)
        splittedText.append(tmpSplit[1])
    return splittedText
