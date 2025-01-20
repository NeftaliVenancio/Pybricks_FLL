from . import Robot

hub = PrimeHub()

bot = Robot()

while True:
    print (bot.button_pressed(Button.LEFT))
