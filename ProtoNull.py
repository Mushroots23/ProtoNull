import pygame as pg
import os
import math
import random
import numpy as np
import time
from frame_loader import FrameLoader
from circle import Circle

# Initialize Pygame
pg.init()

# Initialize the joystick module
pg.joystick.init()

# Check for available joysticks
joystick_count = pg.joystick.get_count()
if joystick_count == 0:
    joyStick = False
    print("No joysticks found.")
else:
    # Use the first joystick found
    joyStick = True
    joystick = pg.joystick.Joystick(0)
    joystick.init()

# Set screen dimensions
screen_width = 1024
screen_height = 768
screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("Prototype_Null")

# Set clock for controlling fps
clock = pg.time.Clock()
bpm = 145 
fps_factor = 4
fps = bpm / float(fps_factor)

# Flag to indicate if we need to switch to the next folder
switch_folder = False

# Initialize variables for streaming frames
current_slot_number = 1
base_path = "slots\\"
current_frames_folder = base_path + f"slot{current_slot_number}"
next_folder = current_frames_folder
next_frames_folder = ""  # Next folder to load
frame_files = []  # List to store frame file names
frame_index = 0  # Index of the current frame
loader = FrameLoader(current_frames_folder)
loader.load_frames(current_frames_folder)  # Load frames from the initial folder
last_frame_time = time.time()
frame_duration = 1.0 / fps

# Get a list of all directories in the specified folder
directories = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]

# Determine the number of folders
slot_count = len(directories)

print("Number of folders:", slot_count)

# Initialize looping variables
looping = False
looping_saw = False
loop_start_frame = 0
start_loop_frame_count = 15  # Number of frames to loop through
loop_direction = 1  # Direction of ping pong loop
start_amplitude = 7.5
alpha = 255

# Circle properties
circle_radius = 25
circle_color = (255, 0, 0)
circle_color1 = (255, 0, 0)
circle_x = screen_width // 2
circle_y = screen_height // 2
circle_speed_x = 5
circle_speed_y = 5
raw1_circle_speed_x = 5
raw1_circle_speed_y = 5
raw2_circle_speed_x = 5
raw2_circle_speed_y = 5
is_circle = True
circle_color2 = (0, 255, 0, 0)
stop_circle = True

# Set the initial alpha value
darkness_alpha = 0  # (0-255 range)

sub_blend = False

# Function to apply blocks of pixels
glitch = False
stop_progress = False
block_size = 20
max_offset = 5

def glitch_image(image, block_size, max_offset):
    glitched_image = image.copy()
    width, height = image.get_size()
    for y in range(0, height, block_size):
        for x in range(0, width, block_size):
            # Ensure that the block is within the bounds of the image
            if x + block_size <= width and y + block_size <= height:
                if x % (block_size * 2) == 0 and y % (block_size * 2) == 0:
                    # Randomly shift the block
                    offset_x = random.randint(-max_offset, max_offset)
                    offset_y = random.randint(-max_offset, max_offset)
                    block = pg.Rect(x, y, block_size, block_size)
                    region = image.subsurface(block)
                    # Ensure that the blit stays within image bounds
                    new_x = min(max(x + offset_x, 0), width - block_size)
                    new_y = min(max(y + offset_y, 0), height - block_size)
                    glitched_image.blit(region, (new_x, new_y))
    return glitched_image

