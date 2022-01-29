from lib import game

game_object = game.Game.instance()
game_object.start_game()

while(True):
  game_object.loop()