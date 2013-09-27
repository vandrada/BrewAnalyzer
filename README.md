#BrewAnalyzer
Analyze your brew!  
Part pet-project and part playground to learn Python, BrewAnalyzer analyzes the
packages that you have installed through
[homebrew](https://github.com/mxcl/homebrew). It gives you the ability to check
for shared dependencies or uses between two programs and list programs that
would be broken if a particular program is removed. More features will be
added in the future.

##Redundant Commands
* `list`
List all the commands that you have installed through brew

* `deps <program>`
List all the dependencies of `program`

* `uses <program>`
List all the uses for `program`  
<sub>*This one differs from the native brew version because it only lists the
uses for `program` that you have installed

* `info <program>`
Lists the uses and the dependencies of `program`

##Novel Commands (AKA the 'helpful' features)
* `sharedDeps <program1> <program2>`
Lists all the dependencies that `program1` and `program2` have in common

* `sharedUses <program1> <program2>`
Lists all the uses that `program1` and `program2` have in common

* `onlyDeps`
Only lists the programs that have uses

* `onlyUses`
Only lists the programs that have uses

* `standlones`
Lists the programs that have neither dependencies nor uses

* `hypotheticalRm <program>`
Lists the programs that would be broken if `program` is removed  
<sub>*I know this is a really horrible name, but until more thought goes into
the name, it stands as is

##Database Commands
* `reload`
Reloads the persistent database

* `create`
Creates a new persistent database
