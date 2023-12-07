import os
import sys

class	Mkgen:
    def __init__(self, name='main', ext='.cpp') -> None:
        self.name = name
        self.ext = ext
        self.cwd = os.getcwd()
        self.files = []
        self.header = []
        self.scanneDir(self.cwd)
    
    def scanneDir(self, cwd):
        items = os.listdir(cwd)
        for item in items:
            item_dir = os.path.join(cwd, item)
            if os.path.isdir(item_dir):
                self.scanneDir(item_dir)
            elif item_dir.endswith(self.ext):
                self.files.append(item_dir.removeprefix(self.cwd + '/').removesuffix(self.ext))
            elif item_dir.endswith(('.h', '.hpp')):
                self.header.append(item_dir.removeprefix(self.cwd + '/'))
    
    def generateMakefile(self):
        template = f"""\
NAME      = {self.name}
CC        = {'c++ -std=c++98' if self.ext == '.cpp' else 'cc'}
FLAGS     = -Wall -Wextra -Werror
RM        = rm -fr
OBJDIR    = .obj
FILES     = {" ".join(self.files)}
SRC       = $(FILES:={self.ext})
OBJ       = $(addprefix $(OBJDIR)/, $(FILES:=.o))
INCLUEDES = {" ".join(self.header)}

all: $(NAME)

$(NAME): $(OBJ)
\t$(CC) $(OBJ) -o $(NAME)

$(OBJDIR)/%.o: %{self.ext} $(INCLUEDES)
\tmkdir -p $(dir $@)
\t$(CC) $(FLAGS) -c $< -o $@

clean:
\t$(RM) $(OBJDIR) $(OBJ)

fclean: clean
\t$(RM)  $(NAME)

re: fclean all
.PHONY: all clean fclean re
"""
        with open('Makefile', 'w') as mk:
            print(template, file=mk)

if __name__ == '__main__':
    try:
        if len(sys.argv) <= 3:
            generator = Mkgen(*sys.argv[1:])
            generator.generateMakefile()
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)
