import re
import logging
import subprocess
from subprocess import PIPE

class SnippetGenerator():
    def __init__(self, file):
        with open(file) as fd:
            self.file_content = fd.read()

        self.functions = self.__get_functions()
        

    def __get_functions(self):
        pattern = r".*\(*\);"
        return re.findall(pattern,self.file_content)

    def __get_function_args(self, function):
        pattern = r"\((.*?)\)"
        return re.findall(pattern, function)[0]

    def __get_function_name(self, function):
        pattern = r"(\w+)\("
        return re.findall(pattern,function)[0]

    def __create_args(self, fargs):
        args = ''
        count_args = fargs.count(',') + 2
        for i in range(1,count_args):
            if i == count_args - 1:
                args += '$'+str(i)
            else:
                args += '$'+str(i)+', '

        return args


    def __generate_snippet(self, function):
        
        desc = function
        fname = self.__get_function_name(function)
        fargs = self.__get_function_args(function)
        args = ''
        if fargs != '' and fargs != 'void':
            args = self.__create_args(fargs)

        snippet = "                    \n" \
        f"snippet {fname} \"{desc}\" b \n" \
        f"{fname}({args});\n"              \
        "endsnippet                    \n"

        return snippet

    def generate_snippets(self):

        with open('c.snippet', 'w') as fd:
            for function in self.functions:
                try:
                    snippet = self.__generate_snippet(function)
                    fd.write(snippet)
                except:
                    pass



    def get_name(self,function):
        return self.__get_function_name(function)

    def get_args(self, function):
        return self.__get_function_args(function)
    

if __name__ == '__main__':
    s = SnippetGenerator('esp_wifi.h')
    print(s.functions[19])
    s.generate_snippets()
    #print(s.get_args(s.functions[19]))
    #print(s.get_name(s.functions[19]))
    #print(s.generate_snippet(s.functions[19]))

