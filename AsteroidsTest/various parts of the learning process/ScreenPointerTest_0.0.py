import pygame
import sys
from math import *

size = width, height = 400, 300
black = 0, 0, 0

screen_center = center_width, center_height = (width // 2), (height // 2)
upper_left_corner = upper_left_x, upper_left_y = 0, 0


screen = pygame.display.set_mode(size)



def report_x_y_on_click():

	new_mouse_x, new_mouse_y = (mouse_position[0] - screen_center[0]), (mouse_position[1] - screen_center[1])
	
	if new_mouse_x == 0:
		new_mouse_x = 0.01
	if new_mouse_y == 0:
		new_mouse_y = 0.01
	
	hypotenuse = sqrt((new_mouse_x * new_mouse_x) + (new_mouse_y * new_mouse_y))
	a = new_mouse_y
	b = new_mouse_x
	c = hypotenuse
	
	sine = a / c
	cosine = b / c
	tangent = a / b
	
	y_vector = sine
	x_vector = cosine

	####
	
	
	
	####
	
	print("\nx == " + str(new_mouse_x))
	print("y == " + str(new_mouse_y))
	print("x-vector == " + str(x_vector))
	print("y-vector == " + str(y_vector))
	
	
game_ticker = 0	
	
while 1:

	mouse_position = mouse_x, mouse_y = pygame.mouse.get_pos()

	button1_pressed, button2_pressed, button3_pressed = pygame.mouse.get_pressed()
	

	game_ticker += 1
	if game_ticker > 15400:
		game_ticker = 0
	
		
	if ((game_ticker % 15500) == 1):
		if button1_pressed == True:
			report_x_y_on_click()
		
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit
		