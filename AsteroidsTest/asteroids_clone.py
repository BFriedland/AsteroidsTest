import pygame
import sys
import math
import random

'''

Notes on the state of the code

This game is still being re-factored to conform to the standards of
    PEP8 and basic human decency. It was coded in the land before time,
    when I had no formal training in software development. As a result
    it should be considered incomplete and for the purposes of code
    quality my more recent projects should be examined.

Two Django apps with better formatting are my student team projects, Imagr
    (much being my creation) and RPi-Haus (in which I was responsible for
    the API), both of which can be found on my GitHub repo (BFriedland).

'''


# # # # Constants # # # #

WINDOW_CAPTION = 'Asteroids! Clone'

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SCREEN_CENTER_X, SCREEN_CENTER_Y = (SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2)
MAP_X, MAP_Y = 0, 0
MAP_X2, MAP_Y2 = (SCREEN_WIDTH * 1.5), (SCREEN_HEIGHT * 1.5)

# This part is to make the screen perfectly centered
# in the middle of the map, regardless of map width.
# It does this by adjusting map minimum and maximum parameters.
DIFF_BETWEEN_MAP_AND_SCREEN_WIDTH = MAP_X2 - SCREEN_WIDTH
DIFF_BETWEEN_MAP_AND_SCREEN_HEIGHT = MAP_Y2 - SCREEN_HEIGHT
MAP_X = MAP_X - (DIFF_BETWEEN_MAP_AND_SCREEN_WIDTH / 2)
MAP_X2 = MAP_X2 - (DIFF_BETWEEN_MAP_AND_SCREEN_WIDTH / 2)
MAP_Y = MAP_Y - (DIFF_BETWEEN_MAP_AND_SCREEN_HEIGHT / 2)
MAP_Y2 = MAP_Y2 - (DIFF_BETWEEN_MAP_AND_SCREEN_HEIGHT / 2)

# Screen dimensions determine the most you can see on the screen.
# If you want the playing field to be smaller (or bigger...)
# than the screen, that should be altered.
PLAYING_FIELD_X, PLAYING_FIELD_Y = 0, 0
PLAYING_FIELD_X2, PLAYING_FIELD_Y2 = SCREEN_WIDTH, SCREEN_HEIGHT

# Game mechanics constants ---v

# Does the player ship maintain its angular velocity
# when not acted upon by an outside force?
PLAYER_HAS_ANGULAR_VELOCITY = False
# Is the player's ship suspended in a motion-resisting aether,
# or are they in outer space?
# Slows the ship down when not accelerating.
PLAYER_SHIP_HAS_DRAG = True
# Do shots inherit velocity from the ship that fired them?
SHOTS_INHERIT_VELOCITY = False
# Is the player ship destroyed when it hits an asteroid?
PLAYER_SHIP_IS_INVULNERABLE = False

# Color defs in RGB; critical for programmatic art.
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]


# # # # Classes # # # #

