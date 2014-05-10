import pygame
import sys
import math
from math import *



#### Constants ####

WINDOW_CAPTION = 'Asteroids! Test version 1.4'

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]


ball_image = pygame.image.load("small_ball.gif")


screen = pygame.display.set_mode(SCREEN_SIZE)


#### Classes ####

class GameObject:
	def __init__(self, starting_x, starting_y, x_velocity, y_velocity, angular_velocity, angle_in_degrees, is_asteroid=False, is_owned_by_player=False, is_shot_object=False, programmatic_object_shape=1, color=None, supplied_image=None, size=1):
		''' GaneObjects are everything visible in the play field: Asteroids, shots, and both the player's and the aliens' ships. '''
		
		self.starting_x = starting_x
		self.starting_y = starting_y

		self.x_velocity = x_velocity
		self.y_velocity = y_velocity
		
		self.angular_velocity = angular_velocity
		
		self.angle_in_degrees = angle_in_degrees
		
		self.color = color
		
		self.programmatic_object_shape = programmatic_object_shape
		
		self.size = size
				

		self.is_asteroid = is_asteroid
		
		self.is_owned_by_player = is_owned_by_player
		
		self.is_shot_object = is_shot_object
		

		self.supplied_image = supplied_image
		
		
		if self.supplied_image != None:
		
			self.rectangle = self.supplied_image.get_rect()

			self.w = self.rectangle[2]
			self.h = self.rectangle[3]
		
			# THIS WOULD BE NICE for the legacy code! IMPORTANT: MUST FIX WHEN USED FOR COPYPASTA OF THIS CODE THAT USES SPRITES IN THE FUTURE.
			#self.rectangle.move(starting_x, starting_y, amidoingthisright_maybefixthis)
		
		elif self.supplied_image == None:
			
			#####   v--- This may deserve to be factored out.
			self.scaling_coefficient = self.size
			
			self.w = self.size #* self.scaling_coefficient
			self.h = self.size #* self.scaling_coefficient

		
			if self.color != None:
				self.color = color
			else:
				self.color = WHITE
		
		
		else:
			print("ERROR ERROR ERROR GameObject class has some kind of missing parameter?")
			
		self.x = 0
		self.y = 0
		
		
		self.x2 = self.w
		self.y2 = self.h
		
		
	def draw(self):
		''' Depending on supplied_image and is_asteroid, either blit the image or draw_programmatic_object() the object. '''
		if self.supplied_image != None:	
			screen.blit(self.supplied_image, self.rectangle)
		
		
		
		else:
			draw_programmatic_object(self.x, self.y, self.w, self.h, self.x2, self.y2, self.angle_in_degrees, self.scaling_coefficient, self.programmatic_object_shape, self.color, self.size)
		
		#else:
		#	print("ERROR another error-- this object is_NOTHING to its own draw() function.")

	def move(self, supplied_x_movement_amount=0, supplied_y_movement_amount=0):
		
		
		if ((supplied_x_movement_amount != 0) and (supplied_y_movement_amount != 0)):
			self.x += supplied_x_movement_amount
			self.y += supplied_y_movement_amount	
			
			self.x2 += supplied_x_movement_amount
			self.y2 += supplied_y_movement_amount
			
		## Since everything is programmatic objects, we're not using imagefoo.get_rect() --> imagefoo.rect.move() for Asteroids. 
		# v-- moves behind-the-scenes x,y/x2,y2 values. Does not directly move the thing on the screen. This part is for collisions.
		self.x += self.x_velocity
		self.y += self.y_velocity
		
		self.x2 += self.x_velocity
		self.y2 += self.y_velocity
		
		## This next part is for bouncing off the edges of the screen. When a map-base approach is implemented this will need modification.
		# v-- Legacy code, kept for bugproofing and ease of future expansion. Note self.rectangle... calls instead of self.x
		if self.supplied_image != None:
			self.rectangle = self.rectangle.move(self.x_velocity, self.y_velocity)
		
			if (self.rectangle.left < 0):
				self.x_velocity = (abs(self.x_velocity) * 1)
				self.angular_velocity *= -1
			if (self.rectangle.right > SCREEN_WIDTH):
				self.x_velocity = (abs(self.x_velocity) * -1)
				self.angular_velocity *= -1
				
			if (self.rectangle.top < 0):
				self.y_velocity = (abs(self.y_velocity) * 1)
				self.angular_velocity *= -1
			if (self.rectangle.bottom > SCREEN_HEIGHT):
				self.y_velocity = (abs(self.y_velocity) * -1)
				self.angular_velocity *= -1
			
		# v-- For asteroid movement.
		else:
			# Already handled in the x-y modificatons above
			if (self.x < 0):
				self.x_velocity = (abs(self.x_velocity) * 1)
				self.angular_velocity *= -1
			if (self.x2 > SCREEN_WIDTH):
				self.x_velocity = (abs(self.x_velocity) * -1)
				self.angular_velocity *= -1
				
			if (self.y < 0):
				self.y_velocity = (abs(self.y_velocity) * 1)
				self.angular_velocity *= -1
			if (self.y2 > SCREEN_HEIGHT):
				self.y_velocity = (abs(self.y_velocity) * -1)
				self.angular_velocity *= -1
			
		
		
			
	def adjust_current_angle(self, angle_adjustment):
		if self.angle_in_degrees != None:
			
			self.angle_in_degrees += angle_adjustment
					
			#each_ball_object.angle_in_degrees += (angle_incrementer / (2 * (each_ball_object.scaling_coefficient + 1)))
				
	
	def adjust_all_velocities(self, x_acceleration, y_acceleration, angular_acceleration, is_bringing_to_zero=False):
		
		
		### Ugh, I think the problem has something to do with the returns from the rotation call not being big enough or something??
		


		rotated_x_velocity_increment, rotated_y_velocity_increment = rotate_these_points_around_that_point(x_acceleration, y_acceleration, 0, 0, self.angle_in_degrees)      #   ship_center_x, ship_center_y, player_ship_objects_array[0].angle_in_degrees)
					
		if is_bringing_to_zero == False:			
			print("rotated_x_velocity_increment == "+str(rotated_x_velocity_increment))
			print("rotated_y_velocity_increment == "+str(rotated_y_velocity_increment))
		
			if ((self.x_velocity > 10) and (rotated_x_velocity_increment > 0)): 
				self.x_velocity -= 0
			elif ((self.x_velocity < -10) and (rotated_x_velocity_increment < 0)):
				self.x_velocity += 0
			
			else:
				self.x_velocity += rotated_x_velocity_increment
			
			
	
			if ((self.y_velocity > 10) and (rotated_y_velocity_increment > 0)): 
				self.y_velocity -= 0
			elif ((self.y_velocity < -10) and (rotated_y_velocity_increment < 0)):
				self.y_velocity += 0	
			else:
				self.y_velocity += rotated_y_velocity_increment
			
			
		
			if (((self.angular_velocity > 10) and (angular_acceleration > 0)) or ((self.angular_velocity < -10) and (angular_acceleration < 0))):
				self.angular_velocity += 0
			else:
				self.angular_velocity += angular_acceleration
				
		elif is_bringing_to_zero == True:
		
			## This took entirely too long to reason out. Basically, the if checks are to hand differently signed accelerations to their respective velocities with the proper sign (hence, += versus -= being significant).
			
			print("rotated_x_velocity_increment == "+str(rotated_x_velocity_increment))
			print("rotated_y_velocity_increment == "+str(rotated_y_velocity_increment))
		
			if (((self.x_velocity > 0) and (rotated_x_velocity_increment > 0)) or ((self.x_velocity < 0) and (rotated_x_velocity_increment < 0))):
				self.x_velocity -= rotated_x_velocity_increment
			else:
				self.x_velocity += rotated_x_velocity_increment
				
			
			if (((self.y_velocity > 0) and (rotated_y_velocity_increment > 0)) or ((self.y_velocity < 0) and (rotated_y_velocity_increment < 0))):
				self.y_velocity -= rotated_y_velocity_increment
			else:
				self.y_velocity += rotated_y_velocity_increment
				
			
			if (((self.angular_velocity > 0) and (angular_acceleration > 0)) or ((self.angular_velocity < 0) and (angular_acceleration < 0))):
				self.angular_velocity -= angular_acceleration
			else:
				self.angular_velocity += angular_acceleration	
		
	
