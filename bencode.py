import re

class error(Exception):
    def __init__(self, err):
        Exception.__init__(self)
        self.err = err
    def __str__(self):
        return repr(self.err)



class de_bencode():

    def __init__(self, filepath):
        self.filepath = filepath
        self.file = ''
        for line in open(filepath, 'r'):#read file into memory
            self.file += repr(line)

        #Define constants
        self.BEGIN_INT='i'  #https://wiki.theory.org/BitTorrentSpecification#Integers
        self.BEGIN_LIST = 'l'  #https://wiki.theory.org/BitTorrentSpecification#Lists
        #Dictionary indicators, iterators
        self.DICT_KEY_VAL =  ': ' #https://wiki.theory.org/BitTorrentSpecification#Dictionaries
        self.DICT_LIST_ITEM = ', '
        self.END_DICT = 'e'
        self.BEGIN_DICT = 'd'
        self.DM = re.compile('\d')

    def _decode(self, file_string):
        char = file_string.pop()
        if char == self.BEGIN_DICT:
            h_dict = {}
            char = file_string.pop()
            while char != self.END_DICT:
                file_string.append(char)
                ll = self._decode(file_string)
                h_dict[ll] = self._decode(file_string)
                char = file_string.pop
            return h_dict #return Dictionary

        elif char == self.BEGIN_LIST:
            h_list = []
            char = file_string.pop()  #delete first (last) item
            while char != self.END_DICT: #end of list
                file_string.append(char)
                h_list.append(_decode(file_string))
                char = file_string.pop()
            return h_list

        elif char == self.BEGIN_INT:
            char = file_string.pop()
            cur_int = '' #as string for file_string
            while char != END_DICT:
                cur_int += char
                char = file_string.pop()
            return int(cur_int)

        elif self.DM.search(str(char)):
            print char
            cur_int = ''
            while self.DM.search(char):
                cur_int += char
                char = file_string.pop()
            iters = ''
            for iterator in range(int(cur_int)):
                iters += file_string.pop()
            return iters

        else:
            file_string.remove(char)
            self._decode(file_string)

           #self._decode(file_string.pop())
       raise error("Invalid Input File")#TODO reenable


    def decode(self):
        tl = list(self.file)
        tl.reverse()
        tl = self._decode(tl)
        return tl