class GameObject(object):
    '''
    Create a programmatically-drawn object in the playing field.
    GameObjects are capable of movement, display, and routine updating.
    '''

    def __init__(self, *args, **kwargs):

        # Preventing extremely long parameter lists:
        # Defaults for kwargs taken from a dictionary
        # rather than being listed in the parameters!

        # With thanks to blubb's StackOverflow answer to this question:
        # https://stackoverflow.com/questions/5899185
        #     /class-with-too-many-parameters-better-design-strategy

        self.initial_parameters = {}

        # First, the positional arguments.
        # These are required to be supplied by
        # the call to the GameObject constructor.
        self.initial_parameters['starting_x'] = args[0]
        self.initial_parameters['starting_y'] = args[1]
        self.initial_parameters['x_velocity'] = args[2]
        self.initial_parameters['y_velocity'] = args[3]
        self.initial_parameters['angular_velocity'] = args[4]

        # Here, we're loading the initial_parameters
        # dictionary with default values for all
        # of the anticipated keyword arguments
        # that might be handed to GameObjects
        # on intialization:
        self.initial_parameters['current_angle_in_degrees'] = 0
        self.initial_parameters['size'] = 1
        self.initial_parameters['color'] = WHITE
        self.initial_parameters['programmatic_object_shape'] = 1
        self.initial_parameters['is_owned_by_player'] = False
        self.initial_parameters['duration_remaining'] = None
        self.initial_parameters['max_velocity'] = 4

        # Now we replace the defaults with values specified
        # by kwargs, and also set up this instance's
        # attributes according to either the default or,
        # if provided, the specified argument.
        # Note that this also covers the non-keyword args, as they
        # have already been added to the intial_parameters dictionary.
        # Also note that in Python 3+ it's dict.items(),
        # whereas in Python 2 it's dict.iteritems()
        for (each_key, default_value) in self.initial_parameters.items():

            specified_value = kwargs.get(each_key, default_value)

            # This is effectively the same as setting self.kwarg = kwarg:
            setattr(self, each_key, specified_value)

            # Also overwrite the value in the initial_parameters dictionary
            # to maintain a record of initial values for later use.
            self.initial_parameters[each_key] = specified_value

        # Now to initialize the derived parameters.
        # These are not handed in either the args or
        # the kwargs, and are instead derived from them.

        self.radius = (self.size / 2)

        self.x = 0
        self.y = 0
        self.move_by_specified_amount(self.starting_x, self.starting_y)

    def draw(self):
        '''
        Call draw_programmatic_object() with the GameObject's parameters.
        '''

        draw_programmatic_object(self.x,
                                 self.y,
                                 self.current_angle_in_degrees,
                                 self.programmatic_object_shape,
                                 self.color,
                                 self.size)

    def move_by_specified_amount(self, delta_x, delta_y):
        '''
        Move the GameObject by the specified x, y amount.
        '''

        self.x += delta_x
        self.y += delta_y

    def move(self):
        '''
        Move the GameObject using its current velocity values;
        bounce off the edges of the playing field if indicated.
        '''

        # The sheer length of this method indicates something is wrong.
        # It should be split into subclasses with modified move() methods.

        # Globals are a sign the code needs more objects.
        # Specifically, these should be stored in a GameState object.
        global player_lives_left
        global score

        if isinstance(self, PlayerShip) is False:

            if (((self.x - self.radius) < MAP_X)
               or (((self.x + self.radius) > MAP_X2))
               or (((self.y - self.radius) < MAP_Y))
               or ((self.y + self.radius) > MAP_Y2)):

                # If GameObject is not owned by the player or is a Shot object,
                # it should bounce off the edges of the map, rather than
                # the screen (or it should be destroyed, for Shot).
                # if ((self.x - self.radius) < MAP_X):
                if isinstance(self, Asteroid) is True:
                    if self in asteroid_objects_array:
                        asteroid_objects_array.remove(self)
                elif isinstance(self, Shot) is True:
                    if self in shot_objects_array:
                        shot_objects_array.remove(self)
                elif isinstance(self, Debris) is True:
                    if self in debris_objects_array:
                        debris_objects_array.remove(self)
                elif isinstance(self, AlienShip) is True:
                    if self in alien_ship_objects_array:
                        alien_ship_objects_array.remove(self)
                else:
                    raise Exception("{} out of bounds!".format(str(self)))

        elif ((self.is_owned_by_player is True)
              and (isinstance(self, Shot) is False)):
            # If it's owned by the player and is NOT a shot object,
            # it must be the player ship, and should bounce off the edges
            # of the playing field (probably == the screen, too).
            if ((self.x - self.radius) < PLAYING_FIELD_X):
                self.x_velocity = (abs(self.x_velocity) * 1)
                self.angular_velocity *= -1
            if ((self.x + self.radius) > PLAYING_FIELD_X2):
                self.x_velocity = (abs(self.x_velocity) * -1)
                self.angular_velocity *= -1

            if ((self.y - self.radius) < PLAYING_FIELD_Y):
                self.y_velocity = (abs(self.y_velocity) * 1)
                self.angular_velocity *= -1
            if ((self.y + self.radius) > PLAYING_FIELD_Y2):
                self.y_velocity = (abs(self.y_velocity) * -1)
                self.angular_velocity *= -1

        # So, there are a lot of these long conditionals in this program.
        # This is because I had no formal training at the time I wrote it
        # and I wanted to be as productive as possible, and at the time
        # that meant solving one problem at a time in whichever way I could.
        # This kind of conditional ought to be turned into an event flag
        # handler or some kind of class state component with a nice, explicit
        # name to aid in bugchex.

        # [Asteroid] collision with [shot, player ship, alien ship]-detection.
        # Note this section uses "shot" to refer to all of these things.

        # ----> Is self a shot?
        if (((isinstance(self, Shot) is True)
            # IF NOT...   is it a player-owned object ...
             or (((self.is_owned_by_player is True)
                 # AND not a shot (ie, the player's ship) ...
                  and (isinstance(self, Shot) is False))
                 # AND also can the player's ship be harmed?
                 and (PLAYER_SHIP_IS_INVULNERABLE is False)))
                # IF NOT, is it an alien ship?
                or (isinstance(self, AlienShip) is True)):

            for each_asteroid in asteroid_objects_array:
                distance_between_them_as_hypotenuse \
                    = return_euclidean_distance(self, each_asteroid)

                combined_shot_and_asteroid_radius \
                    = self.radius + each_asteroid.radius
                if (combined_shot_and_asteroid_radius
                   >= distance_between_them_as_hypotenuse):

                    if self in shot_objects_array:
                        shot_objects_array.remove(self)
                    if self in player_ship_objects_array:
                        self.spawn_player_ship_debris_cloud()
                        player_ship_objects_array.remove(self)
                        remove_player_life()
                    if self in alien_ship_objects_array:
                        # Alien ships colliding with asteroids DO NOT
                        # result in ++score. The aliens aren't bright
                        # enough yet to make that a sensible mechanic
                        # for players to use at this stage of development.
                        self.spawn_debris_cloud()
                        alien_ship_objects_array.remove(self)

                    if each_asteroid in asteroid_objects_array:

                        if self.is_owned_by_player is True:
                            # If the thing destroying the asteroid
                            # is_owned_by_player, then it gives score.
                            # This SHOULD be handled separately;
                            # score incrementing should pass object
                            # references and event flags to a "referee"
                            # class which determines if the event in
                            # question should alter the score.
                            if each_asteroid.size == 100:
                                score += 20
                            elif each_asteroid.size == 50:
                                score += 50
                            elif each_asteroid.size == 20:
                                score += 100

                        if ((each_asteroid.size == 50)
                           or (each_asteroid.size == 100)):
                            # This looks so weird and wrong.
                            # I don't know if I trust Flake8 here...
                            each_asteroid. \
                                break_large_asteroid_into_two_smaller_ones(
                                    self.x_velocity,
                                    self.y_velocity,
                                    self.size)
                        each_asteroid.spawn_debris_cloud()
                        asteroid_objects_array.remove(each_asteroid)

        # [Alien ship] collision with
        # [player ship shot, player ship]-detection.
        # Note that the previous section handled asteroids hitting
        # alien ships and alien ship shots hitting asteroids.
        if isinstance(self, AlienShip) is True:

            # Collision with player shots:
            for each_shot_object in shot_objects_array:
                if each_shot_object.is_owned_by_player is True:

                    distance_between_them_as_hypotenuse \
                        = return_euclidean_distance(self, each_shot_object)

                    combined_alien_and_shot_radius \
                        = self.radius + each_shot_object.radius
                    if (combined_alien_and_shot_radius
                       >= distance_between_them_as_hypotenuse):
                        if self in alien_ship_objects_array:
                            if self.size == 40:
                                score += 200
                            elif self.size == 20:
                                score += 1000
                            self.spawn_debris_cloud()
                            alien_ship_objects_array.remove(self)

                        if each_shot_object in shot_objects_array:
                            shot_objects_array.remove(each_shot_object)

            # Collision with player ships:
            for each_player_ship in player_ship_objects_array:
                # Here is where I realized iterating through player ship
                # objects is a bit weird in a game where there's only one
                # of them. The solution would be a heavier reliance on
                # state carriers somewhere in the main loop, I think.
                distance_between_them_as_hypotenuse \
                    = return_euclidean_distance(self, each_player_ship)

                combined_alien_and_player_ship_radius \
                    = self.radius + each_player_ship.radius
                if (combined_alien_and_player_ship_radius
                   >= distance_between_them_as_hypotenuse):
                    if self in alien_ship_objects_array:
                        if self.size == 40:
                            score += 200
                        elif self.size == 20:
                            score += 1000
                        self.spawn_debris_cloud()
                        alien_ship_objects_array.remove(self)
                    if each_player_ship in player_ship_objects_array:
                        each_player_ship.spawn_player_ship_debris_cloud()
                        player_ship_objects_array.remove(each_player_ship)
                        remove_player_life()

        # [Alien shot] collision with [player ship]-detection.
        elif ((isinstance(self, Shot) is True)
              and (self.is_owned_by_player is False)):

            for each_player_ship in player_ship_objects_array:
                # See above note about oddity of iterating through
                # a list of player ship objects.
                # Also, it's a LIST, not an ARRAY!
                distance_between_them_as_hypotenuse \
                    = return_euclidean_distance(self, each_player_ship)
                combined_alien_shot_and_player_ship_radius \
                    = self.radius + each_player_ship.radius
                if (combined_alien_shot_and_player_ship_radius
                   >= distance_between_them_as_hypotenuse):
                    if self in shot_objects_array:
                        shot_objects_array.remove(self)
                    if each_player_ship in player_ship_objects_array:
                        each_player_ship.spawn_player_ship_debris_cloud()
                        player_ship_objects_array.remove(each_player_ship)
                        remove_player_life()

        # Should -v be before or after -^  ?
        # ...
        # I think after.
        # Change direction if near edge of correct area, THEN move? I wonder...
        self.move_by_specified_amount(self.x_velocity, self.y_velocity)

    def adjust_current_angle(self, angle_adjustment):
        ''' Adjust the GameObject's current angle, in degrees. '''

        if self.current_angle_in_degrees is not None:
            # This if check solves the bullet case,
            # since bullets don't spin in Asteroids!
            self.current_angle_in_degrees += angle_adjustment

        if (abs(self.current_angle_in_degrees) >= 360):
            self.current_angle_in_degrees = 0

    def adjust_all_velocities(self,
                              x_acceleration,
                              y_acceleration,
                              angular_acceleration):
        '''
        Apply acceleration to the GameObject's x_velocity, y_velocity,
        current_angle_in_degrees values; use self.current_angle_in_degrees
        to increment velocities appropriately.
        '''

        # Resolve the angular offset of the velocities.
        # This uses the rotation function to properly apply delta-V
        # in the direction it needs to be going.
        # Final three parameters:
        #     ship_center_x,
        #     ship_center_y,
        #     player_ship_objects_array[0].current_angle_in_degrees
        rotated_x_velocity_increment, rotated_y_velocity_increment \
            = rotate_these_points_around_that_point(
                x_acceleration,
                y_acceleration,
                0,
                0,
                self.current_angle_in_degrees)

        # It's not the euclidean distance, it's just the Pythagorean
        # theorem... Because these are velocities.
        self.x_velocity += rotated_x_velocity_increment
        self.y_velocity += rotated_y_velocity_increment

        hypotenuse_of_x_and_y_velocities = math.sqrt(
            (self.x_velocity * self.x_velocity)
            + (self.y_velocity * self.y_velocity))

        # The micro-offset is to prevent divide-by-zero errors.
        if hypotenuse_of_x_and_y_velocities >= self.max_velocity:
            ratio_of_max_velocity_to_current_velocity \
                = (self.max_velocity
                   / (hypotenuse_of_x_and_y_velocities + 0.00001))

            self.x_velocity = (self.x_velocity
                               * ratio_of_max_velocity_to_current_velocity)
            self.y_velocity = (self.y_velocity
                               * ratio_of_max_velocity_to_current_velocity)

        # # # # Theta (angular velocity)

        # Very similar to the other velocities, except it doesn't
        # have to care about the sign difference between grid
        # direction and total velocity when checking its cap.
        if ((self.angular_velocity > 10) and (angular_acceleration > 0)):
            self.angular_velocity -= 0
        elif ((self.angular_velocity < -10) and (angular_acceleration < 0)):
            self.angular_velocity += 0
        else:
            self.angular_velocity += angular_acceleration

    def brake_all_velocities(self,
                             only_braking_angular_velocity=False,
                             is_gradual_braking=False):
        '''
        Applies acceleration to the GameObject's x_velocity,
        y_velocity, current_angle_in_degrees values, consistently
        opposite to the direction of its velocities' current values.
        '''

        if is_gradual_braking is True:
            braking_coefficient = 0.1
        else:
            braking_coefficient = 0.4

        if only_braking_angular_velocity is False:
            hypotenuse_of_x_and_y_velocities = math.sqrt(
                (self.x_velocity * self.x_velocity)
                + (self.y_velocity * self.y_velocity))
            if hypotenuse_of_x_and_y_velocities >= braking_coefficient:
                ratio_of_minused_hypotenuse_to_hypotenuse \
                    = ((hypotenuse_of_x_and_y_velocities - braking_coefficient)
                       / hypotenuse_of_x_and_y_velocities)
                self.x_velocity \
                    = (self.x_velocity
                        * ratio_of_minused_hypotenuse_to_hypotenuse)
                self.y_velocity \
                    = (self.y_velocity
                        * ratio_of_minused_hypotenuse_to_hypotenuse)
            elif hypotenuse_of_x_and_y_velocities < braking_coefficient:
                self.x_velocity = 0
                self.y_velocity = 0

        if abs(self.angular_velocity) > braking_coefficient:
            # If a nontrivial adjustment needs to be made to angular velocity:
            if self.angular_velocity > 0:
                self.adjust_all_velocities(0, 0, (braking_coefficient * -1))
            elif self.angular_velocity < 0:
                self.adjust_all_velocities(0, 0, braking_coefficient)

        elif abs(self.angular_velocity) <= braking_coefficient:
            # Otherwise, make the trivial adjustment.
            self.angular_velocity = 0

    def decrement_duration_and_if_necessary_destroy(self,
                                                    duration_decrement=0):
        '''
        Decrement remaining duration by supplied duration decrement.
        If (self.duration_remaining <= 0) then destroy self.
        Used for debris objects.
        '''

        # This is in GameObject because I want it
        # to be usable for Shot objects, as well.
        self.duration_remaining -= duration_decrement
        if self.duration_remaining <= 0:
            if isinstance(self, Debris):
                if self in debris_objects_array:
                    debris_objects_array.remove(self)
            if isinstance(self, Shot):
                if self in shot_objects_array:
                    shot_objects_array.remove(self)


