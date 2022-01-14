# Detekcja elementów zeskanowanych umów prawnych

## 1. Instalacja tesseract'a

W pierwszym kroku należy zainstalować oprogramowanie tesseract. Instalator znajduje się w katalogu "need to be installed and added to the PATH". Po zainstalowaniu oprogramowania, należy również dodać program do domyślnej ścieżki, w taki sposób, żeby mógł być on wywoływany w terminalu, niezależnie od katalogu w którym znajduje się użytkownik. 

Instrukcja dla użytkowników korzystających z Windows'a 10. https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/ \
W przypadku systemów Linux wystarczy stworzyć link do programu w katalogu /usr/bin/

## 2. Instalacja modułów do języka python

W celu uruchomienia programu, należy również zainstalować dodatkowe moduły. Można tego dokonać przy pomocy następujących poleceń.
```console
pip install https://pypi.clarin-pl.eu/packages/poldeepner2-0.4.1-py3-none-any.whl#md5=f7780fa6d1feac371fc635b940ecf156
pip install beautifulsoup4
pip install pytesseract
pip install pdfminer
pip install docx2txt
python -m spacy download pl_core_news_sm
python -m spacy link pl_core_news_sm pl_core_news_sm -f
```
Program był testowany jedynie w wersji języka Python 3.8. 

## 3. Uruchomienie programu

Aby uruchomić program, należy z poziomu terminala uruchomić aplikację guiApp.py. 

### Uwaga

W przypadku korzystania z systemu Windows, program może mieć problem z inicjalnym pobraniem modelu sztucznej inteligencji (różnice w slash'ach używanych przy definiowaniu ścieżki w systemach Windows "\" i UNIX "/"). W takim wypadku, jako obejście, można pobrać model pod adresem [nkjp_base_sq](https://drive.google.com/drive/folders/1m57zUdj0sqTlaSCwLLAnUHQpdXN6Umxq?usp=sharing).
