import pygame
import sys
import math



## Refactor all.
## Key handler --> its own function.
## handle_keys() should go AFTER the foo.move() and blanket adjustment commands in the main loop (also, make the blanket adjustment a single function).
## For the slow_to_zero function, the velocity change should be a direct consequence of the actual nonrotated x/y velocities of the object.
## -- Try getting the x, y velocities' abs() as ratios of each other, and subdividing the smaller velocity's delta-v addition into even fractions based on the time it would take the larger one to hit zero at the max (0.4) delta-v rate.
## -- ^-- this is probably the best approach!





#### Constants ####

WINDOW_CAPTION = 'Asteroids! Test version 4.0'

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

MAP_SIZE = MAP_WIDTH, MAP_HEIGHT = SCREEN_WIDTH, SCREEN_HEIGHT # (SCREEN_WIDTH - 200), (SCREEN_HEIGHT - 200) #  for future reference, the map should be bigger than the screen's visible area to let stuff fly smoothly on and off the screen. (SCREEN_WIDTH + 200), (SCREEN_HEIGHT + 200)

PLAYING_FIELD = PLAYING_FIELD_WIDTH, PLAYING_FIELD_HEIGHT = SCREEN_WIDTH, SCREEN_HEIGHT # (MAP_WIDTH - 200), (MAP_HEIGHT - 200)

BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]


screen = pygame.display.set_mode(SCREEN_SIZE)



#### Classes ####