class Ship(GameObject):
	
	#def __init__(is_owned_by_player):
	#	self.is_owned_by_player = is_owned_by_player
	
		#### NOTE: I may need to call __init__() here. It might have to directly reference the __init__() from GameObject in order to get all its stuff... maybe. Maybe not? I think not!
	
	
	def firin_mah_lazor(self):
	
		ship_center_x = (self.x + (self.w / 2))
		ship_center_y = (self.y + (self.h / 2))
		
		ship_front_tip_x = ship_center_x
		ship_front_tip_y = self.y
		
		# Where it's firing from:   ((the front point of the ship))
		rotated_ship_tip_x, rotated_ship_tip_y = rotate_these_points_around_that_point(ship_front_tip_x, ship_front_tip_y, ship_center_x, ship_center_y, self.angle_in_degrees)
		
		print("rotated_ship_tip_x == " + str(rotated_ship_tip_x))
		print("rotated_ship_tip_y == " + str(rotated_ship_tip_y))
		
		# The vector it's traveling in:
		shot_velocity_seed_x, shot_velocity_seed_y = rotate_these_points_around_that_point(0, -10, 0, 0, self.angle_in_degrees)

		
		
		shot_start_location_x = self.x + rotated_ship_tip_x
		shot_start_location_y = self.y + rotated_ship_tip_y
		
		
		## Make and append the shot object
		new_shot_object = Shot(shot_start_location_x, shot_start_location_y, shot_velocity_seed_x, shot_velocity_seed_y, 0, self.angle_in_degrees, is_owned_by_player=self.is_owned_by_player, is_shot_object=True, size=10)
		
		new_shot_object.move(supplied_x_movement_amount=ship_front_tip_x, supplied_y_movement_amount=ship_front_tip_y)
		
		shot_objects_array.append(new_shot_object)
		
		
		# for reference purposes -v
		#object_upper_left_x = x
		#object_upper_left_y = y
		#object_center_x = (x + (w / 2))
		#object_center_y = (y + (h / 2))
	
	

