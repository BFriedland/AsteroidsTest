import pygame
import sys
import math
from math import *



#### Constants ####

WINDOW_CAPTION = 'Ball Shooter Test version 4.0'

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 400, 300

BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]

PI = 3.141592653

ball_speed = 6


ball_image = pygame.image.load("small_ball.gif")


screen = pygame.display.set_mode(SCREEN_SIZE)


#### Classes ####

class GameObject:
	def __init__(self, x_velocity, y_velocity, angle=0, asteroid_scale=None, asteroid_shape=1, color=None, supplied_image=None, size=None):

		self.x_velocity = x_velocity
		self.y_velocity = y_velocity
		
		self.color = color
		
		self.asteroid_shape = asteroid_shape
		self.asteroid_scale = asteroid_scale
		
		self.size = size
		
		self.supplied_image = supplied_image
		
		if self.supplied_image != None:
		
			self.rectangle = self.supplied_image.get_rect()

			self.w = self.rectangle[2]
			self.h = self.rectangle[3]
		
		elif self.asteroid_scale != None:
			self.asteroid_scaling_coefficient = (1 / (2 ** self.asteroid_scale))
			self.w = self.size * self.asteroid_scaling_coefficient
			self.h = self.size * self.asteroid_scaling_coefficient
			
			if self.color != None:
				self.color = color
			else:
				self.color = WHITE
			
		else:
			print("ERROR ERROR ERROR")
			
		self.x = 0
		self.y = 0
		
		self.x2 = self.w
		self.y2 = self.h
		
		self.angle = angle
	
	def draw(self):
	
		if self.supplied_image != None:	
			screen.blit(self.supplied_image, self.rectangle)
		
		
		if self.asteroid_scale != None:
			draw_programmatic_object(self.x, self.y, self.w, self.h, self.x2, self.y2, self.angle, self.asteroid_scaling_coefficient, self.asteroid_shape, self.color, self.size)
			#if self.asteroid_scale == 0:
			#	print("draw_programmatic_object sent: x="+str(self.x)+", y="+str(self.y)+", w="+str(self.w)+", h="+str(self.h)+", x2="+str(self.x2)+", y2="+str(self.y2)+", a_s_c="+str(self.asteroid_scaling_coefficient)+", a_s="+str(self.asteroid_shape)+", color="+str(self.color)+", size="+str(self.size))
			

	def move(self):
		
		
		self.x += self.x_velocity
		self.y += self.y_velocity
		self.x2 += self.x_velocity
		self.y2 += self.y_velocity
		
		
		if self.supplied_image != None:
			self.rectangle = self.rectangle.move(self.x_velocity, self.y_velocity)
		
			if (self.rectangle.left < 0):
				self.x_velocity = (abs(self.x_velocity) * 1)
			if (self.rectangle.right > SCREEN_WIDTH):
				self.x_velocity = (abs(self.x_velocity) * -1)
				
			if (self.rectangle.top < 0):
				self.y_velocity = (abs(self.y_velocity) * 1)
			if (self.rectangle.bottom > SCREEN_HEIGHT):
				self.y_velocity = (abs(self.y_velocity) * -1)
			
		elif self.asteroid_scale != None:
			# Already handled in the x-y modificatons above
			if (self.x < 0):
				self.x_velocity = (abs(self.x_velocity) * 1)
			if (self.x2 > SCREEN_WIDTH):
				self.x_velocity = (abs(self.x_velocity) * -1)
				
			if (self.y < 0):
				self.y_velocity = (abs(self.y_velocity) * 1)
			if (self.y2 > SCREEN_HEIGHT):
				self.y_velocity = (abs(self.y_velocity) * -1)
		
		
		
		
#### Functions ####


def render_all():

	# Note to self: v-- This here's the 'erase' equivalent, for now.	
	screen.fill(BLACK)
	
	
	if len(ball_objects_array) > 0:
		for each_ball_object in range(0, len(ball_objects_array)):
			ball_objects_array[each_ball_object].draw()
	
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
			
			
	#pygame.display.flip()
	

	
	
