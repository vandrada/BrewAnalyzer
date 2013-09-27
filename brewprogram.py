import subprocess
import re

# Class representing a basic brew program.
class BrewProgram(object):
    def __init__(self, name):
        '''
        Initializes the brew program
        '''
        self.name = name                        # the name of the program
        self.deps = []                          # the program's dependencies
        self.uses = []                          # the program's uses

    def build_deps(self):
        '''
        Gets the dependencies of the program and stores them in deps
        '''
        output = subprocess.check_output(["brew", "deps", str(self.name)])
        self.deps = output.split("\n")
        self.deps.pop()

    def build_uses(self):
        '''
        Gets the uses of the program and stores them in uses
        '''
        # `brew uses` returns all the uses for the program. Obviously, that
        # information is not needed in the database object, but that information
        # is retained in the brewprogram object to preserve OOP purity. The
        # filtering is done on creation of a database
        output = subprocess.check_output(["brew", "uses", str(self.name)])
        self.uses = output.split("\n")
        self.uses.pop()

    def get_deps(self):
        '''
        Returns the program's dependencies
        '''
        return self.deps

    def get_uses(self):
        '''
        Returns the program's uses
        '''
        return self.uses

    def get_name(self):
        '''
        Returns the program's name
        '''
        return self.name

    def number_of_deps(self):
        '''
        Returns the number of dependencies that the program has
        '''
        return len(self.deps)

    def number_of_uses(self):
        '''
        Returns the number of uses that the program has
        '''
        return len(self.uses)

    def __repr__(self):
        return str(self.name)

    def __str__(self):
        return self.name
