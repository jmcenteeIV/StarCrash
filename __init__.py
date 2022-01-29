from lib.Game import *

game = Game.instance()
game.start_game()

while(True):
  game.loop()