def draw_programmatic_object(x, y, w, h, x2, y2, angle=0, supplied_asteroid_scaling_coefficient=None, asteroid_shape=1, color=WHITE, size=0):

	
	
	# This is bad. FIX IT. --------------v  ... um, apparently it's not bad, it's just unintended. Graph paper made me do it!
	asteroid_scaling_coefficient = (size / 20) * supplied_asteroid_scaling_coefficient
	
	
	object_upper_left_x = x
	object_upper_left_y = y
	object_center_x = (x + (w / 2))
	object_center_y = (y + (h / 2))
	
	# note: turn into variable
	#asteroid_shape = 1 
	
	if asteroid_scaling_coefficient != None:
		## Then it's an asteroid and will look like an asteroid:
		
		if asteroid_shape == 1:
		
		
			#### v-- DEBUG --v ####
			pygame.draw.rect(screen, RED, [(object_center_x - 3), (object_center_y - 3), 2, 2])	
			#### ^-- DEBUG --^ ####
			
		
			# Line 0
			line_0_start_x, line_0_start_y = rotate_point_x_y_around_center_x_y_by_angle((object_center_x + ( 4 * asteroid_scaling_coefficient)), (object_center_y - (10 * asteroid_scaling_coefficient)), object_center_x, object_center_y, angle)
			line_0_end_x, line_0_end_y = rotate_point_x_y_around_center_x_y_by_angle((object_center_x + (10 * asteroid_scaling_coefficient)), (object_center_y - ( 3 * asteroid_scaling_coefficient)), object_center_x, object_center_y, angle)
			print("line_0_start_x = "+str(line_0_start_x)+", line_0_start_y = "+str(line_0_start_y)+", line_0_end_x = "+str(line_0_end_x)+", line_0_end_y = " + str(line_0_end_y))
			
			
			####~~~~ Intended --v
			pygame.draw.line(screen, color, [line_0_start_x, line_0_start_y], [line_0_end_x, line_0_end_y], 15)
			
			#### DEBUG --vvvv
			#pygame.draw.line(screen, color, [(object_center_x + ( 4 * asteroid_scaling_coefficient)), (object_center_y - (10 * asteroid_scaling_coefficient))], [(object_center_x + (10 * asteroid_scaling_coefficient)), (object_center_y - ( 3 * asteroid_scaling_coefficient))], 1)
			#### DEBUG --^^^^
			
			
			#pygame.draw.line(screen, color, [(object_center_x + ( 4 * asteroid_scaling_coefficient)), (object_center_y - (10 * asteroid_scaling_coefficient))], [(object_center_x + (10 * asteroid_scaling_coefficient)), (object_center_y - ( 3 * asteroid_scaling_coefficient))], 1)
			
			
			
			
			## Line 1
			
			#### Note: These look complex, but they're actually very easy.
			#### It's a line with [(start_x, start_y), (end_x, end_y)]
			#### Just need to transfer all these start-end points into the rotate_point...(x, y, centerx, centery, angle) function. 11 lines and the first one is done already --^
			
			
			line_1_start_x, line_1_start_y = rotate_point_x_y_around_center_x_y_by_angle((object_center_x + (10 * asteroid_scaling_coefficient)), (object_center_y - ( 3 * asteroid_scaling_coefficient)), object_center_x, object_center_y, angle)
			line_1_end_x, line_1_end_y = rotate_point_x_y_around_center_x_y_by_angle((object_center_x + (10 * asteroid_scaling_coefficient)), (object_center_y - ( 0 * asteroid_scaling_coefficient)), object_center_x, object_center_y, angle)
			
			####~~~~ Intended --v
			#pygame.draw.line(screen, color, [line_1_start_x, line_1_start_y], [line_1_end_x, line_1_end_y], 1)
			
			#### DEBUGGGG 
			#pygame.draw.line(screen, color, [(object_center_x + (10 * asteroid_scaling_coefficient)), (object_center_y - ( 3 * asteroid_scaling_coefficient))], [(object_center_x + (10 * asteroid_scaling_coefficient)), (object_center_y - ( 0 * asteroid_scaling_coefficient))], 1)
			#### DEBOOOOG
			
			
			#pygame.draw.line(screen, color, [(object_center_x + (10 * asteroid_scaling_coefficient)), (object_center_y - ( 3 * asteroid_scaling_coefficient))], [(object_center_x + (10 * asteroid_scaling_coefficient)), (object_center_y - ( 0 * asteroid_scaling_coefficient))], 1)
			
			
			## Line 2
			
			line_2_start_x, line_2_start_y = rotate_point_x_y_around_center_x_y_by_angle((object_center_x + (10 * asteroid_scaling_coefficient)), (object_center_y - ( 0 * asteroid_scaling_coefficient)), object_center_x, object_center_y, angle)
			line_2_end_x, line_2_end_y = rotate_point_x_y_around_center_x_y_by_angle((object_center_x + ( 3 * asteroid_scaling_coefficient)), (object_center_y + (10 * asteroid_scaling_coefficient)), object_center_x, object_center_y, angle)
			
			####~~~~ Intended --v
			#pygame.draw.line(screen, color, [line_2_start_x, line_2_start_y], [line_2_end_x, line_2_end_y], 1)
			
			#pygame.draw.line(screen, color, [(object_center_x + (10 * asteroid_scaling_coefficient)), (object_center_y - ( 0 * asteroid_scaling_coefficient))], [(object_center_x + ( 3 * asteroid_scaling_coefficient)), (object_center_y + (10 * asteroid_scaling_coefficient))], 1)
			
			
			## Line 3
			
			####~~~~line_3_start_x, line_3_start_y = rotate_point_x_y_around_center_x_y_by_angle(, object_center_x, object_center_y, angle)
			####~~~~line_3_end_x, line_3_end_y = rotate_point_x_y_around_center_x_y_by_angle(, object_center_x, object_center_y, angle)
			
			#pygame.draw.line(screen, color, [(object_center_x + ( 3 * asteroid_scaling_coefficient)), (object_center_y + (10 * asteroid_scaling_coefficient))], [(object_center_x - ( 2 * asteroid_scaling_coefficient)), (object_center_y + (10 * asteroid_scaling_coefficient))], 1)
			
			
			## Line 4
			
			####~~~~line_4_start_x, line_4_start_y = rotate_point_x_y_around_center_x_y_by_angle(, object_center_x, object_center_y, angle)
			####~~~~line_4_end_x, line_4_end_y = rotate_point_x_y_around_center_x_y_by_angle(, object_center_x, object_center_y, angle)
			
			#pygame.draw.line(screen, color, [(object_center_x - ( 2 * asteroid_scaling_coefficient)), (object_center_y + (10 * asteroid_scaling_coefficient))], [(object_center_x - ( 1 * asteroid_scaling_coefficient)), (object_center_y - ( 0 * asteroid_scaling_coefficient))], 1)
			
			
			## Line 5
			
			####~~~~line_5_start_x, line_5_start_y = rotate_point_x_y_around_center_x_y_by_angle(, object_center_x, object_center_y, angle)
			####~~~~line_5_end_x, line_5_end_y = rotate_point_x_y_around_center_x_y_by_angle(, object_center_x, object_center_y, angle)
			
			#pygame.draw.line(screen, color, [(object_center_x - ( 1 * asteroid_scaling_coefficient)), (object_center_y - ( 0 * asteroid_scaling_coefficient))], [(object_center_x - ( 5 * asteroid_scaling_coefficient)), (object_center_y + (10 * asteroid_scaling_coefficient))], 1)
			
			
			## Line 6
			
			####~~~~line_6_start_x, line_6_start_y = rotate_point_x_y_around_center_x_y_by_angle(, object_center_x, object_center_y, angle)
			####~~~~line_6_end_x, line_6_end_y = rotate_point_x_y_around_center_x_y_by_angle(, object_center_x, object_center_y, angle)
			
			#pygame.draw.line(screen, color, [(object_center_x - ( 5 * asteroid_scaling_coefficient)), (object_center_y + (10 * asteroid_scaling_coefficient))], [(object_center_x - (10 * asteroid_scaling_coefficient)), (object_center_y + ( 1 * asteroid_scaling_coefficient))], 1)
			
			
			## Line 7
			
			####~~~~line_7_start_x, line_7_start_y = rotate_point_x_y_around_center_x_y_by_angle(, object_center_x, object_center_y, angle)
			####~~~~line_7_end_x, line_7_end_y = rotate_point_x_y_around_center_x_y_by_angle(, object_center_x, object_center_y, angle)
			
			#pygame.draw.line(screen, color, [(object_center_x - (10 * asteroid_scaling_coefficient)), (object_center_y + ( 1 * asteroid_scaling_coefficient))], [(object_center_x - ( 5 * asteroid_scaling_coefficient)), (object_center_y - ( 1 * asteroid_scaling_coefficient))], 1)
			
			
			## Line 8
			
			####~~~~line_8_start_x, line_8_start_y = rotate_point_x_y_around_center_x_y_by_angle(, object_center_x, object_center_y, angle)
			####~~~~line_8_end_x, line_8_end_y = rotate_point_x_y_around_center_x_y_by_angle(, object_center_x, object_center_y, angle)
			
			#pygame.draw.line(screen, color, [(object_center_x - ( 5 * asteroid_scaling_coefficient)), (object_center_y - ( 1 * asteroid_scaling_coefficient))], [(object_center_x - (10 * asteroid_scaling_coefficient)), (object_center_y - ( 2 * asteroid_scaling_coefficient))], 1)
			
			
			## Line 9
			
			####~~~~line_9_start_x, line_9_start_y = rotate_point_x_y_around_center_x_y_by_angle(, object_center_x, object_center_y, angle)
			####~~~~line_9_end_x, line_9_end_y = rotate_point_x_y_around_center_x_y_by_angle(, object_center_x, object_center_y, angle)
			
			#pygame.draw.line(screen, color, [(object_center_x - (10 * asteroid_scaling_coefficient)), (object_center_y - ( 2 * asteroid_scaling_coefficient))], [(object_center_x - ( 3 * asteroid_scaling_coefficient)), (object_center_y - (10 * asteroid_scaling_coefficient))], 1)
			
			
			## Line 10
			
			####~~~~line_10_start_x, line_10_start_y = rotate_point_x_y_around_center_x_y_by_angle(, object_center_x, object_center_y, angle)
			####~~~~line_10_end_x, line_10_end_y = rotate_point_x_y_around_center_x_y_by_angle(, object_center_x, object_center_y, angle)
			
			#pygame.draw.line(screen, color, [(object_center_x - ( 3 * asteroid_scaling_coefficient)), (object_center_y - (10 * asteroid_scaling_coefficient))], [(object_center_x + ( 4 * asteroid_scaling_coefficient)), (object_center_y - (10 * asteroid_scaling_coefficient))], 1)
			
	
			pygame.display.flip()
	
			
			
			
			#if asteroid_scaling_coefficient == 1:
				
			#pygame.draw.line(screen, color, [x, y], [x2, y2], 1) # | pygame.draw.line(surface object, color, [start of line x, y], [end of line x, y], line thickness in pixels)
		
		##	rotated_lines_array = [[[[][]][[][]]][[[][]][[][]]][[[][]][[][]]][[[][]][[][]]][[[][]][[][]]][[[][]][[][]]][[[][]][[][]]][[[][]][[][]]][[[][]][[][]]][[[][]][[][]]][[[][]][[][]]]]
		
		## v--- the code to render a full programmatic object from an array of the above kind --^
		
		#for each_line in this_objects_lines_array:
		#	pygame.draw.line(screen, color, [each_line[0][0], each_line[0][1]], [each_line[1][0], each_line[1][1]], 1)
	
	
	## v-- Rotate the object's lines around the center point
	#rotated_points_array = rotate_these_points_around_that_point_with_this_angle(array_of_points_to_be_rotated, object_center_x, object_center_y, angle)
	
	
	## This --v draws a box on the screen
	#pygame.draw.rect(screen, color, [x, y, w, h])
	## and this --v puts a 6x6 black dot in the center of that --^ box
	#pygame.draw.rect(screen, BLACK, [(object_center_x - 3), (object_center_y - 3), 6, 6])	

	
