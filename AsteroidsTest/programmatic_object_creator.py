import pygame
import sys
import math
import random


print("\n\n#### INSTRUCTIONS FOR USE ####")

print("## This was made to facilitate development of my Asteroids! clone's programmatically-defined art assets.")
print("## You can use it by left clicking once inside the green square on the screen that pops up to start drawing a line, then left clicking again somewhere else to finish drawing it.")
print("## I'm pretty sure the green square is the extent of the object's hitbox in-game, and you can actually draw outside it too. Probably.")
print("## KEY COMMANDS:")
print("## - s saves your design and quits the program")
print("## - r cancels the current line")
print("## - g will remove a line you've just drawn")
print("## - q has the same function as left clicking")
print("## - esc quits without saving")
print("## The design will be written to a text file in the same directory as this program.")
print("## In order to incorporate your design into the Asteroids! game, simply copy and paste the contents of the file over the similarly-formatted data inside the game's draw_programmatic_object() function.")
print("## Or comment out the appropriate line and simply put this beneath it.")




#### Goal statement ####

# When the user clicks, a point is added to points_array.
# If the user has clicked, a line is draw from the first point in points_array to the cursor.
# If len(points_array) > 1, lines are drawn between the most recently added point and the next most recently added point. ((edit: start and finish each line separately now))
# ...
# When the user hits the Save key, points_array will be exported to a file for use in other programs as a programmatically drawn object.


#### Notes for future improvement ####

# I think this program might be using the wrong kind of event/keypress monitoring. See http://www.pygame.org/docs/tut/newbieguide.html for details, specifically the event subsystem section.

## Update: This problem has something to do with why I put in user_recently_clicked and tied it to the game clock via a ticker variable.
## As a result of that there's a touch of unresponsiveness if you're drawing very quickly. This is to prevent unwanted oversensitivity.
## The way the program is handling clicks makes it too likely to interpret what the user thought was a single click as multiple clicks in succession.
## The solution was to put duct tape over it and be overjoyed that the result actually worked.
## I am told this constitutes valuable work experience.



#### Constants ####

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 300, 300
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GREEN = [0, 255, 0]
SCREEN_CENTER_X, SCREEN_CENTER_Y = (SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2)


#### Functions ####



def add_previous_point_and_current_point_to_lines_array_as_a_line():
    
    
    global user_is_currently_adding_a_line

    lines_array.append([[previous_point[0], previous_point[1]], [cursor_position[0], cursor_position[1]]])
    user_is_currently_adding_a_line = False
    
    



def add_point_to_points_array():
    ''' Places the x, y values of the cursor's current position into points_array. '''
    
    ## This fails at [0, 0], but fixing that opens up another unknown. What placeholder value should the array be initialized with that the user could never click... that itself wouldn't change some hidden property of the array? Negative numbers? Strings??
    if points_array[0] == [0, 0]:
        points_array[0][0] = cursor_position[0]
        points_array[0][1] = cursor_position[1]
    else:
        points_array.append([cursor_position[0], cursor_position[1]])


def write_something_to_a_text_file(supplied_filename, supplied_string_to_write):
    ''' Writes a supplied string to a text file with a supplied name. '''

    text_file = open(supplied_filename, "w")

    text_file.write(supplied_string_to_write)

    text_file.close()


        
