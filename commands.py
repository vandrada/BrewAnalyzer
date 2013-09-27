import pickle
from os import mkdir, stat
from stat import ST_MTIME
from os.path import exists
from shutil import rmtree
from database import *
from getpass import getuser

class Commands(object):
    def __init__(self):
        self.user = getuser()
        # File locations
        self.dir_location = "/Users/" + self.user + "/.brew_analyzer"
        self.programs_location = self.dir_location + "/programs.pkl"
        self.dependencies_location = self.dir_location + "/dependencies.pkl"
        self.uses_location = self.dir_location + "/uses.pkl"
        self.mtime_location = self.dir_location + "/mtime.pkl"

        self.db = Database()

        # Etc.
        self.YELLOW = "\x1b[93m"
        self.RED = "\x1b[91m"
        self.CLEAR = "\x1b[0m"

        # Lambda functions
        self.has_deps = lambda prog: self.db.dependencies[name(prog)] != []
        self.has_uses = lambda prog: self.db.uses[name(prog)] != []
        self.is_standalone = lambda prog: not self.has_deps(prog) and \
            not self.has_uses(prog)

    def __writeout(self):
        '''
        Writes the contents of the database to disk
        '''
        # Programs
        programs_out = open(self.programs_location, "wb")
        pickle.dump(self.db.programs, programs_out)
        programs_out.close()
        # Dependencies
        deps_out = open(self.dependencies_location, "wb")
        pickle.dump(self.db.dependencies, deps_out)
        deps_out.close()
        # Uses
        uses_out = open(self.uses_location, "wb")
        pickle.dump(self.db.uses, uses_out)
        uses_out.close()

    def __readin(self):
        '''
        Reads the members of database from a pickle file
        '''
        # Programs
        programs_in = open(self.programs_location, "rb")
        self.db.programs = pickle.load(programs_in)
        programs_in.close()
        # Dependencies
        dependencies_in = open(self.dependencies_location, "rb")
        self.db.dependencies = pickle.load(dependencies_in)
        dependencies_in.close()
        # Uses
        uses_in = open(self.uses_location, "rb")
        self.db.uses = pickle.load(uses_in)
        uses_in.close()

    def __first_run(self):
        '''
        When BrewAnalyzer is started for the first time, this function will be
        ran
        '''
        print "No database was found on disk. Would you like to create one?,",\
            "[y/n]\n *This will reduce the time it takes to load the programs"
        response = raw_input("").upper()
        if response == "Y":
            try:
                # Creates the files
                mkdir(self.dir_location)
                print "Please wait while the database is being built--",\
                        "this can take some time"
                self.db.build()
                self.__writeout()
                print "Files saved to", self.dir_location

                self.__save_mtime()
            except OSError:
                print self.RED + "FAILED TO CREATE PERSISTENT DATABASE" +\
                    self.CLEAR
                # Remove any files that may have been created to prevent hiccups
                rmtree(self.dir_location)
        else:
            print "Ok, a temporary database will now be created"
            self.db.build()

    def __normal_run(self):
        '''
        Under normal conditions, this will be ran on startup
        '''
        # Reads in the past mtime
        mtime_in = open(self.mtime_location, "rb")
        past_mtime = pickle.load(mtime_in)
        mtime_in.close()

        if past_mtime != stat("/usr/local/Cellar/")[ST_MTIME]:
            print "The contents of your Cellar and the database differ",\
                    "\nThe database will be rebuilt"
            #TODO don't destroy everything, just update
            self.create_new_database()
            self.__writeout()
            self.__readin()
            self.__save_mtime()
        else:
            print "Reading database from ", self.dir_location
            self.__readin()
            self.__save_mtime()

    def __save_mtime(self):
        '''
        Saves the current mtime of the Cellar
        '''
        current_mtime = stat("/usr/local/Cellar/")[ST_MTIME]
        mtime_out = open(self.mtime_location, "wb")
        pickle.dump(current_mtime, mtime_out)

    def create_new_database(self):
        '''
        Creates a new persistent database in your home directory
        '''
        print "Removing the old database"
        rmtree(self.dir_location)
        mkdir(self.dir_location)
        print "Recreating the database"
        self.db.build()
        self.__save_mtime()
        self.__writeout()
        self.__readin()

    def reload_database(self):
        self.__readin()

    def init(self):
        '''
        Sets up the commands object
        '''
        def files_exist():
            '''Helper function to avoid a nasty boolean test in init'''
            if not exists(self.dir_location): return False
            elif not exists(self.programs_location): return False
            elif not exists(self.dependencies_location): return False
            elif not exists(self.uses_location): return False
            elif not exists(self.mtime_location): return False
            else: return True

        if not files_exist():
            self.__first_run()
        else:
            self.__normal_run()

    # Callable functions

    def deps(self, name):
        '''
        Prints the dependencies of the specified program
        '''
        try:
            if self.db.dependencies[name]:
                return self.db.dependencies[name]
            else:
                return [""]
        except KeyError:
            print "Program with name \"%s\" not found" %(name)

    def uses(self, name):
        '''
        Prints the uses of the specified program
        '''
        try:
            if self.db.uses[name]:
                return self.db.uses[name]
            else:
                return [""]
        except KeyError:
            print "Program with name \"%s\" not found" %(name)

    def shared_deps(self, prog1, prog2):
        '''
        Prints the dependencies that are shared by the two specified programs
        '''
        try:
            if self.db.dependencies[prog1] or self.db.dependencies[prog2]:
                return [dep for dep in self.db.dependencies[prog1] if dep in
                    self.db.dependencies[prog2]]
            else:
                return [""]
        except KeyError:
            print "Program with name \"%s\" or \"%s\" not found" %(prog1, prog2)

    def shared_uses(self, prog1, prog2):
        '''
        Prints the uses that are shared by the two specified programs
        '''
        try:
            if self.db.uses[prog1] or self.db.uses[prog2]:
                return [use for use in self.db.uses[prog1] if use in \
                    self.db.uses[prog2]]
            else:
                return [""]
        except KeyError:
            print "Program with name \"%s\" or \"%s\" not found" %(prog1, prog2)

    def dependency_tree(self, prog, pre):
        '''
        Prints a programs dependency tree
        '''
        print pre + "+---" + prog
        for dep in self.db.dependencies[prog]:
            self.dependency_tree(dep, (pre + "\t"))

    def only_deps(self):
        '''
        Only prints the programs that have dependencies
        '''
        return map(name, filter(self.has_deps, self.db.programs))

    def only_uses(self):
        '''
        Only prints the programs that have uses
        '''
        return map(name, filter(self.has_uses, self.db.programs))

    def standalone(self):
        '''
        Only prints the programs that have no uses and no dependencies
        '''
        return map(name, filter(self.is_standalone, self.db.programs))

    def rm_question(self, program):
        '''
        Prints what programs would be broken if the specified program is
        deleted. The specified program should be a use
        '''
        return self.db.uses[program]

    def print_programs(self):
        '''
        Prints all the programs that are installed
        '''
        return map(name, self.db.programs)

    # Extra functions

    def print_mug(self):
        '''
        Prints out a cool mug:)
        '''
        # The following ascii mug is courtesy of jgs from
        # http://www.ascii-art.com
        print "     oOOOOOo"
        print "    ,|    oO"
        print "   //|     |"
        print "   \\\\|     |"
        print "    `|     |"
        print "     `-----`  jgs"
        print ""


    def welcome(self):
        self.print_mug()
        print "Welcome to the " + self.YELLOW + "HOMEBREW PROGRAM ANALYZER" +\
            self.CLEAR
        print "Type help for a list of available commands"