def rotate_point_x_y_around_center_x_y_by_angle(point_x, point_y, center_x, center_y, angle):
	
	x_length = point_x - center_x
	y_length = point_y - center_y
	
	print("x_length <"+str(x_length)+"> = point_x <"+str(point_x)+"> - center_x <"+str(center_x)+">")
	
	hypotenuse_length = math.sqrt((y_length * y_length) + (x_length * x_length))
	print("hypotenuse_length = " +str(hypotenuse_length))

	cosine_of_line = hypotenuse_length * math.cos(angle)
	sine_of_line = hypotenuse_length * math.sin(angle)
	
	print("cosine_of_line = "+str(cosine_of_line)+", sine_of_line = "+str(sine_of_line))
	
	'''
	cosine_of_line = 1 * math.cos(angle) + hypotenuse_length
	sine_of_line = 1 * math.sin(angle) + hypotenuse_length
	'''
	
	new_point_x = cosine_of_line  + center_x
	new_point_y = sine_of_line  + center_y
	
	
	return new_point_x, new_point_y
	
	
	
	
	# Nice idea but too complicated to easily implement. --v
	
	'''
	new_object_lines_array = []
	
	for each_line in supplied_object_lines_array:
		new_line = []
		for each_endpoint_pair in each_line:
			new_endpoint_pair = []
			
			center_x, center_y = centerpoint
			each_endpoint_pair[0] = point_x
			each_endpoint_pair[1] = point_y
			
			point_y = center_y - point_y
			point_x = center_x - point_x
			
			hypotenuse = math.sqrt((point_y ** point_y) + (point_x ** point_x))
			
			sine_of_line = hypotenuse*math.sin(angle)
			cosine_of_line = hypotenuse*math.cos(angle)
			
			new_point_y = sine_of_line
			new_point_x = cosine_of_line
			
			new_endpoint_pair = [new_point_x, new_point_y]
			new_line.append(new_endpoint_pair)
			
		new_object_lines_array.append(new_line)
		
	return new_object_lines_array		
	
	'''
			
			