def render_all():
    ''' Draw all lines in points_array on the screen. Also draws the tentative next line connecting the last placed point to the cursor, if the user is currently drawing, and draws UI elements. '''
    
    screen.fill(BLACK)
    
    
    if len(points_array) > 1:
        for each_line_index_number in range(1, (len(points_array))):
            ## debugging:
            #print("\neach_line_index_number == " + str(each_line_index_number))
            
            ## Draw each line. Index numbers are taken from the range in the for loop above.
            pygame.draw.line(screen, WHITE, [points_array[(each_line_index_number - 1)][0], points_array[(each_line_index_number - 1)][1]], [points_array[(each_line_index_number)][0], points_array[(each_line_index_number)][1]], 1)
    
    if len(lines_array) >= 1:
        for each_line in range(0, (len(lines_array))):
            pygame.draw.line(screen, WHITE, [lines_array[each_line][0][0], lines_array[each_line][0][1]], [lines_array[each_line][1][0], lines_array[each_line][1][1]], 1)
    
    
    if user_is_drawing == True:
        ## If the user is currently drawing, connect their cursor to the last placed point.
        if len(points_array) > 1:
            pygame.draw.line(screen, WHITE, [previous_point[0][0], previous_point[0][1]], [cursor_position[0], cursor_position[1]], 1)
        elif len(lines_array) >= 0:
            pygame.draw.line(screen, WHITE, [previous_point[0], previous_point[1]], [cursor_position[0], cursor_position[1]], 1)
        
    ## Draws a tiny green dot in the center of the screen. NOT included in the saved programmatic object file; this is for measuring purposes only.
    pygame.draw.rect(screen, GREEN, [(SCREEN_CENTER_X - 1), (SCREEN_CENTER_Y - 1), 2, 2])    
    ## Draws a rectangle around the center 200x200 pixels for measuring purposes. Doing it this way because I want it to be here at the end, drawn on top of user inputted things, alongside the center dot.
    pygame.draw.line(screen, GREEN, [(SCREEN_CENTER_X - 100), (SCREEN_CENTER_Y - 100)], [(SCREEN_CENTER_X + 100), (SCREEN_CENTER_Y - 100)], 1)    
    pygame.draw.line(screen, GREEN, [(SCREEN_CENTER_X + 100), (SCREEN_CENTER_Y - 100)], [(SCREEN_CENTER_X + 100), (SCREEN_CENTER_Y + 100)], 1)
    pygame.draw.line(screen, GREEN, [(SCREEN_CENTER_X + 100), (SCREEN_CENTER_Y + 100)], [(SCREEN_CENTER_X - 100), (SCREEN_CENTER_Y + 100)], 1)
    pygame.draw.line(screen, GREEN, [(SCREEN_CENTER_X - 100), (SCREEN_CENTER_Y + 100)], [(SCREEN_CENTER_X - 100), (SCREEN_CENTER_Y - 100)], 1)
    
        
    pygame.display.flip()
    
    
