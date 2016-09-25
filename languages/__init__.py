import os
import __builtin__

for i in os.listdir('./languages'):
    if i.endswith(".py") == False:
        continue
    
    exec("import {}".format(i[:-3]))
    exec("__builtin__.{}={}".format(i[:-3],i[:-3]))

del(i)