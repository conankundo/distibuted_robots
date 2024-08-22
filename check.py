import pygame
import sys

# Khởi tạo Pygame
pygame.init()

# Kích thước ô vuông
TILE_SIZE = 50
# Kích thước bản đồ
MAP_WIDTH = 10
MAP_HEIGHT = 10
# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

g_centers = []
# Tạo màn hình
screen = pygame.display.set_mode((MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE))
pygame.display.set_caption("Map 5x5")

# Hàm vẽ bản đồ
def draw_map():
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            g_centers.append(rect.center)
            print(rect.center)
            pygame.draw.rect(screen, BLACK, rect, 1)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Xóa màn hình bằng màu trắng
    screen.fill(WHITE)
    # Vẽ bản đồ
    draw_map()
    # Cập nhật màn hình
    pygame.display.flip()

# Kết thúc Pygame
pygame.quit()
sys.exit()