class Shot(GameObject):
	pass
	
	# MAEK HIT THANG
	
		
		
#### Functions ####


def render_all():

	# Note to self: v-- This here's the 'erase' equivalent, for now.	
	screen.fill(BLACK)
	
	
	if len(ball_objects_array) > 0:
		for each_ball_object in range(0, len(ball_objects_array)):
			ball_objects_array[each_ball_object].draw()
	
	if len(player_ship_objects_array) > 0:
		for each_player_ship_object in range(0, len(player_ship_objects_array)):
			player_ship_objects_array[each_player_ship_object].draw()

	if len(shot_objects_array) > 0:
		for each_shot_object in range(0, len(shot_objects_array)):
			shot_objects_array[each_shot_object].draw()
	
			
	## ASTEROIDS NOTE: The order of these if trees dictates which thing is displayed on top! May need to modify later.
	
	'''
	if len(ball_objects_array) > 0:
		for each_ball_object in range(0, len(ball_objects_array)):
			screen.blit(ball_objects_array[each_ball_object].supplied_image, ball_objects_array[each_ball_object].rectangle)
	
	if len(shot_objects_array) > 0:
		for each_shot_object in range(0, len(shot_objects_array)):
			screen.blit(shot_objects_array[each_shot_object].supplied_image, shot_objects_array[each_shot_object].rectangle)
		
	if len(alien_objects_array) > 0:
		for each_alien_object in range(0, len(alien_objects_array)):
			screen.blit(alien_objects_array[each_alien_object].supplied_image, alien_objects_array[each_alien_object].rectangle)
		
	if len(player_objects_array) > 0:
		for each_player_object in range(0, len(player_objects_array)):
			screen.blit(player_objects_array[each_player_object].supplied_image, player_objects_array[each_player_object].rectangle)
	'''
			
			
	pygame.display.flip()
	

	
	