def handle_keys():
    ''' Interpret pressed keys as input commands. '''
    
    global previous_point
    global keep_window_open
    global user_is_drawing
    global user_is_currently_adding_a_line
    global lines_array
    
    for event in pygame.event.get():   # NOTE: This does not seem to allow for continuously-held-down keys being re-read if another key is pressed and released during the first key's held period.
        if event.type == pygame.QUIT:
            sys.exit
        elif event.type == pygame.KEYDOWN:
            ## events and KEYDOWN prevent multiple firings from holding down buttan.
            
            if event.key == pygame.K_ESCAPE:
                sys.exit
                pygame.quit
                keep_window_open = False ## NOTE: Only this line ACTUALLY works!
                # END PROGRAM DOT YES REALLY.
            
            

            ## Note: Previous program functionality has been disabled. Point-pair lines only now.
            #if event.key == pygame.K_q:
            #    ## Then the user is placing a point at the cursor's position.
            #    user_is_drawing = True
            #    add_point_to_points_array()
            #    previous_point = [cursor_position]
                
            if event.key == pygame.K_r:
                ## Cancels drawing mode.
                user_is_currently_adding_a_line = False
                user_is_drawing = False
                previous_point = [0, 0]
                
            if event.key == pygame.K_q:
                ## Then the user is beginning or ending a line.
                if user_is_currently_adding_a_line == True:
                    ## Ending a line
                    add_previous_point_and_current_point_to_lines_array_as_a_line()
                    previous_point = [0, 0]
                    ## Note: The next line is also checked in add_..._a_line() function. Redundancy. Also safety!
                    user_is_currently_adding_a_line = False
                    user_is_drawing = False
                else:
                    ## Beginning a line
                    user_is_currently_adding_a_line = True
                    user_is_drawing = True
                    previous_point[0] = cursor_position[0]
                    previous_point[1] = cursor_position[1]
                    
            if event.key == pygame.K_g:
                ## Then the user is removing the last completed line.
                if len(lines_array) > 0:
                    lines_array.pop()
                
                
            if event.key == pygame.K_s:
                ## Then the user is saving the array to a file.
                random_code = random.randint(0, 1000000)
                generated_filename = str(len(lines_array)) + '-line programmatic object -- randcode ' + str(random_code) + '.txt'
                
                if len(lines_array) >= 1:
                    for each_line_index in range(0, (len(lines_array))):
                        
                        ## IMPORTANT! This is is only for the scaling system used in my Asteroids! test game.
                        ## Please consider changing this if you're using it in the future; it's better not to divide them at all and use pixels as the yardstick, I'd guess.
                        ## But maybe not?! There might be something to be said for having an independent scale.
                        ## Note that the Asteroids! test game uses (object_size / 20) and here dividing the numbers by 10 as seen will fit them to that (foo / 20) metric.
                        ## Imagine a grid, 20x20, with scaling from -10 to +10 on both axes...
                        ## That system is conceptually useful when centerpoints are important for things like radius-based collision detection.
                        
                        # start X    
                        lines_array[each_line_index][0][0] = ((SCREEN_CENTER_X - lines_array[each_line_index][0][0]) / 10)
                        # start Y
                        lines_array[each_line_index][0][1] = ((SCREEN_CENTER_Y - lines_array[each_line_index][0][1]) / 10)
                        # end X
                        lines_array[each_line_index][1][0] = ((SCREEN_CENTER_X - lines_array[each_line_index][1][0]) / 10)
                        # end Y
                        lines_array[each_line_index][1][1] = ((SCREEN_CENTER_Y - lines_array[each_line_index][1][1]) / 10)
                
                
                    ## If the end point of one line are close to the start point of the next, this code splits the difference. Note this assumes you care about exactly matching endpoints.
                    
                    for each_line_index in range(0, (len(lines_array))):
                    
                    
                        ## Special case of the first and last points:
                        if each_line_index == 0:
                            start_x_of_current_line = lines_array[each_line_index][0][0]
                            end_x_of_previous_line = lines_array[(len(lines_array) - 1)][1][0]
                            
                            start_y_of_current_line = lines_array[each_line_index][0][1]
                            end_y_of_previous_line = lines_array[(len(lines_array) - 1)][1][1]
                            
                        else:
                            start_x_of_current_line = lines_array[each_line_index][0][0]
                            end_x_of_previous_line = lines_array[(each_line_index - 1)][1][0]
                        
                            start_y_of_current_line = lines_array[each_line_index][0][1]
                            end_y_of_previous_line = lines_array[(each_line_index - 1)][1][1]
                        
                        
                        
                        ## X
                        if ( (abs(start_x_of_current_line - end_x_of_previous_line)) <= 0.4 ):
                            ## If abs(difference between the end points) <= 0.4, split the difference and set it to that.
                            difference_between_them = (abs(start_x_of_current_line - end_x_of_previous_line))
                            half_of_the_difference = (difference_between_them / 2)
                            
                            start_x_of_current_line += half_of_the_difference
                            end_x_of_previous_line -= half_of_the_difference
                                    
                            ## Round to the nearest tenth
                            start_x_of_current_line *= 10
                            start_x_of_current_line = start_x_of_current_line // 10
                            end_x_of_previous_line *= 10
                            end_x_of_previous_line = end_x_of_previous_line // 10
                                    
                        ## Y
                        
                        if ( (abs(start_y_of_current_line - end_y_of_previous_line)) <= 0.4 ):
                            ## If abs(difference between the end points) <= 0.4, split the difference and set it to that.
                            difference_between_them = (abs(start_y_of_current_line - end_y_of_previous_line))
                            half_of_the_difference = (difference_between_them / 2)
                            
                            start_y_of_current_line += half_of_the_difference
                            end_y_of_previous_line -= half_of_the_difference
                            
                            ## Round to the nearest tenth
                            start_y_of_current_line *= 10
                            start_y_of_current_line = start_y_of_current_line // 10
                            end_y_of_previous_line *= 10
                            end_y_of_previous_line = end_y_of_previous_line // 10    
                            
                        ## This part actually does the setting. I feel like some kind of list comprehension would have helped with the index numbers. To-do list: Learn everything about list comprehensions.        
                        if each_line_index == 0:
                            lines_array[each_line_index][0][0] = start_x_of_current_line
                            lines_array[(len(lines_array) - 1)][1][0] = end_x_of_previous_line
                                
                            lines_array[each_line_index][0][1] = start_y_of_current_line
                            lines_array[(len(lines_array) - 1)][1][1] = end_y_of_previous_line
                        
                        else:
                            lines_array[each_line_index][0][0] = start_x_of_current_line
                            lines_array[(each_line_index - 1)][1][0] = end_x_of_previous_line
                                
                            lines_array[each_line_index][0][1] = start_y_of_current_line
                            lines_array[(each_line_index - 1)][1][1] = end_y_of_previous_line
                    
                    
                    
                    
                
                
                
                write_something_to_a_text_file(generated_filename, str(lines_array))
                keep_window_open = False
                
                
