import pygame
import time
import os
from moviepy.editor import ImageSequenceClip, AudioFileClip

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 1080, 1920
FONT_SIZE = 110
TEXT = "Chat, write a song about children in China"
CURSOR_WIDTH = 15  # Width of the cursor
CURSOR_HEIGHT = FONT_SIZE + 10  # Height of the cursor
CURSOR_BLINK_INTERVAL = 0.5  # Time in seconds for cursor blinking

# Set up display (hidden)
screen = pygame.Surface((WIDTH, HEIGHT))  # Use a surface instead of a window

# Load a monospaced font
try:
    font = pygame.font.Font('font/JetBrainsMonoNL-Regular.ttf', FONT_SIZE)
except FileNotFoundError:
    font = pygame.font.SysFont('Courier New', FONT_SIZE)

# Define colors
GREEN = (0, 255, 0)
BLACK = (8, 10, 8)

def wrap_text(text, font, max_width):
    lines = []
    words = text.split(' ')
    current_line = ''
    for word in words:
        test_line = f'{current_line} {word}'.strip()
        text_surface = font.render(test_line, True, GREEN)
        if text_surface.get_width() <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines

def save_typing_effect_images(text, duration=3):
    wrapped_lines = wrap_text(text, font, WIDTH - 200)
    total_chars = sum(len(line) for line in wrapped_lines)
    
    # Calculate the typing delay
    delay_per_char = duration / total_chars if total_chars > 0 else 0
    
    frame_number = 0
    typed_lines = []

    start_time = time.time()  # To manage cursor blinking

    # Create the rendering directory if it doesn't exist
    os.makedirs('rendering', exist_ok=True)

    for line_index, line in enumerate(wrapped_lines):
        # Type out each character of the current line
        for i in range(len(line) + 1):
            screen.fill(BLACK)  # Black background

            # Draw all lines up to the current one
            for j in range(len(wrapped_lines)):
                if j < len(typed_lines) + 1:  # Ensure only lines up to current line are rendered
                    visible_text = wrapped_lines[j][:i] if j == len(typed_lines) else wrapped_lines[j]
                    line_surface = font.render(visible_text, True, GREEN)
                    line_rect = line_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - (FONT_SIZE * 1.2) * (len(wrapped_lines) // 2 - j)))
                    screen.blit(line_surface, line_rect.topleft)

                    # Draw cursor if it is on the current line
                    if j == line_index:
                        cursor_x = line_rect.left + font.render(wrapped_lines[j][:i], True, GREEN).get_width()
                        cursor_y = line_rect.top
                        cursor_rect = pygame.Rect(cursor_x, cursor_y, CURSOR_WIDTH, CURSOR_HEIGHT)
                        if (time.time() - start_time) % (2 * CURSOR_BLINK_INTERVAL) < CURSOR_BLINK_INTERVAL:
                            pygame.draw.rect(screen, GREEN, cursor_rect)
            
            # Save the frame
            pygame.image.save(screen, f"rendering/frame_{frame_number:03d}.png")
            frame_number += 1

            time.sleep(delay_per_char)

        # Add the fully typed line to the list of typed lines
        typed_lines.append(line)
        
        # Short delay between lines
        time.sleep(0.5)

    # Save the last frame twice
    if frame_number > 0:
        pygame.image.save(screen, f"rendering/frame_{frame_number:03d}.png")
        frame_number += 1
        pygame.image.save(screen, f"rendering/frame_{frame_number:03d}.png")

def create_video_from_frames(frame_folder='rendering', output_filename='typing_effect.mp4', fps=12, audio_file='sound/typing.mp3'):
    # Get sorted list of frame files
    frame_files = sorted([os.path.join(frame_folder, f) for f in os.listdir(frame_folder) if f.startswith('frame_') and f.endswith('.png')])
    
    # Create a video clip from the images
    video_clip = ImageSequenceClip(frame_files, fps=fps)
    
    # Load the audio file
    audio_clip = AudioFileClip(audio_file)
    
    # Set audio to video clip
    video_clip = video_clip.set_audio(audio_clip)
    
    # Write the video file
    video_clip.write_videofile(output_filename, codec='libx264')

# Run functions to save images and create video
save_typing_effect_images(TEXT)
create_video_from_frames(output_filename='typing_effect.mp4', audio_file='sound/typing.mp3')

pygame.quit()