def draw_programmatic_object(x, y, w, h, x2, y2, angle_in_degrees, scaling_coefficient=None, this_programmatic_object_shape=1, color=WHITE, size=100):

	
	# This is bad. FIX IT. --------------v  ... um, apparently it's not too bad, it's just unintended. The graph paper mentality made me do it! ... But it still needs to be fixed.
	if scaling_coefficient != None:
	
		scaling_coefficient = (size / 20)
		
	else:
		print("ERROR in draw_programmatic_object() ! Missing scaling coefficient")
	
	
	object_upper_left_x = x
	object_upper_left_y = y
	object_center_x = (x + (w / 2))
	object_center_y = (y + (h / 2))
	
	
	
	#programmatic_object_shape_1 == [ [11], [(object_center_x + (X_OFFSET * scaling_coefficient)), (object_center_y + (Y_OFFSET * scaling_coefficient))] ]

	if this_programmatic_object_shape == 0:
		supplied_programmatic_object_shape = [  3, [[   0, -10], [6, 10]], [[   0, -10], [-6,10]], [[-5.3,6.6], [5.3,6.6]] ]
	if this_programmatic_object_shape == 1:
		supplied_programmatic_object_shape = [ 11, [[   4, -10], [ 10,  -3]], [[ 10,  -3], [ 10,   0]], [[  10,   0], [  3,  10]], [[   3,  10], [ -2,  10]], [[  -2,  10], [ -1,   0]], [[  -1,   0], [ -5,  10]], [[  -5,  10], [-10,   1]], [[ -10,   1], [ -5,  -1]], [[  -5,  -1], [-10,  -2]], [[ -10,  -2], [ -3, -10]], [[  -3, -10], [  4, -10]], ]

	'''
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
	
	programmatic_object_shape == 2:
		[
			??,
			
			
		]
		
	
	
	'''
	
	
	
	
	
	# IMPORTANT: range(1, foo) is critical because 0th place is not a line!
	
	for each_line_ordinal in range(1, (supplied_programmatic_object_shape[0] + 1)):
		line_start_x, line_start_y   =   rotate_these_points_around_that_point((object_center_x + (supplied_programmatic_object_shape[each_line_ordinal][0][0] * scaling_coefficient)), (object_center_y + (supplied_programmatic_object_shape[each_line_ordinal][0][1] * scaling_coefficient)), object_center_x, object_center_y, angle_in_degrees)
		line_end_x, line_end_y       =   rotate_these_points_around_that_point((object_center_x + (supplied_programmatic_object_shape[each_line_ordinal][1][0] * scaling_coefficient)), (object_center_y + (supplied_programmatic_object_shape[each_line_ordinal][1][1] * scaling_coefficient)), object_center_x, object_center_y, angle_in_degrees)

		pygame.draw.line(screen, color, [line_start_x, line_start_y], [line_end_x, line_end_y], 1)			
		
		
		
		
