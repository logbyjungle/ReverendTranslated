import re
import sys

with open("languages.txt","r") as file:
    langs = eval(file.read())

for lang in langs.values():
    n_line = 0
    try:
        with open(lang+".txt","r") as file:
            lines = file.readlines()
        for i_line in range(len(lines)):
            if i_line % 3 == 0:
                try:
                    re.compile(lines[i_line])
                except Exception:
                    print(f"REGEX PATTERN ERROR ON LINE {i_line+1} FOR FILE {lang+'.txt'}")
                    print(">>>   " + lines[i_line])
                    sys.exit(1)
            elif i_line % 3 == 2:
                if "---" not in lines[i_line]:
                    print(f'"---" HASNT BEEN FOUND ON LINE {i_line+1} FOR FILE {lang+'.txt'}')
                    print(">>>   " + lines[i_line])
                    sys.exit(1)
    except Exception: pass

sys.exit(0)