class Asteroid(GameObject):
    '''
    Make a GameObject with the properties of an asteroid.
    '''

    def spawn_debris_cloud(self):
        '''
        Delete the Asteroid and spawn a debris cloud at its location.
        '''

        number_of_new_debris_objects_to_be_created = random.randint(3, 8)
        for each in range(0, number_of_new_debris_objects_to_be_created):
            # Generate a vector in a random direction at precisely 10 speed.
            random_angle = random.randint(0, 359)
            # It would be nice if debris inherited velocity from
            # the asteroid, so it appeared to actually be fragments
            # of it, but that isn't how Asteroids! works.
            random_x_velocity_result, random_y_velocity_result \
                = rotate_these_points_around_that_point(0, -10, 0, 0,
                                                        random_angle)
            random_duration = random.randint(4, 12)
            new_debris_object = Debris(self.x, self.y,
                                       random_x_velocity_result,
                                       random_y_velocity_result,
                                       0, size=4, programmatic_object_shape=-1,
                                       duration_remaining=random_duration)
            debris_objects_array.append(new_debris_object)

    def break_large_asteroid_into_two_smaller_ones(self,
                                                   shot_x_velocity,
                                                   shot_y_velocity,
                                                   shot_size,
                                                   shot_angular_velocity=None):
        '''
        Create two new asteroids using information from the current asteroid.
        '''

        ratio_of_shot_size_to_asteroid_size = shot_size / self.size
        # # X and Y velocities
        sum_of_shot_and_asteroid_x_velocities \
            = ((shot_x_velocity * ratio_of_shot_size_to_asteroid_size)
               + self.x_velocity)
        sum_of_shot_and_asteroid_y_velocities \
            = ((shot_y_velocity * ratio_of_shot_size_to_asteroid_size)
               + self.y_velocity)
        hypotenuse_of_shot_and_asteroid_velocities \
            = math.sqrt((sum_of_shot_and_asteroid_x_velocities
                         * sum_of_shot_and_asteroid_x_velocities)
                        + (sum_of_shot_and_asteroid_y_velocities
                           * sum_of_shot_and_asteroid_y_velocities))
        if hypotenuse_of_shot_and_asteroid_velocities > 10:
            # Reduce the current vector sum to the max
            # velocity vector sum of the current asteroid.
            number_of_max_velocities_per_current_velocity \
                = (self.max_velocity
                   / (hypotenuse_of_shot_and_asteroid_velocities + 0.00001))
            sum_of_shot_and_asteroid_x_velocities \
                = (sum_of_shot_and_asteroid_x_velocities
                   * number_of_max_velocities_per_current_velocity)
            sum_of_shot_and_asteroid_y_velocities \
                = (sum_of_shot_and_asteroid_y_velocities
                   * number_of_max_velocities_per_current_velocity)
        # Multiply both x and y vectors by 2,
        # take a random proportion and apply
        # each side of it to the child Asteroids:
        sum_of_x_velocities_multiplied_by_two \
            = sum_of_shot_and_asteroid_x_velocities * 2
        sum_of_y_velocities_multiplied_by_two \
            = sum_of_shot_and_asteroid_y_velocities * 2
        random_x_velocity_splitting_ratio = random.random()
        random_y_velocity_splitting_ratio = random.random()
        first_split_asteroid_x_velocity \
            = (sum_of_x_velocities_multiplied_by_two
               * random_x_velocity_splitting_ratio)
        second_split_asteroid_x_velocity \
            = (sum_of_x_velocities_multiplied_by_two
               - first_split_asteroid_x_velocity)
        if (first_split_asteroid_x_velocity
           < (sum_of_x_velocities_multiplied_by_two * 0.5)):
            first_split_asteroid_x_velocity \
                += (sum_of_x_velocities_multiplied_by_two * 0.5)
        if (second_split_asteroid_x_velocity
           < (sum_of_x_velocities_multiplied_by_two * 0.5)):
            second_split_asteroid_x_velocity \
                += (sum_of_x_velocities_multiplied_by_two * 0.5)
        first_split_asteroid_y_velocity \
            = (sum_of_y_velocities_multiplied_by_two
               * random_y_velocity_splitting_ratio)
        second_split_asteroid_y_velocity \
            = (sum_of_y_velocities_multiplied_by_two
               - first_split_asteroid_y_velocity)
        if (first_split_asteroid_y_velocity
           < (sum_of_y_velocities_multiplied_by_two * 0.5)):
            first_split_asteroid_y_velocity \
                += (sum_of_y_velocities_multiplied_by_two * 0.5)
        if (second_split_asteroid_y_velocity
           < (sum_of_y_velocities_multiplied_by_two * 0.5)):
            second_split_asteroid_y_velocity \
                += (sum_of_y_velocities_multiplied_by_two * 0.5)
        # # Angular velocity
        random_angular_velocity_seed = (random.randint(-10, 10))
        random_angular_velocity_seed_splitter = random.random()
        first_split_asteroid_angular_velocity \
            = (random_angular_velocity_seed
               * random_angular_velocity_seed_splitter)
        second_split_asteroid_angular_velocity \
            = ((random_angular_velocity_seed
                - first_split_asteroid_angular_velocity)
               * -1)

        if self.size == 100:
            both_split_asteroids_size = 50
        elif self.size == 50:
            both_split_asteroids_size = 20

        random_asteroid_shape = None

        create_new_asteroid_object(supplied_starting_x=self.x,
                                   supplied_starting_y=self.y,
                                   supplied_x_velocity=first_split_asteroid_x_velocity,
                                   supplied_y_velocity=first_split_asteroid_y_velocity,
                                   supplied_angular_velocity=first_split_asteroid_angular_velocity,
                                   supplied_asteroid_size=both_split_asteroids_size,
                                   supplied_asteroid_shape=random_asteroid_shape)
        create_new_asteroid_object(supplied_starting_x=self.x,
                                   supplied_starting_y=self.y,
                                   supplied_x_velocity=second_split_asteroid_x_velocity,
                                   supplied_y_velocity=second_split_asteroid_y_velocity,
                                   supplied_angular_velocity=second_split_asteroid_angular_velocity,
                                   supplied_asteroid_size=both_split_asteroids_size,
                                   supplied_asteroid_shape=random_asteroid_shape)


class PlayerShip(GameObject):
    '''
    Make a GameObject controlled by either the player or the aliens.
    '''

    def fire_particle_cannon(self):
        '''
        Fire a shot with position and velocity
        info inherited from the firing ship.
        '''

        # Where it's firing from:   ((the front point of the ship))
        ship_front_tip_x = self.x
        ship_front_tip_y = (self.y - self.radius)
        rotated_ship_tip_x, rotated_ship_tip_y \
            = rotate_these_points_around_that_point(ship_front_tip_x,
                                                    ship_front_tip_y,
                                                    self.x,
                                                    self.y,
                                                    self.current_angle_in_degrees)
        # Synonymizing. It helped when I didn't know what I was doing...
        shot_start_location_x = rotated_ship_tip_x
        shot_start_location_y = rotated_ship_tip_y

        # This gives the Shot a velocity of 14 in the correct direction:
        rotated_shot_velocity_x_modifier, rotated_shot_velocity_y_modifier \
            = rotate_these_points_around_that_point(0, -14, 0, 0,
                                                    self.current_angle_in_degrees)

        if SHOTS_INHERIT_VELOCITY is True:
            shot_velocity_seed_x \
                = self.x_velocity + rotated_shot_velocity_x_modifier
            shot_velocity_seed_y \
                = self.y_velocity + rotated_shot_velocity_y_modifier
        else:
            shot_velocity_seed_x = rotated_shot_velocity_x_modifier
            shot_velocity_seed_y = rotated_shot_velocity_y_modifier

        # Make and append the Shot object:
        new_shot_object = Shot(shot_start_location_x,
                               shot_start_location_y,
                               shot_velocity_seed_x,
                               shot_velocity_seed_y,
                               0,
                               self.current_angle_in_degrees,
                               is_owned_by_player=self.is_owned_by_player,
                               programmatic_object_shape=-1,
                               size=4,
                               duration_remaining=26)
        shot_objects_array.append(new_shot_object)

        # Repulsion effect on the ship.
        # Note that, as seen above, the center x and y
        # for this rotation are 0 because we're rotating
        # a velocity value, not a positional value.
        if SHOTS_INHERIT_VELOCITY is True:
            self.adjust_all_velocities(0, 0.1, 0)
        else:
            self.adjust_all_velocities(0, 0.2, 0)

    def spawn_player_ship_debris_cloud(self,
                                       supplied_x_velocity=None,
                                       supplied_y_velocity=None,
                                       supplied_angular_velocity=None):
        '''
        Spawn four debris objects of equal length at
        the player's ship's center's location that persist
        for a few seconds while twirling about in space
        and then disappear. Duration slightly randomized;
        longest must be <2 seconds, shortest >0.5 seconds.
        '''

        for each_debris_piece in range(0, 4):
            random_duration = random.randint(24, 36)
            # Generate a velocity pair in a random direction with speed 10:
            random_angle = random.randint(0, 359)
            random_x_velocity_seed, random_y_velocity_seed \
                = rotate_these_points_around_that_point(0, -10, 0, 0,
                                                        random_angle)
            # Take the hypotenuse of the ship's velocity at impact:
            hypotenuse_of_current_velocities = math.sqrt(
                (self.x_velocity * self.x_velocity)
                + (self.y_velocity * self.y_velocity))
            # Take the hypotenuse of the randomly generated velocities:
            hypotenuse_of_random_velocities = math.sqrt(
                (random_x_velocity_seed * random_x_velocity_seed)
                + (random_y_velocity_seed * random_y_velocity_seed))
            # Find the ratio of the two, so as to figure out how much
            # to multiply the randomly generated velocites by to maintain
            # ship speed in the debris objects while also randomizing
            # direction of the debris. Reason being, fast-flying ships'
            # debris don't lose that momentum in the real world.
            # Note: the + 3 is to give it a minimum velocity so they
            # don't just spin in place if the player ship is
            # destroyed while standing still... and the / 3 is
            # to keep the debris from flying too fast compared
            # to the original Asteroids!.
            ratio_of_current_velocities_to_random_velocities \
                = (((hypotenuse_of_current_velocities + 3) / 3)
                   / hypotenuse_of_random_velocities)
            # Multiply both randomly generated velocities by
            # the current:random velocities ratio
            # to get the properly scaled end result:
            random_x_velocity_result \
                = (random_x_velocity_seed
                   * ratio_of_current_velocities_to_random_velocities)
            random_y_velocity_result \
                = (random_y_velocity_seed
                   * ratio_of_current_velocities_to_random_velocities)
            random_angular_velocity_seed = random.randint(0, 20)
            random_angular_velocity = (random_angular_velocity_seed - 10)

            # This is probably a bad sign. I'm going to refactor it after
            # I do some research about best practices against excessive
            # parameters in constructor calls.
            new_player_ship_debris_object = Debris(self.x, self.y,
                                                   random_x_velocity_result,
                                                   random_y_velocity_result,
                                                   random_angular_velocity,
                                                   current_angle_in_degrees=random_angle,
                                                   size=self.size,
                                                   programmatic_object_shape=-3,
                                                   duration_remaining=random_duration)
            debris_objects_array.append(new_player_ship_debris_object)

    def draw(self):
        '''
        Call GameObject.draw() for this PlayerShip.

        If accelerating (but not during the firing
        of a Shot), also draw ship exhaust.
        '''

        GameObject.draw(self)

        # If the ship is accelerating, draw exhaust behind the ship.
        if player_is_accelerating is True:
            if player_fired_shot is False:
                draw_programmatic_object(
                    self.x,
                    self.y,
                    self.current_angle_in_degrees,
                    this_programmatic_object_shape=-2,
                    color=self.color,
                    size=self.size
                )


