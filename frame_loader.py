import os
import pygame as pg

class FrameLoader:
    def __init__(self, base_path):
        self.base_path = base_path
        self.current_folder = base_path
        self.frame_files = []
        self.frame_index = 0

    def load_frames(self, folder):
        self.current_folder = folder
        self.frame_files = sorted(os.listdir(folder))

    def load_next_frame(self, alpha):
        frame_path = os.path.join(self.current_folder, self.frame_files[self.frame_index])
        frame_surface = pg.image.load(frame_path).convert_alpha()
        frame_surface.set_alpha(alpha)
        return frame_surface

    def switch_folder(self, folder):
        next_folder = folder
        if os.path.isdir(next_folder):
            self.load_frames(next_folder)
            # Reset frame index when switching folders
        else:
            print(f"Folder '{folder}' does not exist.")

    def get_frame_index(self):
        return self.frame_index

    def set_frame_index(self, index):
        if 0 <= index < len(self.frame_files):
            self.frame_index = index
        else:
            print("Invalid frame index.")

    def get_num_frames(self):
        return len(self.frame_files)

# Example usage:
if __name__ == "__main__":
    screen_width = 960
    screen_height = 540

    # Initialize Pygame
    pg.init()
    screen = pg.display.set_mode((screen_width, screen_height))
    clock = pg.time.Clock()

    base_path = "slots/"
    loader = FrameLoader(base_path)
    loader.load_frames(base_path + "slot1")  # Load frames from the initial folder

    alpha = 255  # Example alpha value

    running = True
    while running:

        # Get the number of frames in the current folder
        num_frames = loader.get_num_frames()

        # Get the current frame index
        frame_index = loader.get_frame_index()

        # Set the new frame index
        loader.set_frame_index(frame_index)

        # Load the next frame using the updated frame index
        frame_surface = loader.load_next_frame(alpha)
        screen.blit(frame_surface, (0, 0))
        
        # Update display
        pg.display.flip()
        clock.tick(60)
