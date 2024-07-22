import os
from pprint import pprint
from typing import Any
import toml #type: ignore
import grammar as grammar
import sys
import pickle

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



Usage = "Usage: command cfg:[*.toml] grammar:[*.gram]"

if len(sys.argv[1:]) == 0:
    print(Usage)
    exit(0)


arguments = GetKeywordArgument()

arguments = Expect(arguments,"cfg")
arguments = Expect(arguments,"grammar")

if not os.path.exists(arguments["cfg"]) or \
    not os.path.exists(arguments["grammar"]):
        print("cfg and grammar has to be a path to a valid file or valid symlink.")
        exit(1)

grams = grammar.NewGrammar(arguments["grammar"])
cfg = toml.load(arguments["cfg"])


OUTPUT_FILE = "out.pkl"

if "output" in cfg:
    OUTPUT_FILE = cfg["output"]

if "entry" not in cfg:
    print("entry not found in cfg!")
    exit(1)

Compiled: dict[str,Any] = {}

Compiled["lines"] = grams[cfg["entry"]]

with open(OUTPUT_FILE,"wb") as output:
    pickle.dump(Compiled,output)
