import pygame
import sys

# Game parameters
screen_width = 160
screen_height = 120
background_color = (255, 255, 255)  # White background

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Phytominoes")
clock = pygame.time.Clock()

# Load resources
font = pygame.font.Font(None, 16)  # Default font, size 16

# Button parameters
button_color = (200, 200, 200)  # Light gray
button_hover_color = (180, 180, 180)  # Slightly darker when hovered
button_text_color = (0, 0, 0)  # Black text
button_rect = pygame.Rect(50, 70, 60, 20)  # x, y, width, height

def draw_button(mouse_pos):
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, button_hover_color, button_rect)
    else:
        pygame.draw.rect(screen, button_color, button_rect)
    pygame.draw.rect(screen, (0, 0, 0), button_rect, 1)  # Button border
    
    button_text = font.render("Quit", True, button_text_color)
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)

def update():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

def draw():
    screen.fill(background_color)
    title_text = font.render("Phytominoes", True, (0, 0, 0))  # Black text
    screen.blit(title_text, (55, 10))
    draw_button(pygame.mouse.get_pos())
    pygame.display.flip()

# Main game loop
while True:
    update()
    draw()
    clock.tick(30)  # 30 FPS