class GameObject:

	''' Create a programmatically-drawn object in the playing field. Object will be fully capable of movement. '''
	
	def __init__(self, starting_x, starting_y, x_velocity, y_velocity, max_velocity, angular_velocity, current_angle_in_degrees=0, size=1, color=WHITE, programmatic_object_shape=1, is_asteroid=False, is_owned_by_player=False, is_shot_object=False, is_alien_ship=False):
		
		self.starting_x = starting_x
		self.starting_y = starting_y

		self.x_velocity = x_velocity
		self.y_velocity = y_velocity
		
		self.max_velocity = max_velocity
		
		self.angular_velocity = angular_velocity
		self.current_angle_in_degrees = current_angle_in_degrees
		
		self.size = size
		
		self.w = self.size #* self.scaling_coefficient
		self.h = self.size #* self.scaling_coefficient

		
		self.color = color
		
		self.programmatic_object_shape = programmatic_object_shape
		
				

		self.is_asteroid = is_asteroid
		
		self.is_owned_by_player = is_owned_by_player
		
		self.is_shot_object = is_shot_object
		
		self.is_alien_ship = is_alien_ship

			

		## Initializes the ship position properly. Stuff starts in the top left and gets moved once into its expected starting position at the end of __init__().
		
		self.x = 0
		self.y = 0
		
		## Note: x2/y2 are incremented by move(), so they need to be 0 + w and 0 + h, respectively.
		self.x2 = self.w
		self.y2 = self.h
		

		self.center_x = (self.x + (self.w / 2))
		self.center_y = (self.y + (self.h / 2))
	
	
		self.move_by_specified_amount(self.starting_x, self.starting_y)

			
	def draw(self):
	
		''' Call draw_programmatic_object() with the GameObject's parameters. '''
		
		draw_programmatic_object(self.center_x, self.center_y, self.current_angle_in_degrees, self.programmatic_object_shape, self.color, self.size)
	
	
		
	def move_by_specified_amount(self, supplied_x_movement_amount, supplied_y_movement_amount):
	
		''' Move the GameObject by the specified x, y amount. '''
		
		self.x += supplied_x_movement_amount
		self.y += supplied_y_movement_amount	
			
		self.x2 += supplied_x_movement_amount
		self.y2 += supplied_y_movement_amount
			
		self.center_x += supplied_x_movement_amount
		self.center_y += supplied_y_movement_amount


	def move(self):
	
		''' Move the GameObject using its current velocity values; bounce off the edges of the playing field if indicated. '''
		
		if (self.x < 0):
			if self.is_shot_object == False:
				self.x_velocity = (abs(self.x_velocity) * 1)
				self.angular_velocity *= -1
			elif self.is_shot_object == True:
				if self in shot_objects_array:
					shot_objects_array.remove(self)
		if (self.x2 > PLAYING_FIELD_WIDTH):
			if self.is_shot_object == False:
				self.x_velocity = (abs(self.x_velocity) * -1)
				self.angular_velocity *= -1
			elif self.is_shot_object == True:
				if self in shot_objects_array:
					shot_objects_array.remove(self)
				
		if (self.y < 0):
			if self.is_shot_object == False:
				self.y_velocity = (abs(self.y_velocity) * 1)
				self.angular_velocity *= -1
			elif self.is_shot_object == True:
				if self in shot_objects_array:
					shot_objects_array.remove(self)
		if (self.y2 > PLAYING_FIELD_HEIGHT):
			if self.is_shot_object == False:
				self.y_velocity = (abs(self.y_velocity) * -1)
				self.angular_velocity *= -1
			elif self.is_shot_object == True:
				if self in shot_objects_array:
					shot_objects_array.remove(self)
			
		##   Should -v be before or after -^  ?
		
		self.move_by_specified_amount(self.x_velocity, self.y_velocity)
		
		

	def adjust_current_angle(self, angle_adjustment):
		
		''' Adjust the GameObject's current angle, in degrees. '''
	
		if self.current_angle_in_degrees != None:
		
			## This if check solves the bullet case, since bullets don't spin in Asteroids!
			
			self.current_angle_in_degrees += angle_adjustment
		
		if (abs(self.current_angle_in_degrees) >= 360):
			
			self.current_angle_in_degrees = 0
		

	def adjust_all_velocities(self, x_acceleration, y_acceleration, angular_acceleration):
	
		''' Apply acceleration to the GameObject's x_velocity, y_velocity, current_angle_in_degrees values; use self.current_angle_in_degrees to increment velocities appropriately. '''

		
		hypotenuse_of_x_and_y_velocities = math.sqrt((self.x_velocity * self.x_velocity) + (self.y_velocity * self.y_velocity))

	
		rotated_x_velocity_increment, rotated_y_velocity_increment = rotate_these_points_around_that_point(x_acceleration, y_acceleration, 0, 0, self.current_angle_in_degrees)      #   ship_center_x, ship_center_y, player_ship_objects_array[0].current_angle_in_degrees)
	
		
		
		#### X
		
		##  if    abs(net speed) > 10 ...           and is vectoring rightwards...  and wants to increment rightwards...  
		if ((hypotenuse_of_x_and_y_velocities > self.max_velocity) and (self.x_velocity >= 0) and (rotated_x_velocity_increment > 0)): #### Goal: I want the thing to NOT be going >10 pixels/tick UNROTATED velocity.
			## Then do nothing.
			self.x_velocity -= 0
			
			
			
			
		##  if abs(net speed) > 10 ...                and is vectoring leftwards...    and wants to increment leftwards...	
		elif ((hypotenuse_of_x_and_y_velocities > self.max_velocity) and (self.x_velocity <= 0) and (rotated_x_velocity_increment < 0)):
			## Then do nothing.
			self.x_velocity += 0
			
			
			
			
		else:  ## Otherwise...
			## ... increment x_velocity by the appropriate value.
			self.x_velocity += rotated_x_velocity_increment
		
			
		#### Y
		
		##  if    abs(net speed) > 10 ...           and is vectoring downwards...  and wants to increment downwards...     (( downwards is positive y values in pixelland ))
		if ((hypotenuse_of_x_and_y_velocities > self.max_velocity) and (self.y_velocity >= 0) and (rotated_y_velocity_increment > 0)):
			## Then do nothing.
			self.y_velocity -= 0
			
			
			
			
		## 	if abs(net speed) > 10 ...                and is vectoring upwards...    and wants to increment upwards...	
		elif ((hypotenuse_of_x_and_y_velocities > self.max_velocity) and (self.y_velocity <= 0) and (rotated_y_velocity_increment < 0)):
			## Then do nothing.
			self.y_velocity += 0
			
			
			
		else:  ## Otherwise...
			## ... increment y_velocity by the appropriate value.
			self.y_velocity += rotated_y_velocity_increment
		

		#### Theta
		
		## Very similar to the other velocities, except it doesn't have to care about the sign difference between grid direction and total velocity when checking its cap.
		if ((self.angular_velocity > 10) and (angular_acceleration > 0)):
			self.angular_velocity -= 0
		elif ((self.angular_velocity < -10) and (angular_acceleration < 0)):
			self.angular_velocity += 0
		else:
			self.angular_velocity += angular_acceleration
				
				
				

		
		
		
	
	def brake_all_velocities(self):
	
		''' Applies acceleration to the GameObject's x_velocity, y_velocity, current_angle_in_degrees values, consistently opposite to the direction of its velocities' current values. '''
	
		hypotenuse_of_x_and_y_velocities = math.sqrt((self.x_velocity * self.x_velocity) + (self.y_velocity * self.y_velocity))
	
	
		if (hypotenuse_of_x_and_y_velocities >= 1):
			## If some non-trivial adjustment needs to be made to x ior y velocities...
		
			## Get the smaller_to_bigger_ratio:	
			if (abs(self.x_velocity) >= abs(self.y_velocity)):
				## If X_v >= Y_v...
				smaller_to_bigger_ratio = ( ( abs(self.y_velocity) * 100 ) / ( abs(self.x_velocity) * 100 ) / 100 )  # I hate useless maths, but I think this may functionally protect against numerical instability. If there's a better idea, please do change it.

				if self.x_velocity > 0:
					## If X_v > Y_v and X_v is positive:
						self.x_velocity -= 0.4
				elif self.x_velocity < 0:
					## If X_v > Y_v and X_v is negative:
						self.x_velocity += 0.4
				
				if self.y_velocity > 0:
					## If X_v > Y_v and Y_v is positive:
					self.y_velocity -= (0.4 * smaller_to_bigger_ratio)
				elif self.y_velocity < 0:
					## If X_v > Y_v and Y_v is negative:
					self.y_velocity += (0.4 * smaller_to_bigger_ratio)


			elif (abs(self.x_velocity) < abs(self.y_velocity)):
				## If Y_v > X_v...
				smaller_to_bigger_ratio = ( ( abs(self.x_velocity) * 100 ) / ( abs(self.y_velocity) * 100 ) / 100 )
				
				if self.x_velocity > 0:
					## If Y_v > X_v and X_v is positive:
						self.x_velocity -= (0.4 * smaller_to_bigger_ratio)
				elif self.x_velocity < 0:
					## If Y_v > X_v and X_v is negative:
						self.x_velocity += (0.4 * smaller_to_bigger_ratio)
				
				if self.y_velocity > 0:
					## If Y_v > X_v and Y_v is positive:
					self.y_velocity -= 0.4
				elif self.y_velocity < 0:
					## If Y_v > X_v and Y_v is negative:
					self.y_velocity += 0.4
						

		elif (hypotenuse_of_x_and_y_velocities < 1):
			## Otherwise make the trivial adjustment.
			self.x_velocity = 0
			self.y_velocity = 0
			
			
		if (abs(self.angular_velocity) > 1):	
			## If a nontrivial adjustment needs to be made to angular velocity...
			if self.angular_velocity > 0:
				self.adjust_all_velocities(0, 0, -1)
			elif self.angular_velocity < 0:
				self.adjust_all_velocities(0, 0, 1)

		
		elif (abs(self.angular_velocity) <= 1):
			## Otherwise make the trivial adjustment.
			self.angular_velocity = 0
		
		
