import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(640, 360)
player_size = 200
player = pygame.Surface((player_size, player_size), pygame.SRCALPHA)
pygame.draw.circle(player, (255, 0, 0), (player_size // 2, player_size // 2), player_size // 2)
player_rect = player.get_rect(center=player_pos)

obstacle = pygame.Surface((player_size, player_size), pygame.SRCALPHA)
obstacle.fill((0, 255, 0, 180))
pygame.draw.circle(obstacle, (0, 0, 0, 0), (player_size // 2, player_size // 2), player_size // 2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    # Sync rect with position
    player_rect.center = player_pos

    # Draw
    screen.blit(player, player_rect)
    screen.blit(obstacle, (640 - player_size // 2, 360 - player_size // 2))

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
