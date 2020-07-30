## @file
## @brief Redmine API interface for developer

## @defgroup redmine Redmine
## @brief Redmine API interface for developer
## @{

import config

from metaL import *

class Redmine(Object):
    def eval(self, ctx):
        import redminelib as rmine


redmine = Redmine('local')
redmine << Url(config.REDMINE_HOST)
redmine << User(config.REDMINE_USER)
redmine << Pswd(config.REDMINE_PSWD)
print(redmine)
# redmine.eval(vm)

REPL()

## @}
