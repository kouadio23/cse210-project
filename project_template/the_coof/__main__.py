import arcade
from data import constants
from workbench import MyGame

import random
SPRITE_SCALING = 0.5

class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture(constants.GAME_SCREEN)

    def on_draw(self):
        arcade.start_render()

        self.texture.draw_sized(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
        arcade.draw_text("Click for Instructions", 380, 100, arcade.color.BLACK, 24)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        instructions_view = InstructionView()
        self.window.show_view(instructions_view)


class InstructionView(arcade.View):
    def __init__(self):
        super().__init__()
        # self.texture = arcade.load_texture(constants.INSTRUCTIONS_SCREEN)

    def on_show(self): # delete when instructions screen is added
        arcade.set_background_color(arcade.color.ORANGE_PEEL)

    def on_draw(self):
        arcade.start_render()

        arcade.draw_text("Instructions Screen", constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2,
                         arcade.color.BLACK, font_size=50, anchor_x="center") # delete when instructions screen is added
        arcade.draw_text("Click to Start Game", 380, 100, arcade.color.BLACK, 24)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        self.window.show_view(game_view)


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        
        # call workbench.py
        # if statement when game quits to redirect to game over screen

        MyGame()
        game_over_view = GameOverView()
        self.window.set_mouse_visible(True)
        self.window.show_view(game_over_view)

    #     # If we've collected all the games, then move to a "GAME_OVER"
    #     # state.
    #     if len(self.coin_list) == 0:
    #         game_over_view = GameOverView()
    #         game_over_view.time_taken = self.time_taken
    #         self.window.set_mouse_visible(True)
    #         self.window.show_view(game_over_view)


class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture(constants.GAME_OVER_SCREEN)

    def on_draw(self):
        arcade.start_render()

        self.texture.draw_sized(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
        arcade.draw_text("Click to Play Again", 400, 100, arcade.color.BLACK, 24)

        # replace with HIGH SCORE
        output_total = f"Total Score: {self.window.total_score:,}"
        arcade.draw_text(output_total, 810, 10, arcade.color.BLACK, 18)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        self.window.show_view(game_view)


def main():
    window = arcade.Window(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, constants.SCREEN_TITLE)
    window.total_score = 0
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()