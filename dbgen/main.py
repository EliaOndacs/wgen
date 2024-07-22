import pickle
import json
import os
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



Usage = "Usage: command db:[*.json] o:[*.pkl]"

if len(sys.argv[1:]) == 0:
    print(Usage)
    exit(0)


arguments = GetKeywordArgument()

arguments = Expect(arguments,"db")
arguments = Expect(arguments,"o")

if not os.path.exists(arguments["db"]):
    print("db has to be a valid file or valid symlink.")
    exit(1)

with open(arguments["db"]) as input_:
    data = json.load(input_)

with open(arguments["o"],"wb") as output:
    pickle.dump(data,output)
