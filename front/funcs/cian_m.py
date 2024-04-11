from random import randint
import string 

def gimi_smth(x:int):
    no = string.ascii_letters + string.punctuation + ' _-/.,\\'
    xx = ''
    for i in x:
        if i not in no:
            xx += i

    return f'{x}, {42}, {int(xx)}'