'''		
	
	if (scaling_coefficient != None) and (programmatic_object_shape > 0):
		## Then it's an asteroid and will look like an asteroid:
		
		if programmatic_object_shape == 1:
			
			line_0_start_x, line_0_start_y = rotate_these_points_around_that_point((object_center_x + ( 4 * scaling_coefficient)), (object_center_y - (10 * scaling_coefficient)), object_center_x, object_center_y, angle_in_degrees)
			line_0_end_x, line_0_end_y = rotate_these_points_around_that_point((object_center_x + (10 * scaling_coefficient)), (object_center_y - ( 3 * scaling_coefficient)), object_center_x, object_center_y, angle_in_degrees)
			pygame.draw.line(screen, color, [line_0_start_x, line_0_start_y], [line_0_end_x, line_0_end_y], 1)			
			
			line_1_start_x, line_1_start_y = rotate_these_points_around_that_point((object_center_x + (10 * scaling_coefficient)), (object_center_y - ( 3 * scaling_coefficient)), object_center_x, object_center_y, angle_in_degrees)
			line_1_end_x, line_1_end_y = rotate_these_points_around_that_point((object_center_x + (10 * scaling_coefficient)), (object_center_y - ( 0 * scaling_coefficient)), object_center_x, object_center_y, angle_in_degrees)
			pygame.draw.line(screen, color, [line_1_start_x, line_1_start_y], [line_1_end_x, line_1_end_y], 1)
			
			line_2_start_x, line_2_start_y = rotate_these_points_around_that_point((object_center_x + (10 * scaling_coefficient)), (object_center_y - ( 0 * scaling_coefficient)), object_center_x, object_center_y, angle_in_degrees)
			line_2_end_x, line_2_end_y = rotate_these_points_around_that_point((object_center_x + ( 3 * scaling_coefficient)), (object_center_y + (10 * scaling_coefficient)), object_center_x, object_center_y, angle_in_degrees)
			pygame.draw.line(screen, color, [line_2_start_x, line_2_start_y], [line_2_end_x, line_2_end_y], 1)
			
			line_3_start_x, line_3_start_y = rotate_these_points_around_that_point((object_center_x + ( 3 * scaling_coefficient)), (object_center_y + (10 * scaling_coefficient)), object_center_x, object_center_y, angle_in_degrees)
			line_3_end_x, line_3_end_y = rotate_these_points_around_that_point((object_center_x - ( 2 * scaling_coefficient)), (object_center_y + (10 * scaling_coefficient)), object_center_x, object_center_y, angle_in_degrees)
			pygame.draw.line(screen, color, [line_3_start_x, line_3_start_y], [line_3_end_x, line_3_end_y], 1)
			
			line_4_start_x, line_4_start_y = rotate_these_points_around_that_point((object_center_x - ( 2 * scaling_coefficient)), (object_center_y + (10 * scaling_coefficient)), object_center_x, object_center_y, angle_in_degrees)
			line_4_end_x, line_4_end_y = rotate_these_points_around_that_point((object_center_x - ( 1 * scaling_coefficient)), (object_center_y - ( 0 * scaling_coefficient)), object_center_x, object_center_y, angle_in_degrees)
			pygame.draw.line(screen, color, [line_4_start_x, line_4_start_y], [line_4_end_x, line_4_end_y], 1)
			
			line_5_start_x, line_5_start_y = rotate_these_points_around_that_point((object_center_x - ( 1 * scaling_coefficient)), (object_center_y - ( 0 * scaling_coefficient)), object_center_x, object_center_y, angle_in_degrees)
			line_5_end_x, line_5_end_y = rotate_these_points_around_that_point((object_center_x - ( 5 * scaling_coefficient)), (object_center_y + (10 * scaling_coefficient)), object_center_x, object_center_y, angle_in_degrees)
			pygame.draw.line(screen, color, [line_5_start_x, line_5_start_y], [line_5_end_x, line_5_end_y], 1)
			
			line_6_start_x, line_6_start_y = rotate_these_points_around_that_point((object_center_x - ( 5 * scaling_coefficient)), (object_center_y + (10 * scaling_coefficient)), object_center_x, object_center_y, angle_in_degrees)
			line_6_end_x, line_6_end_y = rotate_these_points_around_that_point((object_center_x - (10 * scaling_coefficient)), (object_center_y + ( 1 * scaling_coefficient)), object_center_x, object_center_y, angle_in_degrees)
			pygame.draw.line(screen, color, [line_6_start_x, line_6_start_y], [line_6_end_x, line_6_end_y], 1)
			
			line_7_start_x, line_7_start_y = rotate_these_points_around_that_point((object_center_x - (10 * scaling_coefficient)), (object_center_y + ( 1 * scaling_coefficient)), object_center_x, object_center_y, angle_in_degrees)
			line_7_end_x, line_7_end_y = rotate_these_points_around_that_point((object_center_x - ( 5 * scaling_coefficient)), (object_center_y - ( 1 * scaling_coefficient)), object_center_x, object_center_y, angle_in_degrees)
			pygame.draw.line(screen, color, [line_7_start_x, line_7_start_y], [line_7_end_x, line_7_end_y], 1)
			
			line_8_start_x, line_8_start_y = rotate_these_points_around_that_point((object_center_x - ( 5 * scaling_coefficient)), (object_center_y - ( 1 * scaling_coefficient)), object_center_x, object_center_y, angle_in_degrees)
			line_8_end_x, line_8_end_y = rotate_these_points_around_that_point((object_center_x - (10 * scaling_coefficient)), (object_center_y - ( 2 * scaling_coefficient)), object_center_x, object_center_y, angle_in_degrees)
			pygame.draw.line(screen, color, [line_8_start_x, line_8_start_y], [line_8_end_x, line_8_end_y], 1)
			
			line_9_start_x, line_9_start_y = rotate_these_points_around_that_point((object_center_x - (10 * scaling_coefficient)), (object_center_y - ( 2 * scaling_coefficient)), object_center_x, object_center_y, angle_in_degrees)
			line_9_end_x, line_9_end_y = rotate_these_points_around_that_point((object_center_x - ( 3 * scaling_coefficient)), (object_center_y - (10 * scaling_coefficient)), object_center_x, object_center_y, angle_in_degrees)
			pygame.draw.line(screen, color, [line_9_start_x, line_9_start_y], [line_9_end_x, line_9_end_y], 1)

			line_10_start_x, line_10_start_y = rotate_these_points_around_that_point((object_center_x - ( 3 * scaling_coefficient)), (object_center_y - (10 * scaling_coefficient)), object_center_x, object_center_y, angle_in_degrees)
			line_10_end_x, line_10_end_y = rotate_these_points_around_that_point((object_center_x + ( 4 * scaling_coefficient)), (object_center_y - (10 * scaling_coefficient)), object_center_x, object_center_y, angle_in_degrees)
			pygame.draw.line(screen, color, [line_10_start_x, line_10_start_y], [line_10_end_x, line_10_end_y], 1)

			
			#if scaling_coefficient == 1:
				
			#pygame.draw.line(screen, color, [x, y], [x2, y2], 1) # | pygame.draw.line(surface object, color, [start of line x, y], [end of line x, y], line thickness in pixels)
'''		
	
	
	
	## v-- Rotates the object's lines around the center point
	#rotated_points_array = rotate_these_points_around_that_point(array_of_points_to_be_rotated, object_center_x, object_center_y)
	
	
	## This --v draws a box on the screen
	#pygame.draw.rect(screen, color, [x, y, w, h])
	## and this --v puts a 6x6 black dot in the center of that --^ box
	#pygame.draw.rect(screen, BLACK, [(object_center_x - 3), (object_center_y - 3), 6, 6])	

	
	