# Main loop
running = True
fullscreen = False
frame_index = 0
circle = Circle(circle_x, circle_y, circle_speed_x, circle_speed_y, screen_width, screen_height)
circle1 = Circle(circle_x - 30, circle_y + 20, circle_speed_x, circle_speed_y, screen_width, screen_height)
circle2 = Circle(circle_x, circle_y, circle_speed_x, circle_speed_y, screen_width, screen_height)
circle3 = Circle(circle_x - 30, circle_y + 20, circle_speed_x, circle_speed_y, screen_width, screen_height)
circle_color = (255, 0, 0)
color_change_frame = 0
size_change_frame = 0
shift = False
time.sleep(2)
while running:
    # Measure the current time
    start_time = time.time()
    current_time = time.time()

    # Calculate the time elapsed since the last frame
    elapsed_time = current_time - last_frame_time

    # Calculate the number of frames to increment the frame index
    frames_to_increment = max(1, round(elapsed_time / frame_duration))

    # Update the last_frame_time for the next iteration
    last_frame_time = current_time

    fps = bpm / float(fps_factor)
    mask_surface = pg.Surface((screen_width, screen_height), pg.SRCALPHA)
    mask_surface.fill((0, 0, 0, 0))  # Fill with transparent color
    frame_index = loader.get_frame_index()
    frame_files = loader.get_num_frames()

    for event in pg.event.get():
        if event.type == pg.QUIT:
                running = False
        elif event.type == pg.KEYDOWN:
            # Increase bpm by 1 when 'Up' arrow key is pressed
            if event.key == pg.K_UP:
                bpm += 1
                print("bpm:", bpm, "fps:", fps)
            # Decrease bpm by 1 when 'Down' arrow key is pressed
            if event.key == pg.K_DOWN:
                bpm -= 1
                print("bpm:", bpm, "fps:", fps)
                if bpm < 60:  # Ensure bpm doesn't go below 60
                    bpm = 60
            # Toggle looping when space bar is pressed
            if event.key == pg.K_SPACE:
                if looping:
                    first = False
                    print("first true")
                else:
                    first = True
                    print("first false")
                looping = not looping
                loop_frame_count = 30
                if looping:
                    loop_start_frame = frame_index  # Set loop_start_frame when looping starts
            if event.key == pg.K_LSHIFT and looping:
                loop_frame_count = 30 
            if event.key == pg.K_RSHIFT and looping:
                loop_frame_count = 60
            if event.key == pg.K_f:
                # Toggle fullscreen mode
                fullscreen = not fullscreen
                if fullscreen:
                    # Set fullscreen mode with current desktop resolution
                    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
                    # Get new screen dimensions
                    screen_width, screen_height = screen.get_size()
                else:
                    screen = pg.display.set_mode((screen_width, screen_height))
            if event.key == pg.K_ESCAPE:
                running = False
            if event.key == pg.K_RETURN:
                # Display a random frame when Enter key is pressed
                frame_index += 60
                loop_start_frame += 60
            if event.key == pg.K_t:
                stop_thread = True
                # Increment the slot number
                current_slot_number += 1
                # Check if current_slot_number exceeds 4, loop back to 1
                current_slot_number = (current_slot_number - 1) % slot_count + 1
                # Update the folder path
                next_frames_folder = base_path + f"slot{current_slot_number}"
                switch_folder = True
        elif event.type == pg.JOYBUTTONDOWN:
            if event.button == 5:
                shift = True
            # Handle joystick button events
            if event.button == 13:
                    if shift:
                        fps_factor *= 0.5
                        fps = bpm / float(fps_factor)
                    else:
                        # Increment the slot number
                        current_slot_number -= 1
                        # Check if current_slot_number is less than 1, cycle back to 4
                        if current_slot_number < 1:
                            # Set current_slot_number to the maximum slot count
                            current_slot_number = slot_count
                        # Update the folder path
                        next_frames_folder = base_path + f"slot{current_slot_number}"
                        switch_folder = True
            if event.button == 2:
                if shift:
                    stop_circle = not stop_circle
                else:
                    is_circle = not is_circle
            if event.button == 14:
                if shift:
                    fps_factor *= 2
                    fps = bpm / float(fps_factor)
                else:
                    # Increment the slot number
                    current_slot_number += 1
                    # Check if current_slot_number exceeds 4, loop back to 1
                    current_slot_number = (current_slot_number - 1) % slot_count + 1
                    # Update the folder path
                    next_frames_folder = base_path + f"slot{current_slot_number}"
                    switch_folder = True
            if event.button == 3:
                is_circle = True
                looping = False
                looping_saw = False
                frame_index = 0
                alpha = 255
            if event.button == 7:
                alpha = 255
                darkness_alpha = 0
            if event.button == 1:
                frame_index += (240*4)
                loop_start_frame += 120
            if event.button == 9:
                if shift:
                    stop_progress = not stop_progress
                else:
                    frame_index -= 30
                    loop_start_frame -= 30
            if event.button == 10:
                frame_index += 30
                loop_start_frame += 30
            if event.button == 8:
                glitch = not glitch
            if event.button == 12:
                if looping or looping_saw:
                    loop_frame_count = math.ceil(loop_frame_count / 2)
                    amplitude = math.ceil(amplitude/2)
                    print(loop_frame_count)
            if event.button == 11:
                if looping or looping_saw:
                    loop_frame_count *= 2
                    amplitude *= 2
                    print(loop_frame_count)
            if event.button == 0:
                is_circle = False
                looping = True
                sub_blend = False
                glitch = False
                stop_progress = False
                alpha = 255
                loop_start_frame = frame_index
                looping_saw = False
                loop_progress = 0
                loop_frame_count = start_loop_frame_count
                amplitude = start_amplitude
                darkness_alpha = 0
                # Convert milliseconds to seconds
                loop_start_time = pg.time.get_ticks() / 1000
            if event.button == 6:
                if shift:
                    bpm += 10
                    fps = bpm / float(fps_factor)
                    print("bpm:", bpm, "fps:", fps)
                else:
                    bpm += 1
                    fps = bpm / float(fps_factor)
                    print("bpm:", bpm, "fps:", fps)
            if event.button == 4:
                if shift:
                    bpm -= 10
                    fps = bpm / float(fps_factor)
                    # Ensure bpm doesn't go below 60
                    if bpm < 60:
                        bpm = 60
                    print("bpm:", bpm, "fps:", fps)
                else:
                    bpm -= 1
                    fps = bpm / float(fps_factor)
                    # Ensure bpm doesn't go below 60
                    if bpm < 60:
                        bpm = 60
                    print("bpm:", bpm, "fps:", fps)
            if event.button == 15:
                # Toggle fullscreen mode
                fullscreen = not fullscreen
                mask_surface = pg.Surface((screen_width, screen_height), pg.SRCALPHA)
                if fullscreen:
                    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)  # Set fullscreen mode with current desktop resolution
                    screen_width, screen_height = screen.get_size()  # Get new screen dimensions
                    print(screen_width, screen_height)
                else:
                    screen = pg.display.set_mode((screen_width, screen_height))
        elif event.type == pg.JOYBUTTONUP:
            if event.button == 5:
                shift = False
        elif event.type == pg.JOYAXISMOTION:
            if event.axis == 4:  # ZL button (left trigger)
                if event.value > 0.5:  # Button pressed
                    if shift:
                        sub_blend = not sub_blend
                    else:
                        looping_saw = not looping_saw
                        looping = False
                        loop_progress = 0
                        loop_frame_count = start_loop_frame_count
                        amplitude = start_amplitude
                        loop_start_frame = frame_index
                        loop_start_time = pg.time.get_ticks() / 1000  # Convert milliseconds to seconds
                    if not sub_blend:
                        darkness_alpha = 0
            if event.axis == 5:  # ZL button (left trigger)
                if event.value > 0.5:  # Button pressed
                    looping = not looping
                    looping_saw = False
                    loop_progress = 0
                    loop_frame_count = start_loop_frame_count
                    amplitude = start_amplitude
                    loop_start_frame = frame_index
                    loop_start_time = pg.time.get_ticks() / 1000  # Convert milliseconds to seconds
        if joyStick:
            joystick1_x = joystick.get_axis(0)  # X-axis input
            joystick1_y = joystick.get_axis(1)  # Y-axis input
            joystick2_x = joystick.get_axis(2)  # X-axis input
            joystick2_y = joystick.get_axis(3)  # Y-axis input
            alpha += int(joystick1_x * 3)
            if alpha > 255:
                alpha = 255
            if alpha < 0:
                alpha = 0
            max_offset += int(joystick2_y * 2)
            if max_offset > 100:
                max_offset = 100
            if max_offset < 1:
                max_offset = 1
            block_size += int(joystick2_x * 2)
            if block_size > 1000:
                block_size = 1000
            if block_size < 10:
                block_size = 10
            
        
        
    if looping:
        loop_time = pg.time.get_ticks() / 1000 - loop_start_time
        loop_progress = math.sin(2 * math.pi * loop_time * fps / loop_frame_count) * amplitude
        # Determine the frame index based on the ping pong loop progress and starting frame
        frame_index = (loop_start_frame + round(loop_progress)) % frame_files

    if looping_saw:
        sawtooth_frequency = fps / loop_frame_count
        loopsaw_time = pg.time.get_ticks() / 1000 - loop_start_time
        loop_progress = (loopsaw_time * sawtooth_frequency) % 1.0 * (amplitude*2)
        # Determine the frame index based on the ping pong loop progress and starting frame
        frame_index = (loop_start_frame + round(loop_progress)) % frame_files

    if switch_folder:
        loader.switch_folder(next_frames_folder)
        frame_files = loader.get_num_frames()
        frame_index = (frame_index + 1) % frame_files
        switch_folder = False

    if not stop_progress:
        frame_index = (frame_index + 1) % frame_files
        # Load frame at the specified index
        loader.set_frame_index(frame_index)
        frame_surface = loader.load_next_frame(alpha)
        destiny_surface = frame_surface

    if glitch:
        loader.set_frame_index(frame_index)
        frame_surface = glitch_image(frame_surface, block_size, max_offset)
        frame_surface.set_alpha(alpha)
        destiny_surface = frame_surface

    if sub_blend:
        loader.set_frame_index(frame_index)
        sub_dark_alpha = darkness_alpha
        if frame_index % 30 == 0 or (frame_index + 1) % 30 == 0 or (frame_index + 2) % 30 == 0 or (frame_index + 3) % 30 == 0 or (frame_index + 4) % 30 == 0 or (frame_index + 5) % 30 == 0 or (frame_index + 6) % 30 == 0:
            destiny_surface = frame_surface
            frame_surface = loader.load_next_frame(alpha)
                    
            # Convert surfaces to NumPy arrays
            source_array = pg.surfarray.pixels3d(frame_surface)
            destiny_array = pg.surfarray.pixels3d(destiny_surface)

            # Perform subtractive blending
            result_array = np.maximum(destiny_array + source_array, 0)
            
            # Create a new surface from the modified array
            frame_surface = pg.surfarray.make_surface(result_array)
            frame_surface.set_alpha(alpha)
            darkness_alpha = 80
        else:
            darkness_alpha = 0

    # Determine blitting positions and dimensions
    frame_width, frame_height = frame_surface.get_size()

    # Calculate the scale factors for resizing the frame_surface
    if frame_width - frame_height >= 0:
        frame_surface = pg.transform.scale(frame_surface, (screen_width, screen_height))
    else:
        frame_surface = pg.transform.scale(frame_surface, (screen_width/2, screen_height))

    frame_width, frame_height = frame_surface.get_size()

    # Blit the frame to the left half of the screen
    screen.blit(frame_surface, (0, 0))

    # Mirror the frame and blit it to the right half of the screen
    mirrored_frame_surface = pg.transform.flip(frame_surface, True, False)
    if frame_width <= screen_width / 2:
        # Adjust the blitting position for frames that are half the screen width
        mirrored_frame_rect = mirrored_frame_surface.get_rect()
        mirrored_frame_rect.topleft = (screen_width // 2, 0)
        screen.blit(mirrored_frame_surface, mirrored_frame_rect)

    # Create a surface to darken the screen
    dark_surface = pg.Surface((screen_width, screen_height))
    dark_surface.fill((0, 0, 0))  # Fill with black color
    dark_surface.set_alpha(darkness_alpha)  # Set the transparency level
    screen.blit(dark_surface, (0, 0))

    if not stop_circle:
        circle.update_position(circle_radius, fullscreen)
        circle1.update_position(circle_radius, fullscreen)
        circle2.update_position(circle_radius, fullscreen)
        circle3.update_position(circle_radius, fullscreen)
        circle.draw(mask_surface, circle_color1, circle_color2, circle_radius, is_circle)
        circle1.draw(mask_surface, circle_color1, circle_color2, circle_radius-10, is_circle)
        circle2.draw(mask_surface, circle_color, circle_color2, circle_radius-20, is_circle)
        circle3.draw(mask_surface, circle_color, circle_color2, circle_radius-30, is_circle)

    # Create a copy of the original image
    image_copy = frame_surface.copy()

    screen.blit(mask_surface, (0, 0))

    # Update display
    pg.display.flip()

   # Change circle size every frame using a sine wave to pulsate
    circlesize_time = pg.time.get_ticks() / 1000
    pulsation_factor = abs(math.sin(fps_factor * math.pi * circlesize_time * fps / 60))
    max_radius = 50
    min_radius = 10
    circle_radius = int(min_radius + (max_radius - min_radius) * pulsation_factor)

    # Change circle color every 30 frames
    max_alpha = 100
    min_alpha = 0
    max_red = 250
    min_red = 100
    circlecol_time = time.time() / 1
    pulsation_factor = abs(math.sin(fps_factor * math.pi * circlecol_time * fps / 120))
    circle_alpha = int(min_radius + (max_alpha - min_alpha) * pulsation_factor)
    red = int(min_red + (max_red - min_red) * pulsation_factor)
    green = int(min_alpha + (max_alpha - min_alpha) * pulsation_factor)
    blue = 255 - int(min_alpha + (max_alpha - min_alpha) * pulsation_factor)
    circle_color = (red, green, blue, circle_alpha)
    circle_color1 = (255 - red, 255 - green, 255 - blue, circle_alpha)
    circle_color2 = (0, 0, 0, 0)
    color_change_frame = frame_index

    # Calculate elapsed time
    elapsed_Ttime = time.time() - start_time

    # Perform time delay if necessary
    if elapsed_Ttime < (1 / fps):
        time.sleep((1 / fps) - elapsed_Ttime)

    # *Debug* Measure frame rate
    #frame_rate = 1 / (time.time() - start_time) 
    #print("Frame rate:", frame_rate, "Fps:", fps, "BPM:", bpm)

# Clean up
pg.quit()
