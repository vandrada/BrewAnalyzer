from brewprogram import *

# Class representing a Database object.
name = lambda prog: prog.get_name()

class Database(object):
    def __init__(self):
        '''
        Initializes the Database object: fills in the programs, the
        dependencies, and the uses
        '''
        self.programs = []              # all the programs installed
        self.dependencies = {}          # the deps of all programs installed

        # This is considerably different from a program's uses. While a
        # program's uses are all the uses for all homebrew formulae, this is
        # only the uses for programs that are in the database...maybe this will
        # change
        self.uses = {}

    def build(self):
        '''
        Builds the database of programs and dependencies
        '''
        # builds self.programs
        print "Fetching programs"
        temp = subprocess.check_output(['brew', 'ls'])
        temp = temp.split("\n")
        temp.pop()
        self.programs = [BrewProgram(name) for name in temp]

        # builds self.dependencies
        print "Fetching dependencies"
        self.__build_deps()

        # builds self.uses
        print "Fetching uses"
        self.__build_uses()

        print "Database complete\n"

    def __build_deps(self):
        '''
        Builds a database's dependencies by calling the program's build_deps
        '''
        for program in self.programs:
            program.build_deps()
            self.dependencies[program.get_name()] = program.get_deps()

    def __build_uses(self):
        '''
        Builds a dict where the key are the programs and the values are their
        uses. Unfortunately, this is terribly slow due to the 'brew uses'
        command. This is the main reason why BrewAnalyzer itself writes
        this out.
        '''
        progress = 1
        program_names = map(name, self.programs)
        for program in self.programs:
            print "%d of %d: adding %s" %\
                (progress, self.number_of_programs(), program)
            program.build_uses()
            self.uses[program.get_name()] =\
                [use for use in program.uses if use in program_names]
            progress += 1

    def number_of_programs(self):
        '''
        Returns the amount of programs installed
        '''
        return len(self.programs)

    def number_with_uses(self):
        '''
        Returns the number of programs with uses
        '''
        return len(self.programs_with_uses)

    def number_with_deps(self):
        '''
        Returns the number of programs with deps
        '''
        return len(self.programs_with_deps)

    def number_of_standalones(self):
        '''
        Returns the number of programs that are standlone
        '''
        return len(self.standalones)

    def __repr__(self):
        "%(num)d programs installed." % {"num": self.number_of_programs()}