def rotate_these_points_around_that_point(point_x, point_y, center_x, center_y, angle_to_rotate_to_in_degrees):
	
	x_length = point_x - center_x
	y_length = point_y - center_y
		
	new_x = (x_length * math.cos(math.radians(angle_to_rotate_to_in_degrees))) - (y_length * math.sin(math.radians(angle_to_rotate_to_in_degrees)))
	new_y = (x_length * math.sin(math.radians(angle_to_rotate_to_in_degrees))) + (y_length * math.cos(math.radians(angle_to_rotate_to_in_degrees)))
	
	new_x += center_x
	new_y += center_y

	return new_x, new_y	
	
'''	
def handle_keys():

	player_action = 'none'

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			player_action = 'exit'
			
		if event.type == pygame.KEYDOWN:	
			
			if event.key == pygame.K_LEFT:
				if abs(player_ship_objects_array[0].angular_velocity) < 10:
					player_ship_objects_array[0].angular_velocity -= 1
					if (player_ship_objects_array[0].angular_velocity < 0):
						# This part is repetitive and must be removed.
						player_ship_objects_array[0].turning_clockwise = False
					
			elif event.key == pygame.K_RIGHT:
				if abs(player_ship_objects_array[0].angular_velocity) < 10:
					player_ship_objects_array[0].angular_velocity += 1
					if (player_ship_objects_array[0].angular_velocity > 0):
						# This part is repetitive and must be removed.
						player_ship_objects_array[0].turning_clockwise = True
						
						
	
	return player_action
'''				
				
'''	
 for event in pygame.event.get(): # User did something
if event.type == pygame.QUIT: # If user clicked close
done=True # Flag that we are done so we exit this loop
# User pressed down on a key
if event.type == pygame.KEYDOWN:
# Figure out if it was an arrow key. If so
# adjust speed.
if event.key == pygame.K_LEFT:
x_speed=-3
if event.key == pygame.K_RIGHT:
x_speed=3
if event.key == pygame.K_UP:
y_speed=-3
if event.key == pygame.K_DOWN:
y_speed=3
# User let up on a key
if event.type == pygame.KEYUP:
# If it is an arrow key, reset vector back to zero
if event.key == pygame.K_LEFT:
x_speed=0
if event.key == pygame.K_RIGHT:
x_speed=0
if event.key == pygame.K_UP:
y_speed=0
if event.key == pygame.K_DOWN:
y_speed=0	
'''

	
#### Inits ####


clock = pygame.time.Clock()

keep_window_open = True
			
pygame.display.set_caption(WINDOW_CAPTION)		
		
		
		
ball_objects_array = []		
shot_objects_array = []		
alien_objects_array = []
player_ship_objects_array = []		
		

third_new_ball_object = GameObject(0, 0, 1, 1, 1, 0, is_asteroid=True, size=100) # supplied_image=ball_image)
ball_objects_array.append(third_new_ball_object)

second_new_ball_object = GameObject(0, 0, 2, 2, 2, 0, is_asteroid=True, color=GREEN, size=50) # supplied_image=ball_image)
ball_objects_array.append(second_new_ball_object)

new_ball_object = GameObject(0, 0, 4, 4, 4, 0, is_asteroid=True, color=RED, size=25) # supplied_image=ball_image)
ball_objects_array.append(new_ball_object)

fourth_new_ball_object = GameObject(0, 0, 8, 8, 8, 0, is_asteroid=True, color=BLUE, size=12)
ball_objects_array.append(fourth_new_ball_object)