'''			
 # Calculate the x,y for the end point of our 'sweep' based on
# the current angle
x=125*math.sin(angle)+145
y=125*math.cos(angle)+145
# Draw the line from the center at 145, 145 to the calculated
# end spot
pygame.draw.line(screen,green,[145,145],[x,y],2)
# Increase the angle by 0.05 radians
angle =angle + .05
# If we have done a full sweep, reset the angle to 0
pi=3.141592653
if angle > 2*pi:
angle = angle - 2*pi
'''	
	
	
	

	
#### Inits ####


clock = pygame.time.Clock()

keep_window_open = True
			
pygame.display.set_caption(WINDOW_CAPTION)		
		
		
		
ball_objects_array = []		
shot_objects_array = []		
alien_objects_array = []
player_objects_array = []		
		

third_new_ball_object = GameObject(1, 1, asteroid_scale=0, size=100) # supplied_image=ball_image)
ball_objects_array.append(third_new_ball_object)

second_new_ball_object = GameObject(2, 2, asteroid_scale=1, color=GREEN, size=100) # supplied_image=ball_image)
ball_objects_array.append(second_new_ball_object)

new_ball_object = GameObject(4, 4, asteroid_scale=2, color=RED, size=100) # supplied_image=ball_image)
ball_objects_array.append(new_ball_object)

