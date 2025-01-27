import os
import pickle
from pprint import pprint
import random
import sys
from typing import Any



def GetKeywordArgument():
    result = {}
    for item in sys.argv[1:]:
        temp = item.split(":",1)
        result[temp[0]] = temp[1]
        del temp
    return result

def Expect(obj: dict|str|int| list,target: str|int|Any):
    if isinstance(obj,dict) or isinstance(obj,list):
        return obj if target in obj else exit(1)
    elif isinstance(obj,str) or isinstance(obj,int):
        return obj if obj == target else exit(1)


Usage = "Usage: command mode:[{r,l}] lib:[*.pkl] obj:[*.pkl] o:[*]?"

if len(sys.argv[1:]) == 0:
    print(Usage)
    exit(0)


arguments = GetKeywordArgument()

arguments = Expect(arguments,"mode")
arguments = Expect(arguments,"lib")
arguments = Expect(arguments,"obj")
arguments = Expect(arguments,"o")

OUTPUT_FILE = arguments["o"]
mode = arguments["mode"]
if arguments["mode"] not in ["l","r"]:
    print("Invalid Mode!")
    print("""it has to be in these mode:
-r: random
-l: length
""")
    exit(1)

if not os.path.exists(arguments["lib"]) or \
    not os.path.exists(arguments["obj"]):
    print("library and the object file has to be valid file or valid symlink")
    exit(1)


def RandBool():
    return True if random.randint(0,1) == 1 else False

def longest_string(lst):
    return max(lst, key=len)

db = pickle.load(open(arguments["lib"],"rb")) # generated by dbgen
ws = pickle.load(open(arguments["obj"],"rb")) # generated by the compiler



text = ""
#Link The WEIGHTS to DB using the selected mode

pprint(ws)

for node in ws["lines"]:
    if node["atomic"] == True:
        if RandBool() == True:
            continue
    
    book = db[str(node["weight"])]
    
    if mode == "r":
        text += random.choice(book)+" "
    elif mode == "l":
        text += longest_string(book)+" "


#end
with open(arguments["o"],"a") as txt:
    txt.write(text)
