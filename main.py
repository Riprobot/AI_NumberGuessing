from model import get_result
import pygame

img_size = 28
image = [[0.0] * img_size for i in range(img_size)]
pygame.init()
screen_size = 800
clear_button_width = 300
clear_button_height = 100
number_guess_period = 1000
clear_button_pos = (screen_size, 0)
font = pygame.font.Font(None, 32)
bold_delta = 0.2
block_size = screen_size // img_size
screen = pygame.display.set_mode([screen_size + clear_button_width, screen_size])
running = True
screen.fill((255, 255, 255))
pygame.draw.rect(screen, (255, 0, 0),
                 pygame.Rect(clear_button_pos[0], clear_button_pos[1], clear_button_width, clear_button_height))
clear_text = font.render("Clear", True, (0, 0, 0))
clear_text_rect = clear_text.get_rect()
screen.blit(clear_text, (clear_button_pos[0] + (clear_button_width - clear_text_rect.width) // 2,
                         clear_button_pos[1] + (clear_button_height - clear_text_rect.height) // 2))


def draw_point_sides(x, y):
    pygame.draw.rect(screen, (230, 230, 230), pygame.Rect(x * block_size, y * block_size, block_size, block_size),
                     1)


for x in range(img_size):
    for y in range(img_size):
        draw_point_sides(x, y)


def draw_point(x, y):
    pygame.draw.rect(screen,
                     (int(255 * (1 - image[x][y])), int(255 * (1 - image[x][y])), int(255 * (1 - image[x][y]))),
                     pygame.Rect(x * block_size, y * block_size, block_size, block_size))


def put_point(x, y, add_delta=bold_delta):
    if x < 0 or y < 0 or add_delta <= 0 or x >= img_size or y >= img_size:
        return
    image[x][y] = min(1.0, image[x][y] + add_delta)
    draw_point(x, y)
    put_point(x, y - 1, add_delta - bold_delta * 4 / 5)
    put_point(x, y + 1, add_delta - bold_delta * 4 / 5)
    put_point(x - 1, y, add_delta - bold_delta * 4 / 5)
    put_point(x + 1, y, add_delta - bold_delta * 4 / 5)
    put_point(x - 1, y - 1, add_delta - bold_delta * 6 / 7)
    put_point(x + 1, y + 1, add_delta - bold_delta * 6 / 7)
    put_point(x - 1, y + 1, add_delta - bold_delta * 6 / 7)
    put_point(x + 1, y - 1, add_delta - bold_delta * 6 / 7)


def draw_answer():
    answer = str(get_result(image))
    text = font.render(answer, True, (0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(screen_size, clear_button_height, 32, 32))
    screen.blit(text, (screen_size, clear_button_height))


def clear_image():
    for i in range(img_size):
        for j in range(img_size):
            image[i][j] = 0
            draw_point(i, j)
            draw_point_sides(i, j)


iteration = 0
while running:
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if clear_button_pos[0] <= mouse_pos[0] <= clear_button_pos[0] + clear_button_width and clear_button_pos[
                1] <= mouse_pos[1] <= clear_button_pos[1] + clear_button_height:
                clear_image()
    if pygame.mouse.get_pressed()[0]:
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] <= screen_size and mouse_pos[1] <= screen_size:
            x = min(img_size - 1, img_size - 1, mouse_pos[0] // block_size)
            y = min(img_size - 1, img_size - 1, mouse_pos[1] // block_size)
            put_point(x, y)
    # Flip the display
    iteration += 1
    if iteration % number_guess_period == 0:
        draw_answer()
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