fourth_new_ball_object = GameObject(8, 8, asteroid_scale=3, color=BLUE, size=100)
ball_objects_array.append(fourth_new_ball_object)

game_ticker = 0

	
#### Main Loop ####

while keep_window_open == True:
		
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit
			
	
	button1_pressed, button2_pressed, button3_pressed = pygame.mouse.get_pressed()
	
	mouse_position = mouse_x, mouse_y = pygame.mouse.get_pos()

	clock.tick(30)
	
	game_ticker += 1
	
	#if ((game_ticker % 2) == 1):
	if game_ticker >= 0:
		for each_ball_object in ball_objects_array:
		
			each_ball_object.move()
			
			each_ball_object.angle += 0.05
			if (each_ball_object.angle > (2 * PI)):
				each_ball_object.angle = (each_ball_object.angle - (2 * PI))
		
	if ((game_ticker % 4) == 1):	
		print("\nball_objects_array[0].x_velocity == " + str(ball_objects_array[0].x_velocity))
		print("ball_objects_array[0].y_velocity == " + str(ball_objects_array[0].y_velocity))
		print("ball_objects_array[0].w == " + str(ball_objects_array[0].w))
		print("ball_objects_array[0].h == " + str(ball_objects_array[0].h))
		print("ball_objects_array[0].x == " + str(ball_objects_array[0].x))
		print("ball_objects_array[0].x2 == " + str(ball_objects_array[0].x2))
		print("ball_objects_array[0].y == " + str(ball_objects_array[0].y))
		print("ball_objects_array[0].y2 == " + str(ball_objects_array[0].y2)) 
		#print("ball_objects_array[0].rectangle == " + str(ball_objects_array[0].rectangle)) # get_rect() DOES NOT WORK if no supplied_image
		
		print("\nball_objects_array[1].x_velocity == " + str(ball_objects_array[1].x_velocity))
		print("ball_objects_array[1].y_velocity == " + str(ball_objects_array[1].y_velocity))
		print("ball_objects_array[1].w == " + str(ball_objects_array[1].w))
		print("ball_objects_array[1].h == " + str(ball_objects_array[1].h))
		print("ball_objects_array[1].x == " + str(ball_objects_array[1].x))
		print("ball_objects_array[1].x2 == " + str(ball_objects_array[1].x2))
		print("ball_objects_array[1].y == " + str(ball_objects_array[1].y))
		print("ball_objects_array[1].y2 == " + str(ball_objects_array[1].y2))		
		#print("ball_objects_array[1].rectangle == " + str(ball_objects_array[1].rectangle)) # get_rect() DOES NOT WORK if no supplied_image
		
			
	if game_ticker == 20:
		game_ticker = 0
	
	render_all()
	
	
pygame.quit	
	