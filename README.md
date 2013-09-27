#BrewAnalyzer

Analyzes the programs that are installed through the Mac OS X package manager
homebrew. It essentially adds some features that I find helpful.

##Mundane Commands (things that brew already does)
* list
* deps
* uses (this one is a little different)

##Money Commands (the features I find 'helpful')
* shared dependencies between two progams
* shared uses between two uses
* only print programs with uses
* only print programs with dependencies
* print programs with no uses and no dependencies
* print programs that will be broken on the removal of a certain program