new_player_ship_size = NPS_size = 40
new_player_ship_starting_coords = NPS_starting_coords_upperleft_x, NPS_starting_coords_upperleft_y = ((SCREEN_WIDTH // 2) - (NPS_size / 2)), ((SCREEN_HEIGHT // 2) - (NPS_size / 2))

new_player_ship_object = Ship(NPS_starting_coords_upperleft_x, NPS_starting_coords_upperleft_y, 0, 0, 0, 0, is_owned_by_player=True, programmatic_object_shape=0, color=WHITE, size=NPS_size)
new_player_ship_object.move(supplied_x_movement_amount=new_player_ship_object.starting_x, supplied_y_movement_amount=new_player_ship_object.starting_y)
player_ship_objects_array.append(new_player_ship_object)




# This can probably be replaced by the pygame clock somehow. See main loop.
game_ticker = 0

	
player_action = 'none'	
	
	
pygame.key.set_repeat(20, 20)	 #  |  when_a_key_is_held_down_it_will_repeat_its_KEYDOWN_signal_with(repeat_delay_in_milliseconds, repeat_interval_in_milliseconds)
	
	
#### Main Loop ####

while keep_window_open == True:
		
	#for event in pygame.event.get():
	#	if event.type == pygame.QUIT:
	#		sys.exit
			
	
	button1_pressed, button2_pressed, button3_pressed = pygame.mouse.get_pressed()
	
	mouse_position = mouse_x, mouse_y = pygame.mouse.get_pos()

	clock.tick(30)
	
	
	#player_action = handle_keys()
	
	
	#if player_action == 'exit':
	#	keep_window_open = False
	#	break
	
	game_ticker += 1
	
	
	#if ((game_ticker % 2) == 1):
	if game_ticker >= 0:
		for each_ball_object in ball_objects_array:
			each_ball_object.move()
			
			if each_ball_object.angle_in_degrees != None:
			
				each_ball_object.adjust_current_angle(each_ball_object.angular_velocity)
			
		for each_player_ship_object in player_ship_objects_array:	
			each_player_ship_object.move()
		
			each_player_ship_object.adjust_current_angle(each_player_ship_object.angular_velocity)
		
		
		
		for each_shot_object in shot_objects_array:
		
			each_shot_object.move()
			
			each_shot_object.adjust_current_angle(each_shot_object.angular_velocity)
					
	if ((game_ticker % 4) == 1):	
		# This part's all debug code.
		print("\nball_objects_array[0].x_velocity == " + str(ball_objects_array[0].x_velocity))
		print("ball_objects_array[0].y_velocity == " + str(ball_objects_array[0].y_velocity))
		print("ball_objects_array[0].w == " + str(ball_objects_array[0].w))
		print("ball_objects_array[0].h == " + str(ball_objects_array[0].h))
		print("ball_objects_array[0].x == " + str(ball_objects_array[0].x))
		print("ball_objects_array[0].x2 == " + str(ball_objects_array[0].x2))
		print("ball_objects_array[0].y == " + str(ball_objects_array[0].y))
		print("ball_objects_array[0].y2 == " + str(ball_objects_array[0].y2)) 
		#print("ball_objects_array[0].rectangle == " + str(ball_objects_array[0].rectangle)) # get_rect() DOES NOT WORK if no supplied_image
		
		#print("\nball_objects_array[1].x_velocity == " + str(ball_objects_array[1].x_velocity))
		#print("ball_objects_array[1].y_velocity == " + str(ball_objects_array[1].y_velocity))
		#print("ball_objects_array[1].w == " + str(ball_objects_array[1].w))
		#print("ball_objects_array[1].h == " + str(ball_objects_array[1].h))
		#print("ball_objects_array[1].x == " + str(ball_objects_array[1].x))
		#print("ball_objects_array[1].x2 == " + str(ball_objects_array[1].x2))
		#print("ball_objects_array[1].y == " + str(ball_objects_array[1].y))
		#print("ball_objects_array[1].y2 == " + str(ball_objects_array[1].y2))		
		#print("ball_objects_array[1].rectangle == " + str(ball_objects_array[1].rectangle)) # get_rect() DOES NOT WORK if no supplied_image
		
		print("\nplayer_ship_objects_array[0].x_velocity == " + str(player_ship_objects_array[0].x_velocity))
		print("player_ship_objects_array[0].y_velocity == " + str(player_ship_objects_array[0].y_velocity))
		print("player_ship_objects_array[0].angle_in_degrees == " + str(player_ship_objects_array[0].angle_in_degrees))
		print("player_ship_objects_array[0].w == " + str(player_ship_objects_array[0].w))
		print("player_ship_objects_array[0].h == " + str(player_ship_objects_array[0].h))
		print("player_ship_objects_array[0].x == " + str(player_ship_objects_array[0].x))
		print("player_ship_objects_array[0].x2 == " + str(player_ship_objects_array[0].x2))
		print("player_ship_objects_array[0].y == " + str(player_ship_objects_array[0].y))
		print("player_ship_objects_array[0].y2 == " + str(player_ship_objects_array[0].y2))			
			
	if game_ticker == 20:
		# I don't know if this is helpful or not. That's probably a bad thing, but I want to worry about problems other than number size limitations right now! I'll learn it later and remember it forever after that point.
		game_ticker = 0
		
	
	render_all()
	
	
	## Keyboard Input ##
	
	for event in pygame.event.get():   # NOTE: This does not seem to allow for continuously-held-down keys being re-read if another key is pressed and released during the first key's held period.
		if event.type == pygame.QUIT:
			sys.exit
			player_action = 'exit'
			
		if event.type == pygame.KEYDOWN:	
			
			if ((event.key == pygame.K_LEFT) or (event.key == pygame.K_a)):
				if player_ship_objects_array[0].angular_velocity > -12:
					player_ship_objects_array[0].angular_velocity += -1
					#if (player_ship_objects_array[0].angular_velocity <= 0):
						# This part is repetitive and must be removed.
						#player_ship_objects_array[0].turning_clockwise = False
					
			elif ((event.key == pygame.K_RIGHT) or (event.key == pygame.K_d)):
				if player_ship_objects_array[0].angular_velocity < 12:
					player_ship_objects_array[0].angular_velocity += 1
					#if (player_ship_objects_array[0].angular_velocity >= 0):
						
						#player_ship_objects_array[0].turning_clockwise = True
			
				
			
			
			elif ((event.key == pygame.K_w) or (event.key == pygame.K_UP)):
	
				player_ship_objects_array[0].adjust_all_velocities(0, -1, 0)
		
			elif (event.key == pygame.K_q): 

				player_ship_objects_array[0].adjust_all_velocities(-1, 0, 0)
		
			elif (event.key == pygame.K_e): 

				player_ship_objects_array[0].adjust_all_velocities(1, 0, 0)
		
					
			elif ((event.key == pygame.K_s) or (event.key == pygame.K_DOWN)):

				## Slow all velocity to zero.
				
				## x_velocity:
				
				if (player_ship_objects_array[0].x_velocity >= 1):
					player_ship_objects_array[0].adjust_all_velocities(-0.4, 0.0001, 0, is_bringing_to_zero=True)
				
				elif (player_ship_objects_array[0].x_velocity <= -1):
					player_ship_objects_array[0].adjust_all_velocities(0.4, 0.0001, 0, is_bringing_to_zero=True)
		
				elif ((player_ship_objects_array[0].x_velocity < 1) and (player_ship_objects_array[0].x_velocity > -1)):	
					player_ship_objects_array[0].x_velocity = 0
				
				
				## y_velocity:
				
				if (player_ship_objects_array[0].y_velocity >= 1):
					player_ship_objects_array[0].adjust_all_velocities(0.0001, -0.4, 0, is_bringing_to_zero=True)
				
				elif (player_ship_objects_array[0].y_velocity <= -1):
					player_ship_objects_array[0].adjust_all_velocities(0.0001, 0.4, 0, is_bringing_to_zero=True)
		
				elif ((player_ship_objects_array[0].y_velocity < 1) and (player_ship_objects_array[0].y_velocity > -1)):	
					player_ship_objects_array[0].y_velocity = 0
						
				
				## angular_velocity:
				
				if (player_ship_objects_array[0].angular_velocity >= 1):
					player_ship_objects_array[0].adjust_all_velocities(0, 0, -1, is_bringing_to_zero=True)
				
				elif (player_ship_objects_array[0].angular_velocity <= -1):
					player_ship_objects_array[0].adjust_all_velocities(0, 0, 1, is_bringing_to_zero=True)
		
				elif ((player_ship_objects_array[0].angular_velocity < 1) and (player_ship_objects_array[0].angular_velocity > -1)):	
					player_ship_objects_array[0].angular_velocity = 0
			


			elif (event.key == pygame.K_SPACE):
				for each in player_ship_objects_array:
					each.firin_mah_lazor()
						
						
						
					
pygame.quit	
	