#### Initializations ####


screen = pygame.display.set_mode(SCREEN_SIZE)

user_is_drawing = False

user_is_currently_adding_a_line = False

user_recently_clicked = False

points_array = [[0, 0]]

lines_array = []

previous_point = [0, 0]

## To keep the game running
keep_window_open = True

## Create a clock object to make the game run at a specified speed in the main loop
clock = pygame.time.Clock()

## Using the game_ticker model is currently necessary to decouple program running speed from pygame's Clock function. There's probably a better way to do this somewhere... This is fairly simple, though.
game_ticker = 0

#### Main Loop ####


while keep_window_open == True:

    cursor_position = cursor_x, cursor_y = pygame.mouse.get_pos()

    button1_pressed, button2_pressed, button3_pressed = pygame.mouse.get_pressed()
    
    
    ## Process keyboard input
    handle_keys()
    
    

            
    ## Event progression metering
    clock.tick(40)
    
    if game_ticker < 80:
        game_ticker += 1
    elif game_ticker >= 80:
        game_ticker = 0
    
    
    ## Note: Previous program functionality has been disabled. Point-pair lines only now.
    #if button1_pressed == True:
    #    ## Left mouse click enables drawing mode and places a point in points_array.
    #    user_is_drawing = True
    #    add_point_to_points_array()
    #    previous_point = [cursor_position]
    
    if ( (user_recently_clicked == True) and ((game_ticker % 30) == 1) ):
        user_recently_clicked = False
        
    if ((game_ticker % 1) == 0):    
        
        if ((button1_pressed == True) and (user_recently_clicked == False)):    
            if user_is_currently_adding_a_line == True:
                ## Ending a line
                add_previous_point_and_current_point_to_lines_array_as_a_line()
                previous_point = [0, 0]
                ## Note: The next line is also checked in add_..._a_line() function. Redundancy. Also safety!
                user_is_currently_adding_a_line = False
                user_is_drawing = False
                user_recently_clicked = True
            else:
                ## Beginning a line
                user_is_currently_adding_a_line = True
                user_is_drawing = True
                previous_point[0] = cursor_position[0]
                previous_point[1] = cursor_position[1]
                user_recently_clicked = True
                    
            
            
            
        if button3_pressed == True:
            ## Right mouse click cancels drawing mode.
            user_is_currently_adding_a_line = False
            user_is_drawing = False
            previous_point = [0, 0]
        
        ## Debugging section ---v
        
        ## Note: Previous program functionality has been disabled. Point-pair lines only now.
        #print("\npoints_array == " + str(points_array))
        #print("\nprevious_point == " + str(previous_point))
        
        
        # print("\nlines_array == " + str(lines_array))
        # print("\nprevious_point == " + str(previous_point))
        
    
    ## Display everything that needs to be displayed
    render_all()

# "Be IDLE friendly," they said.    
pygame.quit    
    
