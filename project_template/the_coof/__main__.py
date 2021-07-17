import arcade
import arcade.gui
from arcade.gui import UIManager
from data import constants
from workbench import MyGame

import random
SPRITE_SCALING = 0.5


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()
        self.texture = arcade.load_texture(constants.GAME_SCREEN)

    def on_draw(self):
        arcade.start_render()

        self.texture.draw_sized(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)

    def on_show_view(self):
        """ Called once when view is activated. """
        self.setup()
    
    def on_hide_view(self):
        self.ui_manager.unregister_handlers()
    
    def setup(self):
        """ Set up this view. """
        self.ui_manager.purge_ui_elements()

        y_slot = self.window.height // 5.5
        left_column_x = self.window.width // 2

        button_normal = arcade.load_texture(':resources:gui_basic_assets/red_button_normal.png')
        hovered_texture = arcade.load_texture(':resources:gui_basic_assets/red_button_hover.png')
        pressed_texture = arcade.load_texture(':resources:gui_basic_assets/red_button_press.png')
        help_button = arcade.gui.UIImageButton(
            center_x=left_column_x,
            center_y=y_slot * 1,
            normal_texture=button_normal,
            hover_texture=hovered_texture,
            press_texture=pressed_texture,
            text='Instructions'
        )
        self.ui_manager.add_ui_element(help_button)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        instructions_view = InstructionView()
        self.window.show_view(instructions_view)


class InstructionView(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()
        self.texture = arcade.load_texture(constants.INSTRUCTIONS_SCREEN)

    def on_draw(self):
        arcade.start_render()

        self.texture.draw_sized(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)

    def on_show_view(self):
        """ Called once when view is activated. """
        self.setup()
    
    def on_hide_view(self):
        self.ui_manager.unregister_handlers()
    
    def setup(self):
        """ Set up this view. """
        self.ui_manager.purge_ui_elements()

        y_slot = self.window.height // 5.5
        left_column_x = self.window.width // 2

        button_normal = arcade.load_texture(':resources:gui_basic_assets/red_button_normal.png')
        hovered_texture = arcade.load_texture(':resources:gui_basic_assets/red_button_hover.png')
        pressed_texture = arcade.load_texture(':resources:gui_basic_assets/red_button_press.png')
        play_button = arcade.gui.UIImageButton(
            center_x=left_column_x,
            center_y=y_slot * 1,
            normal_texture=button_normal,
            hover_texture=hovered_texture,
            press_texture=pressed_texture,
            text='Play'
        )
        self.ui_manager.add_ui_element(play_button)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        self.window.show_view(game_view)


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        # MyGame()
    
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_over_view = GameOverView()
        self.window.show_view(game_over_view)


class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()
        self.texture = arcade.load_texture(constants.GAME_OVER_SCREEN)

    def on_draw(self):
        arcade.start_render()

        self.texture.draw_sized(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)

    def on_show_view(self):
        """ Called once when view is activated. """
        self.setup()
    
    def on_hide_view(self):
        self.ui_manager.unregister_handlers()
    
    def setup(self):
        """ Set up this view. """
        self.ui_manager.purge_ui_elements()

        y_slot = self.window.height // 5.5
        left_column_x = self.window.width // 2

        button_normal = arcade.load_texture(':resources:gui_basic_assets/red_button_normal.png')
        hovered_texture = arcade.load_texture(':resources:gui_basic_assets/red_button_hover.png')
        pressed_texture = arcade.load_texture(':resources:gui_basic_assets/red_button_press.png')
        play_button = arcade.gui.UIImageButton(
            center_x=left_column_x,
            center_y=y_slot * 1,
            normal_texture=button_normal,
            hover_texture=hovered_texture,
            press_texture=pressed_texture,
            text='Play Again'
        )
        self.ui_manager.add_ui_element(play_button)

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