class Ship(GameObject):

	''' Make a GameObject controlled by either the player or the aliens. '''
	
	def firin_mah_lazor(self):

		''' Fire a shot with position and velocity info inherited from the firing ship. '''

		## Where it's firing from:   ((the front point of the ship))
		ship_front_tip_x = self.center_x
		ship_front_tip_y = self.y
		rotated_ship_tip_x, rotated_ship_tip_y = rotate_these_points_around_that_point(ship_front_tip_x, ship_front_tip_y, self.center_x, self.center_y, self.current_angle_in_degrees)
		shot_start_location_x = rotated_ship_tip_x
		shot_start_location_y = rotated_ship_tip_y
		

		
		
		## The vector it's traveling in:
		rotated_shot_velocity_x_modifier, rotated_shot_velocity_y_modifier = rotate_these_points_around_that_point(0, -10, 0, 0, self.current_angle_in_degrees)
		shot_velocity_seed_x = (self.x_velocity + rotated_shot_velocity_x_modifier)
		shot_velocity_seed_y = (self.y_velocity + rotated_shot_velocity_y_modifier) ## I hope this works! Shots are supposed to inherit the ship's base velocity. Newton's second law.
		
		
		
		
		## Make and append the shot object:
		new_shot_object = Shot(shot_start_location_x, shot_start_location_y, shot_velocity_seed_x, shot_velocity_seed_y, 0, self.current_angle_in_degrees, is_owned_by_player=self.is_owned_by_player, is_shot_object=True, programmatic_object_shape=-1, size=10)
		shot_objects_array.append(new_shot_object)
		
		
		## Repulsion effect on the ship. Tee hee.
		##IMPORTANT: Is it -1 or +1 for a tiny 10-size object to be repelled from a 40 size ship? (( It's +1, ship forwards is negative Y, backwards is positive Y )) This clearly needs more thought put into it. f=ma, but m is not really clear yet -- only size is clear, but size is the sqrt of m if size is the sqrt of the giant square programmatic object that is the ship. Fudging it for now, but value can be added by expanding this later!
		## Also note that, as above, the center x and y for this rotation are 0 because we're rotating a velocity value, not a positional value. --v

		
		self.adjust_all_velocities(0, 0.1, 0)
		
		
		
	