class AlienShip(GameObject):
    '''
    Create an alien ship that sometimes changes its velocity
    and shoots both randomly and at the player's ship.
    '''

    def __init__(self, *args, **kwargs):

        GameObject.__init__(self, *args, **kwargs)

        self.pixellus_cannon_recharge_ticker = 0

    def spawn_debris_cloud(self):
        '''
        Delete the AlienShip and spawn a cloud
        of Debris objects at its location.
        '''

        number_of_new_debris_objects_to_be_created = random.randint(3, 8)
        for each in range(0, number_of_new_debris_objects_to_be_created):
            # Generate a vector in a random direction at precisely 10 speed.
            random_angle = random.randint(0, 359)
            random_x_velocity_result, random_y_velocity_result \
                = rotate_these_points_around_that_point(0, -10, 0, 0,
                                                        random_angle)
            random_duration = random.randint(4, 12)
            new_debris_object \
                = Debris(self.x, self.y,
                         random_x_velocity_result, random_y_velocity_result,
                         0, size=4, programmatic_object_shape=-1,
                         duration_remaining=random_duration)
            debris_objects_array.append(new_debris_object)

    def hard_velocity_adjustment(self):
        '''
        Sharply change the AlienShip's velocity.
        '''

        # I think simplicity is best, given what
        # the Asteroids! Let's Plays showed.

        if (len(player_ship_objects_array) > 0):
            for each_player_ship in player_ship_objects_array:

                x_distance_between_alien_and_player \
                    = each_player_ship.x - self.x
                y_distance_between_alien_and_player \
                    = each_player_ship.y - self.y
                distance_between_them_as_hypotenuse \
                    = math.sqrt((x_distance_between_alien_and_player
                                 * x_distance_between_alien_and_player)
                                + (y_distance_between_alien_and_player
                                   * y_distance_between_alien_and_player))

                if distance_between_them_as_hypotenuse <= 150:
                    # If near to the player's ship,
                    # adjust movement direction randomly.
                    random_angle = random.randint(0, 359)

                    new_x_velocity, new_y_velocity \
                        = rotate_these_points_around_that_point(
                            self.x_velocity, self.y_velocity,
                            0, 0, random_angle)

                    self.x_velocity = new_x_velocity
                    self.y_velocity = new_y_velocity

                else:
                    # If the alien ship is far from the player's ship,
                    # adjust movement direction to move towards
                    # the player's ship.
                    ratio_of_alien_max_velocities_per_hypotenuse \
                        = (self.max_velocity
                           / distance_between_them_as_hypotenuse)
                    new_alien_ship_x_velocity \
                        = (x_distance_between_alien_and_player
                           * ratio_of_alien_max_velocities_per_hypotenuse)
                    new_alien_ship_y_velocity \
                        = (y_distance_between_alien_and_player
                           * ratio_of_alien_max_velocities_per_hypotenuse)
                    self.x_velocity = new_alien_ship_x_velocity
                    self.y_velocity = new_alien_ship_y_velocity

        else:
            # For when the player is not around.
            random_angle = random.randint(0, 359)
            new_x_velocity, new_y_velocity \
                = rotate_these_points_around_that_point(self.x_velocity,
                                                        self.y_velocity,
                                                        0, 0, random_angle)
            self.x_velocity = new_x_velocity
            self.y_velocity = new_y_velocity

    def attempt_to_avoid_an_asteroid(self):
        '''
        Scan for nearby asteroids and adjust heading to to avoid them.
        '''

        if (len(asteroid_objects_array) > 0):
            for each_asteroid in asteroid_objects_array:
                x_distance_between_alien_and_rock = self.x - each_asteroid.x
                y_distance_between_alien_and_rock = self.y - each_asteroid.y
                distance_between_them_as_hypotenuse \
                    = math.sqrt((x_distance_between_alien_and_rock
                                 * x_distance_between_alien_and_rock)
                                + (y_distance_between_alien_and_rock
                                   * y_distance_between_alien_and_rock))
                if distance_between_them_as_hypotenuse <= 50:
                    self.x_velocity *= -1
                    self.y_velocity *= -1

    def shoot_at_random_angle(self):
        '''
        Cause the alien ship to shoot at a random angle.
        '''

        random_alien_shot_angle = random.randint(0, 359)
        alien_shot_x_velocity, alien_shot_y_velocity \
            = rotate_these_points_around_that_point(0, -14, 0, 0,
                                                    random_alien_shot_angle)

        new_shot_object = Shot(self.x, self.y,
                               alien_shot_x_velocity,
                               alien_shot_y_velocity,
                               0,
                               self.current_angle_in_degrees,
                               is_owned_by_player=self.is_owned_by_player,
                               programmatic_object_shape=-1,
                               size=4,
                               duration_remaining=26)
        shot_objects_array.append(new_shot_object)


class Shot(GameObject):
    '''
    Shot objects are spawned by PlayerShips and AlienShips
    during their respective shooting events.

    Shots will destroy Asteroids on contact.
    Shots may destroy PlayerShips or AlienShips if their
    is_owned_by_player check fails or passes, respectively.

    See the GameObject move function for details
    on Shot collision detection and effects.
    '''
    # Why am I making empty classes?
    # Answer: isinstance checking.
    # ... and future modularity.

    pass


class Debris(GameObject):
    '''
    Debris objects spawn from destroyed
    Asteroids, PlayerShips, and AlienShips.
    '''

    pass


class UserInterfaceObject(GameObject):
    '''
    Create a UserInterfaceObject, inheriting
    from GameObject for visual display.

    UserInterfaceObjects do not process physics.
    '''

    def __init__(self, *args, **kwargs):

        # This transition to star-args is becoming considerably
        # more complicated than I believed it would be.
        # Nevertheless, this works perfectly:
        GameObject.__init__(self, *args, **kwargs)

        self.player_life_icon_number = kwargs['player_life_icon_number']


# # # # Functions # # # #


