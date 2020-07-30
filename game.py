## @file
## @brief `pygame` interface

## @defgroup game Game
## @brief `pygame` interface


import pygame

## @ingroup game
class Game(Object):
    def __init__(self, V):
        Object.__init__(self, V)
        pygame.init()

## @ingroup game
class Display(Game):

    ## @param[in] V
    ## @param[in] W width in pixels
    ## @param[in] H height in pixels
    def __init__(self, V, W=320, H=240):
        Game.__init__(self, V)
        self['W'] = Integer(W)
        self['H'] = Integer(H)

    ## show game window on execution
    def eval(self, ctx):
        W = self['W'].val
        H = self['H'].val
        self.display = pygame.display.set_mode((W, H))
        return self


vm['game'] = Game(MODULE) << Display(MODULE)
