from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message
import string

class ID_Filter(BaseFilter):

    def __init__(self):
        self.no = string.ascii_letters + string.punctuation + ' _-/.,\\'

    async def __call__(self, message: Message) -> bool:

        text = message.text
        k = ''

        for i in text:
            if i not in self.no:
                k += i
        
        if 7 < len(k) < 10:
            return str(int(k)) == k
        else:
            return False
        
        

class Square_F(BaseFilter):
    def __init__(self):
        self.no = string.ascii_letters + string.punctuation + ' _-/.,\\'


    async def __call__(self, message: Message) -> bool:

        text = message.text
        
        k = ''
        for i in text:
            if i.isdigit():
                k += i
        
        if 1 <=  len(k)  <= 4:
            return str(int(k)) == str(k)
        else:
            return False