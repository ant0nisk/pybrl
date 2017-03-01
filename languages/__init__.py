import os
import builtins

for i in os.listdir(os.path.split(os.path.abspath(__file__))[0]):
    if i.endswith(".py") == False:
        continue
    
    exec("from . import {}".format(i[:-3]))
    exec("builtins.{}={}".format(i[:-3],i[:-3]))

del(i)