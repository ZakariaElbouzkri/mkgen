import os
import sys

HEADER = 1
FILE = 2
ANY = 3

def typeOfFile(item, ext, hExt):
    if (item.endswith(ext)):
        return (FILE)
    elif item.endswith(hExt):
        return (HEADER)
    return (ANY)

def recursivSearch(cwd, ext, hExt, files=[], headers=[]):
    items = os.listdir(cwd)
    for item in items:
        itemdir = os.path.join(cwd, item)
        # ignore file that contains test word
        if itemdir.find("test") != -1:
            continue
        if os.path.isdir(itemdir):
            recursivSearch(itemdir, ext, hExt)
        elif (x:= typeOfFile(itemdir, ext, hExt)) != ANY:
            if x == HEADER:
                headers.append(itemdir)
            else:
                files.append(itemdir)
    return files, headers

def main():
    cwd = os.getcwd()
    args = sys.argv[1:]
    extention = '.c'
    if len(args) >= 1:
        extention = args[0]
    header_extention = ".h" if extention == '.c' else ".hpp"
    files, headerFiles = recursivSearch(cwd, extention, header_extention)
    files, headerFiles = [list(map(lambda x:x.removeprefix(cwd+'/'), files)), 
                        list(map(lambda x:x.removeprefix(cwd+'/'), headerFiles))]
    comp = "gcc" if extention == '.c' else "c++"
    comp += " -Wall -Wextra -Werror"
    if extention == '.cpp': comp += " -std=c++98"
    
    MakeFileTemplate=f"""\
NAME = main
CC   = {comp}
RM   = rm -f
SRCS = {" ".join(files)}
OBJ  = $(SRCS:{extention}=.o)
INC  = {" ".join(headerFiles)}

all: $(NAME)

$(NAME): $(OBJ)
\t$(CC) $^ -o $@

%.o: %{extention} $(INC)
\t$(CC) -c $< -o $@

clean:
\t$(RM) $(OBJ)

fclean: clean
\t$(RM) $(NAME)

re: fclean all

.PHONY: fclean all clean re
"""
    with open("Makefile", "w") as f:
        print(MakeFileTemplate, file=f)
    

if __name__=='__main__':
    main()