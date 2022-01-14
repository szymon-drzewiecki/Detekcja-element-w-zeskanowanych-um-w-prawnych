# Detekcja elementów zeskanowanych umów prawnych

## 1. Instalacja tesseract'a

W pierwszym kroku należy zainstalować oprogramowanie tesseract. Instalator znajduje się w katalogu "need to be installed and added to the PATH". Po zainstalowaniu oprogramowania, należy również dodać program do domyślnej ścieżki, w taki sposób, żeby mógł być on wywoływany w terminalu, niezależnie od katalogu w którym znajduje się użytkownik. 

Instrukcja dla użytkowników korzystających z Windows'a 10. https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/ \
W przypadku systemów Linux wystarczy stworzyć link do programu w katalogu /usr/bin/

## 2. Instalacja modułów do języka python

W celu uruchomienia programu, należy również zainstalować dodatkowe moduły. Można tego dokonać przy pomocy następujących poleceń.
```console
pip install poldeepner2
pip install beautifulsoup4
pip install pytesseract
pip install pdfminer
pip install docx2txt
```
Program był testowany jedynie w wersji języka Python 3.8. 

## 3. Uruchomienie programu

Aby uruchomić program, należy z poziomu terminala uruchomić aplikację guiApp.py. 
