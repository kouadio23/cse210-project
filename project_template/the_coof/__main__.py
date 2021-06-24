# program entry point
import arcade
from data.constants import Constants
from data.character import Character
from data.obstacles import Obstacles
from data.point import Point
from data.score import Score

def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()