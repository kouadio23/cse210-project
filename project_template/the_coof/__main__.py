import arcade
import arcade.gui
from arcade.gui import UIManager
from data import constants


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
        game_view.setup(1)
        self.window.show_view(game_view)


class GameView(arcade.View):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__()

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.shield_list = None
        self.wall_list = None
        self.foreground_list = None
        self.background_list = None
        self.dont_touch_list = None
        self.player_list = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our physics engine
        self.physics_engine = None

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Keep track of the score
        self.score = 0

        # Where is the right edge of the map?
        self.end_of_map = 0

        # Level
        self.level = 1

        # Load sounds
        self.music = arcade.load_sound(constants.MUSIC)
        arcade.play_sound(self.music)
        self.collect_shield_sound = arcade.load_sound(constants.MASK_SOUND)
        self.jump_sound = arcade.load_sound(constants.JUMP_SOUND)
        self.game_over = arcade.load_sound(constants.GAME_OVER_SOUND)

        f = open(constants.HIGH_SCORE, "r")
        self.high_score = f.readline()
        f.close()

        self.is_game_over = False

    def setup(self, level):
        """ Set up the game here. Call this function to restart the game. """

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Keep track of the score
        self.score = 0

        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.foreground_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.shield_list = arcade.SpriteList()

        # Set up the player, specifically placing it at these coordinates.
        image_source = constants.BRO_NATE
        self.player_sprite = arcade.Sprite(image_source, constants.CHARACTER_SCALING)
        self.player_sprite.center_x = constants.PLAYER_START_X
        self.player_sprite.center_y = constants.PLAYER_START_Y
        self.player_list.append(self.player_sprite)
        self.player_sprite.change_x = constants.PLAYER_MOVEMENT_SPEED

        # --- Load in a map from the tiled editor ---
        # Name of the layer in the file that has our platforms/walls
        platforms_layer_name = 'Platform (Snow)'
        # Name of the layer that has items for foreground
        foreground_layer_name = 'Foreground'
        # Name of the layer that has items for background
        background_layer_name = 'Background (Clouds)'
        # Name of the layer that has items we shouldn't touch
        dont_touch_layer_name = "Don't Touch (Viruses)"
        # Name of the layer that has items for pick-up
        shield_layer_name = 'Shield (Mask)'

        # Map name
        map_name = constants.MAP

        # Read in the tiled map
        my_map = arcade.tilemap.read_tmx(map_name)

        # Calculate the right edge of the my_map in pixels
        self.end_of_map = my_map.map_size.width * constants.GRID_PIXEL_SIZE

        # -- Background
        self.background_list = arcade.tilemap.process_layer(my_map,
                                                            background_layer_name,
                                                            constants.TILE_SCALING)

        # -- Foreground
        self.foreground_list = arcade.tilemap.process_layer(my_map,
                                                            foreground_layer_name,
                                                            constants.TILE_SCALING)

        # -- Platforms
        self.wall_list = arcade.tilemap.process_layer(map_object=my_map,
                                                      layer_name=platforms_layer_name,
                                                      scaling=constants.TILE_SCALING,
                                                      use_spatial_hash=True)

        # -- Don't Touch Layer
        self.dont_touch_list = arcade.tilemap.process_layer(my_map,
                                                            dont_touch_layer_name,
                                                            constants.TILE_SCALING,
                                                            use_spatial_hash=True)
        
        # -- Shields
        self.shield_list = arcade.tilemap.process_layer(my_map,
                                                      shield_layer_name,
                                                      constants.TILE_SCALING,
                                                      use_spatial_hash=True)

        # --- Other stuff
        # Set the background color
        if my_map.background_color:
            arcade.set_background_color(my_map.background_color)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             constants.GRAVITY)

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen to the background color
        arcade.start_render()

        # Draw our sprites
        self.wall_list.draw()
        self.background_list.draw()
        self.wall_list.draw()
        self.shield_list.draw()
        self.dont_touch_list.draw()
        self.player_list.draw()
        self.foreground_list.draw()

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom,
                         arcade.csscolor.BLACK, 18)

        high_score_text = f"High Score: {self.high_score}"
        arcade.draw_text(high_score_text, 830 + self.view_left, 10 + self.view_bottom,
                         arcade.csscolor.BLACK, 18)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = constants.PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)

    def update(self, delta_time):
        """ Movement and game logic """

        # Move the player with the physics engine
        self.physics_engine.update()

        # See if we hit any shields
        shield_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                            self.shield_list)

        # Loop through each shield we hit (if any) and remove it
        for shield in shield_hit_list:
            # Remove the shield
            shield.remove_from_sprite_lists()
            # Play a sound
            arcade.play_sound(self.collect_shield_sound)
            # Add bonus 400 points to the score for collecting the mask/sanitizer
            self.score += 400
        
        self.score += 1

        # Track if we need to change the viewport
        changed_viewport = False

        # Did the player fall off the map?
        if self.player_sprite.center_y < -100:
            self.player_sprite.center_x = constants.PLAYER_START_X
            self.player_sprite.center_y = constants.PLAYER_START_Y

            # Set the camera to the start
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True
            arcade.play_sound(self.game_over)

        # Did the player touch something they should not?
        if arcade.check_for_collision_with_list(self.player_sprite,
                                                self.dont_touch_list):
            self.player_sprite.change_x = constants.PLAYER_MOVEMENT_SPEED
            self.player_sprite.change_y = 0
            self.player_sprite.center_x = constants.PLAYER_START_X
            self.player_sprite.center_y = constants.PLAYER_START_Y

            if int(self.score) > int(self.high_score):
                f = open(constants.HIGH_SCORE, "w")
                f.write(str(self.score))
                f.close()

            # Set the camera to the start
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True
            arcade.play_sound(self.game_over)
            self.is_game_over = True
            
        if self.is_game_over:
            game_over_view = GameOverView()
            self.window.show_view(game_over_view)
    

        # --- Manage Scrolling ---
        # Scroll left
        left_boundary = self.view_left + constants.LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed_viewport = True

        # Scroll right
        right_boundary = self.view_left + constants.SCREEN_WIDTH - constants.RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed_viewport = True

        # Scroll up
        top_boundary = self.view_bottom + constants.SCREEN_HEIGHT - constants.TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed_viewport = True

        # Scroll down
        bottom_boundary = self.view_bottom + constants.BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed_viewport = True

        if changed_viewport:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                constants.SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                constants.SCREEN_HEIGHT + self.view_bottom)


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
        game_view.setup(1)
        self.window.show_view(game_view)


def main():
    window = arcade.Window(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, constants.SCREEN_TITLE)
    window.total_score = 0
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()