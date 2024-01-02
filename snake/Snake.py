import pygame
import sys
import random

# Initialisation de Pygame
pygame.init()

# Paramètres du jeu
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
FPS = 10

# Couleurs
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# États du jeu
WAITING_TO_START = 0
CHOOSING_DIFFICULTY = 1
IN_GAME = 2
GAME_OVER = 3

# Initialisation de la fenêtre de jeu
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Chargez l'image originale de la pomme
apple_original = pygame.image.load("2.png")

# Redimensionnez l'image pour qu'elle ait la même taille qu'une case du jeu
apple_image = pygame.transform.scale(apple_original, (GRID_SIZE, GRID_SIZE))

# Fonction pour dessiner le serpent
def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# Modifiez la fonction draw_apple pour utiliser l'image redimensionnée
def draw_apple(apple):
    screen.blit(apple_image, (apple[0] * GRID_SIZE, apple[1] * GRID_SIZE))

# Fonction pour dessiner le terrain
def draw_grid():
    screen.fill(BLACK)
    for i in range(WIDTH // GRID_SIZE):
        for j in range(HEIGHT // GRID_SIZE):
            pygame.draw.rect(screen, BLACK, (i * GRID_SIZE, j * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

# Fonction pour afficher le score
def show_score(score):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Fonction pour afficher le message d'invitation
def show_start_message():
    font = pygame.font.Font(None, 36)
    text = font.render("Appuyez sur Espace pour commencer", True, WHITE)
    screen.blit(text, (WIDTH // 6, HEIGHT // 2))
    pygame.display.flip()

# Fonction pour choisir le niveau de difficulté
def choose_difficulty():
    font = pygame.font.Font(None, 36)
    text = font.render("Choisissez le niveau de difficulté :", True, WHITE)
    easy_text = font.render("Facile (5 de vitesse)", True, WHITE)
    medium_text = font.render("Moyen (10 de vitesse)", True, WHITE)
    hard_text = font.render("Difficile (15 de vitesse)", True, WHITE)

    selected_difficulty = 1  # 1 pour Facile, 2 pour Moyen, 3 pour Difficile

    while True:
        screen.fill((0, 0, 0))
        screen.blit(text, (WIDTH // 6, HEIGHT // 4))
        screen.blit(easy_text, (WIDTH // 6, HEIGHT // 2 - 20))
        screen.blit(medium_text, (WIDTH // 6, HEIGHT // 2 + 30))
        screen.blit(hard_text, (WIDTH // 6, HEIGHT // 2 + 80))

        pygame.draw.rect(
            screen,
            WHITE,
            (
                WIDTH // 6 - 10,
                HEIGHT // 2 - 25 + (selected_difficulty - 1) * 50,
                WIDTH // 2 + 20,
                40,
            ),
            2,
        )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_difficulty = max(1, selected_difficulty - 1)
                elif event.key == pygame.K_DOWN:
                    selected_difficulty = min(3, selected_difficulty + 1)
                elif event.key == pygame.K_SPACE:
                    return selected_difficulty * 5

# Fonction pour afficher le message de fin de jeu
def show_game_over_message(score):
    font_big = pygame.font.Font(None, 72)
    font_small = pygame.font.Font(None, 36)
    game_over_text = font_big.render("Game Over", True, WHITE)
    score_text = font_small.render(f"Score: {score}", True, WHITE)
    message_text = font_small.render("Appuyez sur Espace pour recommencer", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 6, HEIGHT // 4))
    screen.blit(score_text, (WIDTH // 3, HEIGHT // 2))
    screen.blit(message_text, (WIDTH // 6, HEIGHT // 2 + 50))
    pygame.display.flip()

# Fonction pour gérer la fin du jeu
def game_over(score):
    show_game_over_message(score)

    waiting = True

    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return True

        pygame.display.flip()

    return False

# Fonction principale du jeu
def main():
    game_state = WAITING_TO_START
    speed = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if game_state == WAITING_TO_START:
            show_start_message()
            game_state = CHOOSING_DIFFICULTY

        elif game_state == CHOOSING_DIFFICULTY:
            speed = choose_difficulty()
            game_state = IN_GAME

        elif game_state == IN_GAME:
            clock = pygame.time.Clock()

            # Position initiale du serpent
            snake = [(5, 5)]
            direction = (1, 0)  # Déplacement initial vers la droite

            # Position initiale de la pomme
            apple = (random.randint(0, WIDTH // GRID_SIZE - 1), random.randint(0, HEIGHT // GRID_SIZE - 1))

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP and direction != (0, 1):
                            direction = (0, -1)
                        elif event.key == pygame.K_DOWN and direction != (0, -1):
                            direction = (0, 1)
                        elif event.key == pygame.K_LEFT and direction != (1, 0):
                            direction = (-1, 0)
                        elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                            direction = (1, 0)

                # Mise à jour de la position du serpent
                new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
                snake.insert(0, new_head)

                # Vérification des collisions
                if new_head == apple:
                    apple = (random.randint(0, WIDTH // GRID_SIZE - 1), random.randint(0, HEIGHT // GRID_SIZE - 1))
                else:
                    snake.pop()

                if (
                    new_head[0] < 0
                    or new_head[0] >= WIDTH // GRID_SIZE
                    or new_head[1] < 0
                    or new_head[1] >= HEIGHT // GRID_SIZE
                    or new_head in snake[1:]
                ):
                    game_state = GAME_OVER
                    break

                # Dessin de l'écran
                draw_grid()
                draw_snake(snake)
                draw_apple(apple)
                show_score(len(snake) - 1)
                pygame.display.flip()

                clock.tick(speed)

        elif game_state == GAME_OVER:
            if not game_over(len(snake) - 1):
                pygame.quit()
                sys.exit()

            game_state = WAITING_TO_START


if __name__ == "__main__":
    main()
