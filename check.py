# -*- coding: utf-8 -*-

"""
In __author__  werden die an der Lösung beteiligten Autoren aufgezählt.
Die Notation für einen Autor ist:

__author__ = "Matrikelnummer: Vorname Nachname"

Mehrere Autoren werden durch ein Komma getrennt:

__author__ = "123456: Vojtech Jarnik, 1234567: Robert C. Prim"

Gültige Zeichen:
    Für den Vor- bzw. Nachname sind die Buchstaben A-Z, a-z,
    Leerzeichen, Bindestrich (-) und/oder Punkte (.) erlaubt.
    Die Matrikelnummer besteht aus 6 oder 7 Ziffern.
"""

__author__ = "123456: Carsten Heep"
__copyright__ = "Copyright 2013"
__license__ = "GPL" 
__version__ = "1.0"
__email__ = "cheep@gdv.cs.uni-frankfurt.de"
__status__ = "Prototype"


import ast, os, re

PATTERN = "^(\d{6,7}\ *\:\ [A-Za-z.\ \-]+)\ *(\,\ *\d{6,7}\ *\:\ *[A-Za-z.\ \-]+)*\ "

def check_script(file:str) -> bool:
    '''
Verifies __author__ is set and its value is confirmed by our Pattern.

file:
     The Argument "file" is expected to be of type str.
     It refers to a single Python Script File which is to proof.

return:
     The return type is boolean.
     Its value is True, if __author__ is valid in form of condition, given by 
     the Pattern. False means the opposite.
    '''
    try:
        for node in ast.parse(open(file, "r" ).read()).body:
            if type(node) == ast.Assign and node.targets[0].id == "__author__":
                return bool(re.search(PATTERN, node.value.s))
    except Exception as e:
        print(e, file)
         
    return False

def main(top:str) -> None:
    '''
The main-Function verifies all file, with extentioon '.py' in Directory given 
by top and its Subfolders. Function stops working, as soon as a single check 
fails. In that case a reference to the invalid file will be displayed on the 
Screen.

top:
    The Argument "top" sets the root Directory for checking
    '''
    checked_files = 0
    failed_files = 0
    for dirpath, dirnames, filenames in os.walk(top):
        for file in filter(lambda x: x.endswith('.py'), filenames):
            checked_files += 1
            if not check_script(dirpath + os.sep + file):
                failed_files += 1
                print("Invalid file: {0}".format(dirpath + os.sep + file))
    if failed_files == 0:
        print("Your Code passed the checker!")
    else:
        s = """
Von {0} überprüfen Datei(en) haben {1} Datei(en) die Überprüfung nicht bestanden.
Das entspricht einer Fehlerquote von ~{2:.0%}.
"""
        print(s.format(checked_files, failed_files, failed_files/checked_files))

if __name__ == "__main__":
    import sys
    if sys.version_info.major != 3:
        s = """
Der Test wurde Abgebrochen!
Sie verwenden Python in einer "ungültigen" Version. Ihre Version ist:
{0}.{1}.{2}. In der Veranstalltung wird Bezug auf Version 3.x genommen.
Bitte aktualisieren Sie Ihre installtion.
http://www.python.org/download/releases/3.3.2
"""
        print(s.format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro))
        try:
            import webbrowser
            webbrowser.open_new("http://www.python.org/download/releases/3.3.2")
        except:
            pass
    else:
        if len(sys.argv) == 1:
            main(os.curdir)
        elif len(sys.argv) == 2:
            main(sys.argv[1])
        else:
            s = """
Wird das Script ohne Parameter aufgerufen wird das Verzeichnis in dem sich die 
Datei (check.py) befindet als "root" angenommen und die Suchen startet von dort 
aus für alle Dateien die in diesem Verzeichnisse und allen Unterverzeichnissen 
liegen.
Das Skript kann auch mit einem Parameter gestartet werden, um diese 
"root"-Verzeichnis festzulegen.
Wird das Script mit mehr als einem Parameter gestartet erscheint dieser Text.
"""
            print(s)

