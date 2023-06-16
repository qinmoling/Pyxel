import pygame
pygame.init()

WIDTH = 800
HEIGHT = 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Game Editor")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

PIXEL_SIZE = 20
LEVEL_WIDTH = WIDTH // PIXEL_SIZE
LEVEL_HEIGHT = HEIGHT // PIXEL_SIZE

state = "LEVEL"

level = [[0 for y in range(LEVEL_HEIGHT)] for x in range(LEVEL_WIDTH)]

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PIXEL_SIZE, PIXEL_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_l:
                state = "LEVEL"
            elif event.key == pygame.K_p:
                state = "PLAYER"
            elif event.key == pygame.K_s:
                with open("level.txt", "w") as f:
                    for row in level:
                        f.write("".join(str(x) for x in row) + "\n")
#设计等级
    if state == "LEVEL":
        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            x //= PIXEL_SIZE
            y //= PIXEL_SIZE
            level[x][y] = 1
        elif pygame.mouse.get_pressed()[2]:
            x, y = pygame.mouse.get_pos()
            x //= PIXEL_SIZE
            y //= PIXEL_SIZE
            level[x][y] = 0

        SCREEN.fill(WHITE)
        for x in range(LEVEL_WIDTH):
            for y in range(LEVEL_HEIGHT):
                if level[x][y] == 1:
                    pygame.draw.rect(SCREEN, GRAY, (x * PIXEL_SIZE, y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))
#设计人物
    elif state == "PLAYER":
        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            x //= PIXEL_SIZE
            y //= PIXEL_SIZE
            player.update(x * PIXEL_SIZE, y * PIXEL_SIZE)

        SCREEN.fill(WHITE)
        all_sprites.draw(SCREEN)

    pygame.display.flip()

pygame.quit()