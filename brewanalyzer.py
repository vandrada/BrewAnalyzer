#!/usr/bin/env python

import cmd
import commands
import database
from os import popen

__version__ = "0.10"
# gets the size of the terminal to make it all pretty and such
column_size = int(popen('stty size', 'r').read().split()[1])

class BrewAnalyzer(cmd.Cmd):
    # Setup
    def preloop(self):
        comm.welcome()

    def do_quit(self, line):
        '''
        Quits the program
        '''
        return True

    def do_EOF(self, line):
        '''
        Quits the program on EOF
        '''
        return True

    def completedefault(self, text, line, start_index, end_index):
        '''
        Adds cool tab completion
        '''
        if text:
            return [program.get_name() for program in comm.db.programs if
                    program.get_name().startswith(text)]
        else:
            return map(lambda prog: prog.get_name(), comm.db.programs)

    def do_reload(self, line):
        '''
        Reloads the database
        '''
        comm.reload_database()

    def do_create(self, line):
        '''Creates a new persistent database
        '''
        comm.create_new_database()

    # Database
    def do_list(self, line):
        '''
        Prints all the programs installed
        '''
        self.columnize(comm.print_programs(), displaywidth=column_size)

    def do_deps(self, line):
        '''
        Prints the dependencies of a program
        '''
        self.columnize(comm.deps(line), displaywidth=column_size)

    def do_uses(self, line):
        '''
        Prints the uses of a program
        '''
        self.columnize(comm.uses(line), displaywidth=column_size)

    def do_info(self, line):
        '''
        Prints the dependencies and the uses of a program
        '''
        program = line.split()
        if len(program) != 1:
            self.do_help("info")
        else:
            print "Dependencies:"
            self.do_deps(program[0])
            print "\nUses:"
            self.do_uses(program[0])

    def do_sharedDeps(self, line):
        '''
        Prints the dependencies shared by two programs
        '''
        programs = line.split()
        if len(programs) != 2:
            self.do_help("sharedDeps")
        else:
            program1, program2 = programs
            self.columnize(comm.shared_deps(program1, program2),
                    displaywidth=column_size)

    def do_sharedUses(self, line):
        '''
        Prints the uses shared by two programs
        '''
        programs = line.split()
        if len(programs) != 2:
            self.do_help("sharedUses")
        else:
            program1, program2 = programs
            self.columnize(comm.shared_uses(program1, program2),
                    displaywidth=column_size)

    def do_onlyDeps(self, line):
        '''
        Only prints the programs that have dependencies
        '''
        if len(line) != 0:
            self.do_help("onlyDeps")
        else:
            self.columnize(comm.only_deps(), displaywidth=column_size)

    def do_onlyUses(self, line):
        '''
        Only prints the programs with uses
        '''
        if len(line) != 0:
            self.do_help("onlyUses")
        else:
            self.columnize(comm.only_uses(), displaywidth=column_size)

    def do_standalones(self, line):
        '''
        Prints the programs with no dependencies and no uses
        '''
        if len(line) != 0:
            self.do_help("standalones")
        else:
            self.columnize(comm.standalone(), displaywidth=column_size)

    # There has to be a better name for this
    def do_hypotheticalRm(self, line):
        '''
        Prints the programs that will be broken if a program is removed
        '''
        program = line.split()
        if len(program) != 1:
            self.do_help("hypotheticalRm")
        else:
            self.columnize(comm.rm_question(program[0]),
                    displaywidth=column_size)

    def do_tree(self, line):
        '''
        Prints a tree representing the program and it's dependencies
        '''
        comm.dependency_tree(line, "")

if __name__ == "__main__":
    comm = commands.Commands()
    comm.init()
    brew = BrewAnalyzer()
    brew.prompt = "BrewAnalyzer@" + comm.user + ": "
    brew.ruler = "-"
    brew.cmdloop()
