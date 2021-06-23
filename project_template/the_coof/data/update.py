class Update:
    def update(self, delta_time):
            """ Movement and game logic """

            # Move the player with the physics engine
            self.physics_engine.update()

            # See if we hit any coins
            coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                                self.coin_list)

            # Loop through each coin we hit (if any) and remove it
            for coin in coin_hit_list:
                # Remove the coin
                coin.remove_from_sprite_lists()
                # Play a sound
                arcade.play_sound(self.collect_coin_sound)
                # Add one to the score
                self.score += 1

            # Track if we need to change the viewport
            changed_viewport = False

            # Did the player fall off the map?
            if self.player_sprite.center_y < -100:
                self.player_sprite.center_x = PLAYER_START_X
                self.player_sprite.center_y = PLAYER_START_Y

                # Set the camera to the start
                self.view_left = 0
                self.view_bottom = 0
                changed_viewport = True
                arcade.play_sound(self.game_over)

            # Did the player touch something they should not?
            if arcade.check_for_collision_with_list(self.player_sprite,
                                                    self.dont_touch_list):
                self.player_sprite.change_x = 0
                self.player_sprite.change_y = 0
                self.player_sprite.center_x = PLAYER_START_X
                self.player_sprite.center_y = PLAYER_START_Y

                # Set the camera to the start
                self.view_left = 0
                self.view_bottom = 0
                changed_viewport = True
                arcade.play_sound(self.game_over)

            # See if the user got to the end of the level
            if self.player_sprite.center_x >= self.end_of_map:
                # Advance to the next level
                self.level += 1

                # Load the next level
                self.setup(self.level)

                # Set the camera to the start
                self.view_left = 0
                self.view_bottom = 0
                changed_viewport = True

            # --- Manage Scrolling ---

            # Scroll left
            left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
            if self.player_sprite.left < left_boundary:
                self.view_left -= left_boundary - self.player_sprite.left
                changed_viewport = True

            # Scroll right
            right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
            if self.player_sprite.right > right_boundary:
                self.view_left += self.player_sprite.right - right_boundary
                changed_viewport = True

            # Scroll up
            top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
            if self.player_sprite.top > top_boundary:
                self.view_bottom += self.player_sprite.top - top_boundary
                changed_viewport = True

            # Scroll down
            bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
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
                                    SCREEN_WIDTH + self.view_left,
                                    self.view_bottom,
                                    SCREEN_HEIGHT + self.view_bottom)