class Shot(GameObject):
	pass
	
	# MAEK HIT THANGS
		
	
		
#### Functions ####


def render_all():

	''' Draw every GameObject in the main arrays via their draw() command. '''

	screen.fill(BLACK)
		
	
	if len(asteroid_objects_array) > 0:
		for each_asteroid_object in range(0, len(asteroid_objects_array)):
			asteroid_objects_array[each_asteroid_object].draw()
	
	if len(player_ship_objects_array) > 0:
		for each_player_ship_object in range(0, len(player_ship_objects_array)):
			player_ship_objects_array[each_player_ship_object].draw()

	if len(shot_objects_array) > 0:
		for each_shot_object in range(0, len(shot_objects_array)):
			shot_objects_array[each_shot_object].draw()
	
	
	pygame.display.flip()
	

def draw_programmatic_object(center_x, center_y, current_angle_in_degrees, this_programmatic_object_shape=1, color=WHITE, size=100):
		
	''' Use GameObject parameters to draw programmatic graphics reflective of the GameObject's properties. Does not display.flip(). ''' 	
		
	scaling_coefficient = (size / 20)
		
	
	if this_programmatic_object_shape == 0:
		## It's the player ship.
		supplied_programmatic_object_shape = [  3, [[   0, -10], [6, 10]], [[   0, -10], [-6,10]], [[-5.3,6.6], [5.3,6.6]] ]

	if this_programmatic_object_shape == 1:
		## It's the first asteroid shape -- deep fracture in the left and bottom.
		supplied_programmatic_object_shape = [ 11, [[   4, -10], [ 10,  -3]], [[ 10,  -3], [ 10,   0]], [[  10,   0], [  3,  10]], [[   3,  10], [ -2,  10]], [[  -2,  10], [ -1,   0]], [[  -1,   0], [ -5,  10]], [[  -5,  10], [-10,   1]], [[ -10,   1], [ -5,  -1]], [[  -5,  -1], [-10,  -2]], [[ -10,  -2], [ -3, -10]], [[  -3, -10], [  4, -10]], ]

	if this_programmatic_object_shape == -1:
		## It's a shot.
		supplied_programmatic_object_shape = [ 0 ]
		
		
	'''
			
	#~~~ START OF EXAMPLE OF A PROGRAMMATIC OBJECT ARRAY ~~~#		
			
	programmatic_object_shape == 1:
		[
			11, 
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
	
	for each_line_ordinal in range(1, (supplied_programmatic_object_shape[0] + 1)):
		line_start_x, line_start_y   =   rotate_these_points_around_that_point((center_x + (supplied_programmatic_object_shape[each_line_ordinal][0][0] * scaling_coefficient)), (center_y + (supplied_programmatic_object_shape[each_line_ordinal][0][1] * scaling_coefficient)), center_x, center_y, current_angle_in_degrees)
		line_end_x, line_end_y       =   rotate_these_points_around_that_point((center_x + (supplied_programmatic_object_shape[each_line_ordinal][1][0] * scaling_coefficient)), (center_y + (supplied_programmatic_object_shape[each_line_ordinal][1][1] * scaling_coefficient)), center_x, center_y, current_angle_in_degrees)

		pygame.draw.line(screen, color, [line_start_x, line_start_y], [line_end_x, line_end_y], 1)			
		
		
	if this_programmatic_object_shape == -1:
		## Then it's a rectangle (a shot).
		pygame.draw.rect(screen, color, [(center_x - 3), (center_y - 3), 2, 2])	
			
	
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

		## Keyboard input interpretation ---v
	
	for event in pygame.event.get():   # NOTE: This does not seem to allow for continuously-held-down keys being re-read if another key is pressed and released during the first key's held period.
		if event.type == pygame.QUIT:
			sys.exit
			
		if event.type == pygame.KEYDOWN:	
			
			## Turn the ship...
			
			## counter clockwise:
			if ((event.key == pygame.K_LEFT) or (event.key == pygame.K_a)):
				if player_ship_objects_array[0].angular_velocity > -12:
					player_ship_objects_array[0].angular_velocity += -1
					
			## clockwise:				
			elif ((event.key == pygame.K_RIGHT) or (event.key == pygame.K_d)):
				if player_ship_objects_array[0].angular_velocity < 12:
					player_ship_objects_array[0].angular_velocity += 1
		
		
			## Move the ship...
			
			## forwards:
			elif ((event.key == pygame.K_w) or (event.key == pygame.K_UP)):

				player_ship_objects_array[0].adjust_all_velocities(0, -1, 0)
			
			## leftwards:
			elif (event.key == pygame.K_q): 

				player_ship_objects_array[0].adjust_all_velocities(-1, 0, 0)
			
			## rightwards:
			elif (event.key == pygame.K_e): 
			
				player_ship_objects_array[0].adjust_all_velocities(1, 0, 0)
		
		
			## Brake the ship:
			elif ((event.key == pygame.K_s) or (event.key == pygame.K_DOWN)):

				player_ship_objects_array[0].brake_all_velocities()


			## Fire a shot object:
			elif ((event.key == pygame.K_SPACE) or (event.key == pygame.K_f)):
				for each in player_ship_objects_array:
					each.firin_mah_lazor()
						

	
	
	
	




	
#### Inits ####


## Create a clock object to make the game run at a specified speed in the main loop
clock = pygame.time.Clock()

## To keep the game running
keep_window_open = True

## Window title			
pygame.display.set_caption(WINDOW_CAPTION)		
		
		
## Init the GameObject arrays		
asteroid_objects_array = []		
shot_objects_array = []		
alien_objects_array = []
player_ship_objects_array = []		
			
#def __init__(self, starting_x, starting_y, x_velocity, y_velocity, max_velocity, angular_velocity, current_angle_in_degrees=0, size=1, color=WHITE, programmatic_object_shape=1, is_asteroid=False, is_owned_by_player=False, is_shot_object=False, is_alien_ship=False):
				
			
## Test asteroids
third_new_asteroid_object = GameObject(0, 0, 1, 1, 1, 1, is_asteroid=True, size=100)
asteroid_objects_array.append(third_new_asteroid_object)

second_new_asteroid_object = GameObject(0, 0, 2, 2, 2, 2, is_asteroid=True, color=GREEN, size=50)
asteroid_objects_array.append(second_new_asteroid_object)

new_asteroid_object = GameObject(0, 0, 4, 4, 4, 4, is_asteroid=True, color=RED, size=25)
asteroid_objects_array.append(new_asteroid_object)

fourth_new_asteroid_object = GameObject(0, 0, 8, 8, 8, 8, is_asteroid=True, color=BLUE, size=12)
asteroid_objects_array.append(fourth_new_asteroid_object)



## Player ship
new_player_ship_size = NPS_size = 30
new_player_ship_starting_coords = NPS_starting_coords_upperleft_x, NPS_starting_coords_upperleft_y = ((SCREEN_WIDTH // 2) - (NPS_size / 2)), ((SCREEN_HEIGHT // 2) - (NPS_size / 2))

new_player_ship_object = Ship(NPS_starting_coords_upperleft_x, NPS_starting_coords_upperleft_y, 0, 0, 10, 0, is_owned_by_player=True, programmatic_object_shape=0, color=WHITE, size=NPS_size)
player_ship_objects_array.append(new_player_ship_object)

## Init the game ticker -- it's used for making things happen at set intervals of each other in the main loop, independent of the game ticker (perhaps this should be factored out in favor of a 100% clock-based system)
game_ticker = 0

	
pygame.key.set_repeat(20, 20)	 #  <--- ==  when_a_key_is_held_down_it_will_repeat_its_KEYDOWN_signal_with(repeat_delay_in_milliseconds, repeat_interval_in_milliseconds)
	
	
#### Main Loop ####

while keep_window_open == True:
										
	
	## Input handler variables
	button1_pressed, button2_pressed, button3_pressed = pygame.mouse.get_pressed()
	mouse_position = mouse_x, mouse_y = pygame.mouse.get_pos()
	

	## Process keyboard input
	handle_keys()
	
	
	## Game speed and event progression metering
	clock.tick(30)
	game_ticker += 1
				
	if game_ticker == 20:
		## I don't know if this is helpful or not. That's probably a bad thing, but I want to worry about problems other than number size limitations right now! I'll learn it later and remember it forever after that point.
		game_ticker = 0
		
	
	## Move all GameObjects and adjust their angles
	if game_ticker >= 0:
	
		for each_asteroid_object in asteroid_objects_array:
			each_asteroid_object.move()
			each_asteroid_object.adjust_current_angle(each_asteroid_object.angular_velocity)
			
			
		for each_player_ship_object in player_ship_objects_array:	
			each_player_ship_object.move()
			each_player_ship_object.adjust_current_angle(each_player_ship_object.angular_velocity)
		
		
		for each_shot_object in shot_objects_array:
			each_shot_object.move()
			each_shot_object.adjust_current_angle(each_shot_object.angular_velocity)
		
	
	## This part's debug code ---v	
	if ((game_ticker % 4) == 1):	
		print("\nasteroid_objects_array[0].x_velocity == " + str(asteroid_objects_array[0].x_velocity))
		print("asteroid_objects_array[0].y_velocity == " + str(asteroid_objects_array[0].y_velocity))
		print("asteroid_objects_array[0].w == " + str(asteroid_objects_array[0].w))
		print("asteroid_objects_array[0].h == " + str(asteroid_objects_array[0].h))
		print("asteroid_objects_array[0].x == " + str(asteroid_objects_array[0].x))
		print("asteroid_objects_array[0].x2 == " + str(asteroid_objects_array[0].x2))
		print("asteroid_objects_array[0].y == " + str(asteroid_objects_array[0].y))
		print("asteroid_objects_array[0].y2 == " + str(asteroid_objects_array[0].y2)) 
		
		print("\nplayer_ship_objects_array[0].x_velocity == " + str(player_ship_objects_array[0].x_velocity))
		print("player_ship_objects_array[0].y_velocity == " + str(player_ship_objects_array[0].y_velocity))
		print("hypotenuse_of_velocities == " + (str(math.sqrt((player_ship_objects_array[0].x_velocity * player_ship_objects_array[0].x_velocity) + (player_ship_objects_array[0].y_velocity * player_ship_objects_array[0].y_velocity)))))
		print("player_ship_objects_array[0].current_angle_in_degrees == " + str(player_ship_objects_array[0].current_angle_in_degrees))
		print("player_ship_objects_array[0].w == " + str(player_ship_objects_array[0].w))
		print("player_ship_objects_array[0].h == " + str(player_ship_objects_array[0].h))
		print("player_ship_objects_array[0].x == " + str(player_ship_objects_array[0].x))
		print("player_ship_objects_array[0].x2 == " + str(player_ship_objects_array[0].x2))
		print("player_ship_objects_array[0].y == " + str(player_ship_objects_array[0].y))
		print("player_ship_objects_array[0].y2 == " + str(player_ship_objects_array[0].y2))		
		print("player_ship_objects_array[0].center_x == " + str(player_ship_objects_array[0].center_x))
		print("player_ship_objects_array[0].center_y == " + str(player_ship_objects_array[0].center_y))			

	
	## Note: I think we need to display things AFTER moving them.
	render_all()						
						
	


# "Be IDLE friendly," they said.	
pygame.quit	
		
	
	
	
	
	
	
	
	
	
	

	