def spawn_new_player_ship():
    ''' Create the player's Ship object. '''
    
    global time_since_player_ship_spawned
    
    if ( (len(player_ship_objects_array) == 0) and (len(debris_objects_array) == 0) ):
        
        time_since_player_ship_spawned = 0
    
        new_player_ship_size = NPS_size = 30
        new_player_ship_starting_coords = NPS_starting_coords_upperleft_x, NPS_starting_coords_upperleft_y = ((SCREEN_WIDTH // 2) - (NPS_size / 2)), ((SCREEN_HEIGHT // 2) - (NPS_size / 2))

        new_player_ship_object = PlayerShip(NPS_starting_coords_upperleft_x, NPS_starting_coords_upperleft_y, 0, 0, 0, is_owned_by_player=True, programmatic_object_shape=0, color=WHITE, size=NPS_size, max_velocity=8)
        player_ship_objects_array.append(new_player_ship_object)    
    
    
def randomly_generate_new_alien_ship():
    '''
    Create a new AlienShip object with randomly
    generated features at the edge of the map.
    '''

    # Generate a random direction for the
    # alien ship to travel in at speed 4.
    # Note: The velocity will be inverted if it threatens to head
    # straight off the map after spawning;
    # see below in the placement generator.
    random_velocity_angle = random.randint(0, 359)
    random_alien_x_velocity, random_alien_y_velocity \
        = rotate_these_points_around_that_point(0, -5, 0, 0,
                                                random_velocity_angle)

    random_size_selector = random.randint(1, 2)
    if random_size_selector == 1:
        random_alien_size = 40
    elif random_size_selector == 2:
        random_alien_size = 20

    random_x_and_y = random.randint(1, 4)
    if random_x_and_y <= 2:
        # Then it's on the top or bottom (use Y values of min and max).

        # Select the x location:
        random_starting_x = random.randint(1, MAP_X2)
        if random_x_and_y == 1:
            # Then it's on the top.
            random_starting_y = -120
            # ... incidentally, -120 should probably be changed
            # to a fraction of map size, proportional to how much
            # bigger the map size is compared to the screen...
            # with a hard minimum bound set at
            # (radius_of_the_largest_spawnable_object + 1).
            # But this isn't strictly necessary.

        elif random_x_and_y == 2:
            # Then it's on the bottom.
            random_starting_y = (MAP_Y2 - 120)
            # Keep the alien from sliding off the map immediately.
            # This is only needed if the ship stars on the bottom.
            random_alien_y_velocity = (random_alien_y_velocity * -1)

    elif (random_x_and_y > 2):
        # Then it's on the left or right (use X values of min and max).
        # Select the y location:
        random_starting_y = random.randint(1, MAP_Y2)
        if random_x_and_y == 3:
                # Then it's on the left.
                random_starting_x = -120
        elif random_x_and_y == 4:
            # Then it's on the right.
            random_starting_x = (MAP_X2 - 120)
            # Keep the alien from sliding off the map immediately.
            # This is only needed if the ship stars on the bottom.
            random_alien_x_velocity = (random_alien_x_velocity * -1)

    new_alien_ship_object = AlienShip(random_starting_x,
                                      random_starting_y,
                                      random_alien_x_velocity,
                                      random_alien_y_velocity,
                                      0,
                                      programmatic_object_shape=-4,
                                      size=random_alien_size)
    alien_ship_objects_array.append(new_alien_ship_object)


def create_new_asteroid_object(supplied_starting_x=None, supplied_starting_y=None, supplied_x_velocity=None, supplied_y_velocity=None, supplied_angular_velocity=None, supplied_asteroid_size=None, supplied_asteroid_shape=None):
    ''' Create a new Asteroid object, with wholely or partially randomly generated features, at the edge of the map or at specific coordinates, with specific velocity, shape and size, depending on parameters. '''
    
    if ((supplied_x_velocity == None) or (supplied_y_velocity == None)):
        random_x_velocity_selector = random.randint(2, 6)
        random_y_velocity_selector = random.randint(2, 6) 
    else:
        random_x_velocity_selector = supplied_x_velocity
        random_y_velocity_selector = supplied_y_velocity    
    
    if supplied_angular_velocity == None:
        random_angular_velocity_selector = random.randint(1, 3)
    else:
        random_angular_velocity_selector = supplied_angular_velocity
    
    
    if supplied_asteroid_size == None:
        ## If a size was not supplied as a parameter at the function call, generate a number for the asteroid's size.
        
        random_size_selector = random.randint(1, 3)

    elif ((supplied_asteroid_size == 100) or (supplied_asteroid_size == 50) or (supplied_asteroid_size == 20)):    
        
        if supplied_asteroid_size == 100:
            random_size_selector = 1
        elif supplied_asteroid_size == 50:
            random_size_selector = 2
        else:
            random_size_selector = 3
        
    else:
        # print("Error in create_new_asteroid_object() ... supplied_asteroid_size == " + str(supplied_asteroid_size))
        pass

    
    if random_size_selector == 1:
        ## Note: These lines are scaling operations rather than randint() creations themselves.
        random_size = 100
        random_starting_x_velocity = (random_x_velocity_selector / 3)
        random_starting_y_velocity = (random_y_velocity_selector / 3)        
        random_max_velocity = 3
        random_angular_velocity = random_angular_velocity_selector
    elif random_size_selector == 2:
        random_size = 50
        random_starting_x_velocity = (random_x_velocity_selector / 1.5)
        random_starting_y_velocity = (random_y_velocity_selector / 1.5)
        random_max_velocity = 6
        random_angular_velocity = random_angular_velocity_selector * 2
    elif random_size_selector == 3:
        random_starting_x_velocity = random_x_velocity_selector
        random_starting_y_velocity = random_y_velocity_selector
        random_size = 20
        random_max_velocity = 9
        random_angular_velocity = random_angular_velocity_selector * 3
    else:
        # print("Weird error in create_new_asteroid_object()!")

        pass

    
    if ((supplied_starting_x == None) or (supplied_starting_y == None)):    
        ## If x and y coords were not supplied as parameters at the function call, generate an asteroid at the edge of the map.
        
        random_x_and_y = random.randint(1, 4)
        
        if random_x_and_y <= 2:
            ## Then it's on the top or bottom (use Y values of min and max).
            
            ## Select the x location:
            random_starting_x = random.randint(1, (MAP_X2))
            
            if random_x_and_y == 1:
                ## Then it's on the top.
                random_starting_y = -120
                
            elif random_x_and_y == 2:
                ## Then it's on the bottom.
                random_starting_y = (MAP_Y2 - 120)
                ## Keeps the asteroid from sliding off the map immediately:
                random_starting_y_velocity = (random_starting_y_velocity * -1)
        
        elif (random_x_and_y > 2):
            ## Then it's on the left or right (use X values of min and max).
            
            ## Select the y location:
            random_starting_y = random.randint(1, (MAP_Y2))
                
            if random_x_and_y == 3:
                ## Then it's on the left.
                random_starting_x = -120
                
            elif random_x_and_y == 4:
                ## Then it's on the right.
                random_starting_x = (MAP_X2 - 120)   
                
                ## Keeps the asteroid from sliding off the map immediately:
                random_starting_x_velocity = (random_starting_x_velocity * -1)
    else:
        random_starting_x = supplied_starting_x
        random_starting_y = supplied_starting_y
    
    if supplied_asteroid_shape == None:
        ## If an asteroid shape number was not supplied as a parameter at the function call, generate an asteroid shape number.
        ## Not enough art assets to be random yet!
        ## HOORAY two art assets. ... four...
        random_asteroid_shape = random.randint(1, 4)
    else:
        random_asteroid_shape = supplied_asteroid_shape
    
    new_asteroid_object = Asteroid(random_starting_x, random_starting_y, random_starting_x_velocity, random_starting_y_velocity, random_angular_velocity, current_angle_in_degrees=0, programmatic_object_shape=random_asteroid_shape, size=random_size)
    
    
    asteroid_objects_array.append(new_asteroid_object)


def render_all():
    ''' Draw every GameObject in the main arrays via their draw() command. '''

    screen.fill(BLACK)
        
        
    if len(asteroid_objects_array) > 0:
        for each_asteroid_object in range(0, len(asteroid_objects_array)):
            asteroid_objects_array[each_asteroid_object].draw()
    
    if len(shot_objects_array) > 0:
        for each_shot_object in range(0, len(shot_objects_array)):
            shot_objects_array[each_shot_object].draw()
    
    if len(player_ship_objects_array) > 0:
        for each_player_ship in range(0, len(player_ship_objects_array)):
            player_ship_objects_array[each_player_ship].draw()

    if len(alien_ship_objects_array) > 0:
        for each_alien_ship_object in range(0, len(alien_ship_objects_array)):
            alien_ship_objects_array[each_alien_ship_object].draw()
            
    if len(debris_objects_array) > 0:
        for each_debris_object in range(0, len(debris_objects_array)):
            debris_objects_array[each_debris_object].draw()
        
    ## UserInterfaceObjects should be drawn last.
    if len(player_life_icons_array) > 0:
        for each_player_life_icon in range(0, len(player_life_icons_array)):
            player_life_icons_array[each_player_life_icon].draw()
    
    ## The score counter:
    ## font.render(text_to_be_rendered, ???, color) 
    if game_is_on_start_screen == False:
        score_text = font.render(str(score), True, WHITE)
    
        ## screen.blit(---^, (x, y)
        screen.blit(score_text, (110, 16))
    
    
    
    if ( (len(player_life_icons_array) <= 0) and (game_is_on_start_screen == False) ):
        game_over_text = font.render('GAME OVER', True, WHITE)
        screen.blit(game_over_text, ((SCREEN_CENTER_X - 95),(SCREEN_CENTER_Y - 90)))
    
    if game_is_on_start_screen == True:
    
        
        asteroids_title_text = big_huge_font.render('ASTEROIDS', True, WHITE)
        screen.blit(asteroids_title_text, ((SCREEN_CENTER_X - 315),(SCREEN_CENTER_Y - 165)))
    
        play_game_text = font.render('PLAY GAME', True, WHITE)
        screen.blit(play_game_text, ((SCREEN_CENTER_X - 95),(SCREEN_CENTER_Y + 60)))
        
        ## New in 9.4!
        controls_help_tag = tiny_little_font.render('Q W E A S D F SPACE', True, WHITE)
        screen.blit(controls_help_tag, ((SCREEN_CENTER_X - 89), (SCREEN_HEIGHT - 30)))
          
        
    
    
    pygame.display.flip()
    

    
def add_player_life():
    ''' Add a life to the player's total. '''

    global player_lives_left
        
    new_icon_x = (140 + (player_lives_left * 32))
    new_icon_y = 75

    player_lives_left += 1
        
    new_player_life_icon = UserInterfaceObject(new_icon_x, new_icon_y, 0, 0, 0, current_angle_in_degrees=0, size=30, color=WHITE, programmatic_object_shape=0, player_life_icon_number=player_lives_left)
        
    player_life_icons_array.append(new_player_life_icon)
    

def remove_player_life():
    ''' Remove a life from the player's total. '''
    
    global player_lives_left
    
    for each_icon in player_life_icons_array:
        if each_icon.player_life_icon_number == player_lives_left:
            if each_icon in player_life_icons_array:
                player_life_icons_array.remove(each_icon)
                
                player_lives_left -= 1


def restart_game():
    ''' Add three player lives, reset the score, clear all asteroids/aliens/shots, and spawn the ship. '''

    global score
    
    if ( (len(player_ship_objects_array) == 0) and (len(debris_objects_array) == 0) ):
            
        score = 0
        
        clear_all_game_objects_from_the_map()
        
        add_player_life()
        add_player_life()
        add_player_life()
        
        spawn_new_player_ship()
        

def clear_all_game_objects_from_the_map():
    ''' Clear all GameObjects from the map. '''

    ## It wasn't doing it all in one pass, so repetition.
    ## I think deleting an entire array of many objects via foo.remove() isn't actually the proper way to go about doing it.
    ## Now I'm certain this can't be the right way to go about doing it. range(0, 2) was NOT sufficient to wipe all the asteroids...
    ## ... one from a split after the player ship hit a medium asteroid stuck around after range(0, 2) repetitions! WHY. -_-
    for each_repetition in range(0, 22):
        if len(asteroid_objects_array) > 0:
            for each_asteroid in asteroid_objects_array:
                if each_asteroid in asteroid_objects_array:
                    asteroid_objects_array.remove(each_asteroid)

        if len(shot_objects_array) > 0:
            for each_shot in shot_objects_array:
                if each_shot in shot_objects_array:
                    shot_objects_array.remove(each_shot)
                        
        if len(shot_objects_array) > 0:
            for each_shot in shot_objects_array:
                if each_shot in shot_objects_array:
                    shot_objects_array.remove(each_shot)        
                        
        if len(alien_ship_objects_array) > 0:
            for each_alien_ship in alien_ship_objects_array:
                if each_alien_ship in alien_ship_objects_array:
                    alien_ship_objects_array.remove(each_alien_ship)


def return_euclidean_distance(first_object, second_object):
    '''
    Return the Euclidean distance between two objects,
    both of which must have x and y attributes.
    '''
    # See also the Pythagorean theorem.
    # It's fascinating how frequently I use that in everyday life,
    # but I suppose as a programmer it's to be expected.
    x_distance = first_object.x - second_object.x
    y_distance = first_object.y - second_object.y

    square_of_x = x_distance ** 2
    square_of_y = y_distance ** 2

    sum_of_the_squares = square_of_x + square_of_y
    euclidean_distance = math.sqrt(sum_of_the_squares)

    return euclidean_distance


def draw_programmatic_object(x, y, current_angle_in_degrees, this_programmatic_object_shape=1, color=WHITE, size=100):
    ''' Use GameObject parameters to draw programmatic graphics reflective of the GameObject's properties. Does not display.flip(). '''     
        
    scaling_coefficient = (size / 20)
        
    
    if this_programmatic_object_shape == 0:
        ## It's the player ship.
        #supplied_programmatic_object_shape = [  3, [[   0, -10], [6, 10]], [[   0, -10], [-6,10]], [[-5.3,6.6], [5.3,6.6]] ]
        supplied_programmatic_object_shape = [ [[   0, -10], [6, 10]], [[   0, -10], [-6,10]], [[-5.3,6.6], [5.3,6.6]] ]

        
    if this_programmatic_object_shape == 1:
        ## It's the first asteroid shape -- deep fracture in the left and bottom.
        #supplied_programmatic_object_shape = [ 11, [[   4, -10], [ 10,  -3]], [[ 10,  -3], [ 10,   0]], [[  10,   0], [  3,  10]], [[   3,  10], [ -2,  10]], [[  -2,  10], [ -1,   0]], [[  -1,   0], [ -5,  10]], [[  -5,  10], [-10,   1]], [[ -10,   1], [ -5,  -1]], [[  -5,  -1], [-10,  -2]], [[ -10,  -2], [ -3, -10]], [[  -3, -10], [  4, -10]], ]
        supplied_programmatic_object_shape = [ [[   4, -10], [ 10,  -3]], [[ 10,  -3], [ 10,   0]], [[  10,   0], [  3,  10]], [[   3,  10], [ -2,  10]], [[  -2,  10], [ -1,   0]], [[  -1,   0], [ -5,  10]], [[  -5,  10], [-10,   1]], [[ -10,   1], [ -5,  -1]], [[  -5,  -1], [-10,  -2]], [[ -10,  -2], [ -3, -10]], [[  -3, -10], [  4, -10]], ]
        
    if this_programmatic_object_shape == 2:
        ## It's the second asteroid shape -- looks like a blunt mushroom with the cap pointing down and to the left.
        #supplied_programmatic_object_shape = [ 10, [[   0,  -6], [  6, -10]], [[  6, -10], [ 10,-6.5]], [[  10,-6.5], [  7,-0.5]], [[   7,-0.5], [ 10,   6]], [[  10,   6], [  3,  10]], [[   3,  10], [-6.5, 10]], [[-6.5,  10], [-10,   7]], [[ -10,   7], [-10,-5.5]], [[ -10,-5.5], [-5.5,-10]], [[-5.5, -10], [  0,  -6]] ]
        supplied_programmatic_object_shape = [ [[   0,  -6], [  6, -10]], [[  6, -10], [ 10,-6.5]], [[  10,-6.5], [  7,-0.5]], [[   7,-0.5], [ 10,   6]], [[  10,   6], [  3,  10]], [[   3,  10], [-6.5, 10]], [[-6.5,  10], [-10,   7]], [[ -10,   7], [-10,-5.5]], [[ -10,-5.5], [-5.5,-10]], [[-5.5, -10], [  0,  -6]] ]
        
    if this_programmatic_object_shape == 3:
        ## It's the third asteroid shape -- 
        supplied_programmatic_object_shape = [[[-1.2, -0.4], [-9.8, -5.2]], [[-9.8, -5.2], [-4.5, -10.0]], [[-4.5, -10.0], [-1.5, -8.1]], [[-1.5, -8.1], [6.1, -10.0]], [[6.1, -10.0], [10.0, -2.9]], [[10.0, -2.9], [10.0, 5.3]], [[10.0, 5.3], [2.5, 5.2]], [[2.5, 5.2], [5.5, 10.0]], [[5.5, 10.0], [-2.0, 9.8]], [[-2.0, 9.8], [-9.8, 5.0]], [[-9.8, 5.0], [-9.9, 2.7]], [[-9.9, 2.7], [-1.2, -0.4]]]
        
    if this_programmatic_object_shape == 4:
        ## It's the fourth asteroid shape -- 
        supplied_programmatic_object_shape = [[[-4.0, 9.0], [-10.0, 5.0]], [[-10.0, 5.0], [-4.0, 2.0]], [[-4.0, 2.0], [-10.0, -2.0]], [[-10.0, -2.0], [-4.0, -10.0]], [[-4.0, -10.0], [2.0, -7.0]], [[2.0, -7.0], [4.0, -10.0]], [[4.0, -10.0], [9.0, -5.0]], [[9.0, -5.0], [7.0, -1.0]], [[7.0, -1.0], [7.0, -1.0]], [[7.0, -1.0], [10.0, 4.0]], [[10.0, 4.0], [4.0, 10.0]], [[4.0, 10.0], [0.0, 7.0]], [[0.0, 7.0], [-4.0, 9.0]]]
        
    if this_programmatic_object_shape == -1:
        ## It's a rectangle.
        supplied_programmatic_object_shape = [ 0 ]
    
    if this_programmatic_object_shape == -2:
        ## It's the player's ship's exhaust.
        #supplied_programmatic_object_shape = [  2, [[  -2.5,  6.6], [   0, 14]], [[   0, 14], [   2.5,  6.6]] ]
        supplied_programmatic_object_shape = [ [[  -2.5,  6.6], [   0, 14]], [[   0, 14], [   2.5,  6.6]] ]

    if this_programmatic_object_shape == -3:
        ## Then it's a single line.
        #supplied_programmatic_object_shape = [  1, [[   0,   -6], [   0,  6]] ]
        supplied_programmatic_object_shape = [ [[   0,   -6], [   0,  6]] ]

    if this_programmatic_object_shape == -4:
        ## Then it's an alien ship. Also, I think the graphics quality could probably be better; it's supposed to look like three sharply aligned trapezoids, not a cakewreck.
        # bad one. blergh. hand drawn. #supplied_programmatic_object_shape = [[[3.6, 6.5], [-4.0, 6.0]], [[-4.0, 6.0], [-6.0, 2.0]], [[-6.0, 2.0], [-12.0, -2.0]], [[-12.0, -2.0], [-6.0, -6.0]], [[-6.0, -6.0], [4.0, -6.0]], [[4.0, -6.0], [11.0, -2.0]], [[11.0, -2.0], [5.0, 2.0]], [[5.0, 2.0], [3.6, 6.5]], [[-11.0, -2.0], [11.0, -2.0]], [[-5.5, 2.9], [5.5, 2.9]]]
        supplied_programmatic_object_shape = [ [[ 3.4, -7.5], [ 5.3,-2.5]], [[ 5.3,-2.5], [11,2.5]], [[11,2.5], [5.3,7.5]], [[5.3,7.5], [-5.3,7.5]], [[-5.3,7.5], [-11,2.5]], [[-11,2.5], [-5.3,-2.5]], [[-5.3,-2.5], [-3.4,-7.5]], [[-3.4,-7.5], [3.4,-7.5]], [[-5.3,-2.5], [5.3,-2.5]], [[-11,2.5], [11,2.5]] ]
        
    '''
            
    #~~~ START OF EXAMPLE OF A PROGRAMMATIC OBJECT ARRAY ~~~#        
            
    programmatic_object_shape == 1:
        [
            # 11,  # <--- superfluous, removed line
                [[   4, -10], [ 10,  -3]],  # 0
                [[  10,  -3], [ 10,   0]],  # 1
                [[  10,   0], [  3,  10]],  # 2
                [[   3,  10], [ -2,  10]],  # 3
                [[  -2,  10], [ -1,   0]],  # 4
                [[  -1,   0], [ -5,  10]],  # 5
                [[  -5,  10], [-10,   1]],  # 6
                [[ -10,   1], [ -5,  -1]],  # 7
                [[  -5,  -1], [-10,  -2]],  # 8
                [[ -10,  -2], [ -3, -10]],  # 9
                [[  -3, -10], [  4, -10]],  # 10
        ]
        
    #~~~ END OF EXAMPLE OF A PROGRAMMATIC OBJECT ARRAY ~~~#
    
    '''
    
    ## Actually drawing the programmatic object given the above parameters:
    
    ## Note: range(1, foo) is critical because 0th place is the number of lines in the object, not a line in itself. Probably can be factored out but I think it helps the legibility of the array. Perhaps it's not a good tradeoff, though...
    #if (len(supplied_programmatic_object_shape) <= 1):
    #    ## Urgh, I almost want to factor it out right now, but legibility is important. For the moment, anyways...   See above note.
    #    for each_line_ordinal in range(1, (supplied_programmatic_object_shape[0] + 1)):
    #        line_start_x, line_start_y   =   rotate_these_points_around_that_point((x + (supplied_programmatic_object_shape[each_line_ordinal][0][0] * scaling_coefficient)), (y + (supplied_programmatic_object_shape[each_line_ordinal][0][1] * scaling_coefficient)), x, y, current_angle_in_degrees)
    #        line_end_x, line_end_y       =   rotate_these_points_around_that_point((x + (supplied_programmatic_object_shape[each_line_ordinal][1][0] * scaling_coefficient)), (y + (supplied_programmatic_object_shape[each_line_ordinal][1][1] * scaling_coefficient)), x, y, current_angle_in_degrees)
    #        
    #        pygame.draw.line(screen, color, [line_start_x, line_start_y], [line_end_x, line_end_y], 1)            
    #else:
    #    for each_line_ordinal in range(0, (len(supplied_programmatic_object_shape))):
    #        line_start_x, line_start_y   =   rotate_these_points_around_that_point((x + (supplied_programmatic_object_shape[each_line_ordinal][0][0] * scaling_coefficient)), (y + (supplied_programmatic_object_shape[each_line_ordinal][0][1] * scaling_coefficient)), x, y, current_angle_in_degrees)
    #        line_end_x, line_end_y       =   rotate_these_points_around_that_point((x + (supplied_programmatic_object_shape[each_line_ordinal][1][0] * scaling_coefficient)), (y + (supplied_programmatic_object_shape[each_line_ordinal][1][1] * scaling_coefficient)), x, y, current_angle_in_degrees)
    #        
    #        pygame.draw.line(screen, color, [line_start_x, line_start_y], [line_end_x, line_end_y], 1)            
    
    
    if ( (len(supplied_programmatic_object_shape) > 1) or (this_programmatic_object_shape == -3) ):
        for each_line_index_number in range(0, (len(supplied_programmatic_object_shape))):
            line_start_x, line_start_y   =   rotate_these_points_around_that_point((x + (supplied_programmatic_object_shape[each_line_index_number][0][0] * scaling_coefficient)), (y + (supplied_programmatic_object_shape[each_line_index_number][0][1] * scaling_coefficient)), x, y, current_angle_in_degrees)
            line_end_x, line_end_y       =   rotate_these_points_around_that_point((x + (supplied_programmatic_object_shape[each_line_index_number][1][0] * scaling_coefficient)), (y + (supplied_programmatic_object_shape[each_line_index_number][1][1] * scaling_coefficient)), x, y, current_angle_in_degrees)
                
            pygame.draw.line(screen, color, [line_start_x, line_start_y], [line_end_x, line_end_y], 1)        
        
    
        
        
    if this_programmatic_object_shape == -1:
        ## Then it's a rectangle (a shot).
        pygame.draw.rect(screen, color, [(x - 3), (y - 3), (size - 2), (size - 2)])    
            
    
            
    
def rotate_these_points_around_that_point(point_x, point_y, center_x, center_y, angle_to_rotate_to_in_degrees):
    
    ''' Rotate a point (x, y) around another point (center_x, center_y) by an angle where (parameter[0], parameter[1]) == (x, y) and (parameter[2], parameter[3]) == (center_x, center_y) and parameter(4) == the angle. '''
    
    x_length = point_x - center_x
    y_length = point_y - center_y
        
    new_x = (x_length * math.cos(math.radians(angle_to_rotate_to_in_degrees))) - (y_length * math.sin(math.radians(angle_to_rotate_to_in_degrees)))
    new_y = (x_length * math.sin(math.radians(angle_to_rotate_to_in_degrees))) + (y_length * math.cos(math.radians(angle_to_rotate_to_in_degrees)))
    
    new_x += center_x
    new_y += center_y

    return new_x, new_y    
        
    
def handle_keys():

    ''' Interpret pressed keys as input commands. '''

    global player_ammo
    global player_is_accelerating
    global game_paused
    global keep_window_open
    global game_is_on_start_screen
    
    ## Is it bad to have a lot of things in the global namespace?

    
    for event in pygame.event.get():   # NOTE: This does not seem to allow for continuously-held-down keys being re-read if another key is pressed and released during the first key's held period.
        if event.type == pygame.QUIT:
            sys.exit
        elif event.type == pygame.KEYDOWN:
            # KEYDOWN prevents interpreting holding down
            # the button as multiple keypresses.
            
            if event.key == pygame.K_ESCAPE:
                sys.exit
                pygame.quit
                keep_window_open = False ## NOTE: Only this line ACTUALLY works!
                # END PROGRAM DOT YES REALLY.
            
            if event.key == pygame.K_r:
                if game_paused == False:
                    game_paused = True
                elif game_paused == True:
                    game_paused = False
        
            if ( (len(player_ship_objects_array) > 0) and (game_paused == False) ):
                if ((event.key == pygame.K_SPACE) or (event.key == pygame.K_f)):    
                
                    if (are_we_using_player_ammo_this_game == True):
                        if (player_ammo >= 1):
                            for each in player_ship_objects_array:
                                each.fire_particle_cannon()
                                player_ammo -= 1
                    else:
                        for each in player_ship_objects_array:
                            each.fire_particle_cannon()
                        
                    player_fired_shot = True
            
            ## If the player hits space, respawn the player ship if the player is dead, player_lives_left > 0, debris_objects_array is empty and we're not on the start screen.
            elif ( (len(player_ship_objects_array) == 0) and (player_lives_left > 0) and (game_is_on_start_screen == False) and (len(debris_objects_array) == 0) ):
                if event.key == pygame.K_SPACE:
                    spawn_new_player_ship()
                    
            ## Reset the game to the start screen when the player hits space if the player is dead and player_lives_left <= 0 and we're not on the start screen and debris_objects_array is empty.        
            elif ( (len(player_ship_objects_array) == 0) and (player_lives_left <= 0) and (game_is_on_start_screen == False) and (len(debris_objects_array) == 0) ):
                if event.key == pygame.K_SPACE:
                    game_is_on_start_screen = True
                    clear_all_game_objects_from_the_map()
                    #display_start_screen()
            
            ## If we're on the start screen and the player hits space, clear the start screen and restart the game.
            elif game_is_on_start_screen == True:
                if event.key == pygame.K_SPACE:
                    game_is_on_start_screen = False
                    restart_game()    
    
    keys_pressed = pygame.key.get_pressed()
    ## This section, unlike the KEYDOWN section, allows multiple keys to be held down simultaneously.
    
    if ( (len(player_ship_objects_array) > 0) and (game_paused == False) ):
        ## Turn the ship...
        
        x_velocity_modification_amount = 0
        y_velocity_modification_amount = 0
        angular_velocity_modification_amount = 0
        velocity_adjustment_key_was_pressed = False
                
        ## counter clockwise:
        if ((keys_pressed[pygame.K_LEFT]) or (keys_pressed[pygame.K_a])):
            if PLAYER_HAS_ANGULAR_VELOCITY == True:
                if player_ship_objects_array[0].angular_velocity > -12:
                    angular_velocity_modification_amount = -1
                    velocity_adjustment_key_was_pressed = True
                else:
                    pass
            else:
                player_ship_objects_array[0].adjust_current_angle(-12)
                    
        ## clockwise:                
        if ((keys_pressed[pygame.K_RIGHT]) or (keys_pressed[pygame.K_d])):
            if PLAYER_HAS_ANGULAR_VELOCITY == True:
                if player_ship_objects_array[0].angular_velocity < 12:
                    angular_velocity_modification_amount = 1
                    velocity_adjustment_key_was_pressed = True
                else:
                    pass
            else:
                player_ship_objects_array[0].adjust_current_angle(12)
        
        
        ## Move the ship...
            
        ## forwards:
        if ((keys_pressed[pygame.K_w]) or (keys_pressed[pygame.K_UP])):
            y_velocity_modification_amount = -1
            velocity_adjustment_key_was_pressed = True
            player_is_accelerating = True
            
        ## leftwards:
        if keys_pressed[pygame.K_q]: 

            x_velocity_modification_amount = -1
            velocity_adjustment_key_was_pressed = True
            player_is_accelerating = True
                
        ## rightwards:
        if keys_pressed[pygame.K_e]: 
                
            x_velocity_modification_amount = 1
            velocity_adjustment_key_was_pressed = True
            player_is_accelerating = True
            
            
        ## Brake the ship:
        if ((keys_pressed[pygame.K_s]) or (keys_pressed[pygame.K_DOWN])):

            player_ship_objects_array[0].brake_all_velocities()
            player_is_accelerating = True

                
        ## Brake the ship's angular velocity only:
        if keys_pressed[pygame.K_z]:
                    
            player_ship_objects_array[0].brake_all_velocities(only_braking_angular_velocity=True)
                    
        if velocity_adjustment_key_was_pressed == True:        
            player_ship_objects_array[0].adjust_all_velocities(x_velocity_modification_amount, y_velocity_modification_amount, angular_velocity_modification_amount)
    
    
    





# # # # Inits # # # #


## Initialize the screen
screen = pygame.display.set_mode(SCREEN_SIZE)


## This is needed for the font.
pygame.init()

## "intantiate the default system font" ...      |  ref: http://www.nerdparadise.com/tech/python/pygame/basics/part5/
font = pygame.font.Font(None, 45)
big_huge_font = pygame.font.Font(None, 150)
tiny_little_font = pygame.font.Font(None, 23)

## Create a clock object to make the game run at a specified speed in the main loop
clock = pygame.time.Clock()

## To keep the game running
keep_window_open = True

## Window title
pygame.display.set_caption(WINDOW_CAPTION)


## Init the GameObject arrays
asteroid_objects_array = []
shot_objects_array = []
alien_ship_objects_array = []
player_ship_objects_array = []
debris_objects_array = []
player_life_icons_array = []

#def __init__(self, starting_x, starting_y, x_velocity, y_velocity, max_velocity, angular_velocity, current_angle_in_degrees=0, size=1, color=WHITE, programmatic_object_shape=1, is_owned_by_player=False):
                

## Test asteroids
#third_new_asteroid_object = GameObject(0, 0, 1, 1, 1, size=100)
#asteroid_objects_array.append(third_new_asteroid_object)

#second_new_asteroid_object = GameObject(0, 0, 2, 2, 2, color=GREEN, size=50)
#asteroid_objects_array.append(second_new_asteroid_object)

#new_asteroid_object = GameObject(0, 0, 4, 4, 4, color=RED, size=25)
#asteroid_objects_array.append(new_asteroid_object)

#fourth_new_asteroid_object = GameObject(0, 0, 8, 8, 8, color=BLUE, size=12)
#asteroid_objects_array.append(fourth_new_asteroid_object)



## Player ship
## Commented out since we're on the start screen at the start, now.
#spawn_new_player_ship()

## Initializes a timer to make the player ship blink after it's been spawned. A specialized game ticker.
## Uhh... one Let's Play had a blink after respawn, another didn't, yet both were otherwise seemingly identical Asteroids!. Gonna leave this out for now.
time_since_player_ship_spawned = 0

## This should be a constant... maybe?
are_we_using_player_ammo_this_game = False

player_ammo = 1


player_lives_left = 0
## Commented out since we're on the start screen at the start, now.
#add_player_life()
#add_player_life()
#add_player_life()

## Protects the ship from being dragged to a stop when the player is moving it. Useful when PLAYER_SHIP_HAS_DRAG == True.
player_is_accelerating = False

## player_fired_shot works alongside player_is_accelerating to prevent exhaust from being shown only when the ship is not being accelerated manually AND the player is firing a shot.
player_fired_shot = False

## Init the game ticker -- it's used for making things happen at set intervals of each other in the main loop, independent of the game ticker (perhaps this should be factored out in favor of a 100% clock-based system)
game_ticker = 0

## The player's score
score = 0

## IMPORTANT: Leave the next line commented to force the player to spam the firing keys instead of allowing them to hold them down.
#pygame.key.set_repeat(20, 20)     #  <--- ==  when_a_key_is_held_down_it_will_repeat_its_KEYDOWN_signal_with(repeat_delay_in_milliseconds, repeat_interval_in_milliseconds)

## Starts the game... on the start screen.
game_is_on_start_screen = True



## Debugging globals
ratio_of_max_to_current_this_is_a_debugging_variable = 0
game_paused = False


# # # # Main Loop # # # #

while keep_window_open == True:


    ## Input handler variables
    button1_pressed, button2_pressed, button3_pressed = pygame.mouse.get_pressed()
    mouse_position = mouse_x, mouse_y = pygame.mouse.get_pos()

    ## The if lets the game keep displaying ship exhaust even when paused, when ship exhaust reasonably ought to continue being displayed.
    if game_paused == False:
        player_fired_shot = False
        player_is_accelerating = False

    ## Process keyboard input
    handle_keys()


    ## Game speed and event progression metering
    clock.tick(30)

    ## Asteroids shouldn't be pausible, but this should help with debugging.
    if game_paused == False:
        game_ticker += 1

    if ((game_ticker == 20) and (game_paused == False)):
        ## I don't know if this next line is helpful or not. That's probably a bad thing, but I want to worry about problems other than number size limitations right now! I'll learn it later and remember it forever after that point.
        game_ticker = 0

        if are_we_using_player_ammo_this_game == True:
            if player_ammo < 3:
                player_ammo += 1

        ## This controls how often asteroids spawn.
        ## if ( (number of asteroids currently in action) is fewer than (the number we'd prefer) ):
        if (len(asteroid_objects_array) < 14):
            create_new_asteroid_object()
        elif (len(asteroid_objects_array) < 24):
            asteroid_spawn_chance = random.randint(1, 100)
            if asteroid_spawn_chance > 30:
                create_new_asteroid_object()
        elif  (len(asteroid_objects_array) < 36):
            asteroid_spawn_chance = random.randint(1, 100)
            if asteroid_spawn_chance > 50:
                create_new_asteroid_object()
        elif  (len(asteroid_objects_array) < 48):
            asteroid_spawn_chance = random.randint(1, 100)
            if asteroid_spawn_chance > 90:
                create_new_asteroid_object()

        ## This controls how early and how often aliens spawn.
        if (score >= 20):
            if (len(alien_ship_objects_array) < 1):
                alien_ship_spawn_chance = random.randint(1, 100)
                if alien_ship_spawn_chance > 80:
                    randomly_generate_new_alien_ship()
            elif (len(alien_ship_objects_array) < 2):
                alien_ship_spawn_chance = random.randint(1, 100)
                if alien_ship_spawn_chance > 95:
                    randomly_generate_new_alien_ship()

    ## Move all GameObjects and adjust their angles
    if ((game_ticker >= 0) and (game_paused == False)):

        for each_asteroid_object in asteroid_objects_array:
            each_asteroid_object.move()
            each_asteroid_object.adjust_current_angle(each_asteroid_object.angular_velocity)


        for each_player_ship in player_ship_objects_array:
            each_player_ship.move()
            if PLAYER_HAS_ANGULAR_VELOCITY == True:
                each_player_ship.adjust_current_angle(each_player_ship.angular_velocity)
            if PLAYER_SHIP_HAS_DRAG == True:
                if ((player_is_accelerating == False) and (player_fired_shot == False)):
                    each_player_ship.brake_all_velocities(is_gradual_braking=True)


        for each_shot_object in shot_objects_array:
            each_shot_object.move()
            each_shot_object.adjust_current_angle(each_shot_object.angular_velocity)

            each_shot_object.decrement_duration_and_if_necessary_destroy(1)


        for each_debris_object in debris_objects_array:
            each_debris_object.move()
            each_debris_object.adjust_current_angle(each_debris_object.angular_velocity)

            ## Positive numbers decrement time remaining, negative numbers increment it. +1 brings it closer to deletion.
            each_debris_object.decrement_duration_and_if_necessary_destroy(1)

        for each_alien_ship_object in alien_ship_objects_array:
            each_alien_ship_object.move()
            ## Alien ships do not rotate.

            ## However, they can do other things, such as change directions without warning...
            random_alien_hard_velocity_adjustment_chance = random.randint(1, 100)
            if random_alien_hard_velocity_adjustment_chance > 98:
                each_alien_ship_object.hard_velocity_adjustment()
            elif random_alien_hard_velocity_adjustment_chance <= 3:
                each_alien_ship_object.attempt_to_avoid_an_asteroid()
                
            ## ... and fire Pixellus Cannons.
            random_alien_shot_chance = random.randint(1, 100)
            if random_alien_shot_chance > 70:
                each_alien_ship_object.pixellus_cannon_recharge_ticker += 1

            if each_alien_ship_object.pixellus_cannon_recharge_ticker >= 10:
                each_alien_ship_object.shoot_at_random_angle()
                each_alien_ship_object.pixellus_cannon_recharge_ticker = 0

    ## This part's debug code ---v
    if ( ((game_ticker % 4) == 1) and (game_paused == False) ):

        #if (len(asteroid_objects_array) > 0):
        #    # print("\nasteroid_objects_array[0].x_velocity == " + str(asteroid_objects_array[0].x_velocity))
        #    # print("asteroid_objects_array[0].y_velocity == " + str(asteroid_objects_array[0].y_velocity))
        #    # print("asteroid_objects_array[0].x == " + str(asteroid_objects_array[0].x))
        #    # print("asteroid_objects_array[0].y == " + str(asteroid_objects_array[0].y))
        #    # print("asteroid_objects_array[0].radius == " + str(asteroid_objects_array[0].radius))

        if (len(player_ship_objects_array) > 0):
            # print("\nplayer_ship_objects_array[0].x_velocity == " + str(player_ship_objects_array[0].x_velocity))
            # print("player_ship_objects_array[0].y_velocity == " + str(player_ship_objects_array[0].y_velocity))
            # print("hypotenuse_of_velocities == " + (str(math.sqrt((player_ship_objects_array[0].x_velocity * player_ship_objects_array[0].x_velocity) + (player_ship_objects_array[0].y_velocity * player_ship_objects_array[0].y_velocity)))))
            # print("ratio_of_max_to_current_vel_hyp == " + str(ratio_of_max_to_current_this_is_a_debugging_variable))
            # print("player_ship_objects_array[0].current_angle_in_degrees == " + str(player_ship_objects_array[0].current_angle_in_degrees))
            # print("player_ship_objects_array[0].x == " + str(player_ship_objects_array[0].x))
            # print("player_ship_objects_array[0].y == " + str(player_ship_objects_array[0].y))
            # print("player_ship_objects_array[0].radius == " + str(player_ship_objects_array[0].radius))

            pass

        if (len(debris_objects_array) > 0):
            # print("\ndebris_objects_array[0].x_velocity == " + str(debris_objects_array[0].x_velocity))
            # print("debris_objects_array[0].y_velocity == " + str(debris_objects_array[0].y_velocity))

            pass

        # print("\nMAP_X == " + str(MAP_X))
        # print("MAP_X2 == " + str(MAP_X2))
        # print("MAP_Y == " + str(MAP_Y))
        # print("MAP_Y2 == " + str(MAP_Y2))

    ## Note: I think we need to display things AFTER moving them.
    render_all()





pygame.quit
