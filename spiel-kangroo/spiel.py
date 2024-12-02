import os
import pygame
import random
import time
 
# Einstellungen für das Spiel
class Settings:
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 800
    FPS = 60
    FILE_PATH = os.path.dirname(os.path.abspath(__file__))  # Pfad zur aktuellen Python-Datei
    IMAGE_PATH = os.path.join(FILE_PATH, "images")  # Der Ordner "images" befindet sich im gleichen Verzeichnis wie die Python-Datei
 
# Spieler-Klasse
class Player:
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path)  # Bild laden
        self.image = pygame.transform.scale(self.image, (40, 40))  # Bild skalieren
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.start_x = (Settings.WINDOW_WIDTH - self.width) // 2
        self.start_y = Settings.WINDOW_HEIGHT - self.height
        self.x = self.start_x
        self.y = self.start_y
        self.speed = 4
        self.sprint_speed = 8  # Sprintgeschwindigkeit
        self.sprint_duration = 0.2  # Dauer des Sprints (in Sekunden)
        self.last_sprint_time = 0  # Zeitstempel für den letzten Sprint
        self.jump_speed = 12  # Geschwindigkeit des Sprungs nach oben
        self.is_jumping = False  # Status, ob der Spieler springt
 
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
 
    def move(self, keys):
        # Sprinten: Wenn Leertaste gedrückt wird, springe nach oben
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.is_jumping = True
            self.y -= self.jump_speed  # Sprung nach oben
            self.last_sprint_time = time.time()
 
        # Normale Bewegung nach links, rechts, oben, unten
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed
 
        # Sicherstellen, dass der Spieler innerhalb des Fensters bleibt
        self.x = max(0, min(Settings.WINDOW_WIDTH - self.width, self.x))
        self.y = max(0, min(Settings.WINDOW_HEIGHT - self.height, self.y))
 
        # Wenn der Sprung vorbei ist (nach einer kurzen Zeit), dann zurücksetzen
        if self.is_jumping and time.time() - self.last_sprint_time > self.sprint_duration:
            self.is_jumping = False
            self.y = max(0, self.y)  # Verhindere, dass der Spieler unter den Bildschirm fällt
 
    def reset_position(self):
        self.x = self.start_x
        self.y = self.start_y
 
# Klasse für bewegliche Hindernisse
class MovingObstacle:
    def __init__(self, image_path, x, y, speed_x, speed_y, size):
        self.image = pygame.image.load(image_path)  # Bild laden
        self.image = pygame.transform.scale(self.image, size)  # Bild skalieren
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = x
        self.y = y
        self.speed_x = speed_x  # Geschwindigkeit in x-Richtung
        self.speed_y = speed_y  # Geschwindigkeit in y-Richtung
 
    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
 
        # Wenn das Hindernis den Bildschirm verlässt, wird es auf die andere Seite gesetzt
        if self.x < -self.width:
            self.x = Settings.WINDOW_WIDTH
        elif self.x > Settings.WINDOW_WIDTH:
            self.x = -self.width
 
        if self.y < -self.height:
            self.y = Settings.WINDOW_HEIGHT
        elif self.y > Settings.WINDOW_HEIGHT:
            self.y = -self.height
 
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
 
    def check_collision(self, player):
        return self.x < player.x + player.width and self.x + self.width > player.x and self.y < player.y + player.height and self.y + self.height > player.y
 
# Dunkle Überlagerung anzeigen, wenn das Spiel pausiert ist
def draw_dark_overlay(screen):
    overlay = pygame.Surface((Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT))  
    overlay.set_alpha(150)  # Transparenz für das Overlay
    overlay.fill((0, 0, 0))  # Schwarze Farbe
    screen.blit(overlay, (0, 0))
 
# Punktestand anzeigen
def display_score(screen, score):
    font = pygame.font.Font(None, 36)  
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))  
    screen.blit(score_text, (10, 10))
 
# Hauptfunktion
def main():
    os.environ["SDL_VIDEO_WINDOW_POS"] = "10, 50"
    pygame.init()
 
    screen = pygame.display.set_mode((Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT))
    pygame.display.set_caption("Zombie Crossing Game")
    clock = pygame.time.Clock()
 
    # Hindernisse und Hintergrund laden
    obstacles = [
        MovingObstacle(os.path.join(Settings.IMAGE_PATH, "car1.1.png"), 250, 50, -3, 0, (80, 60)),
        MovingObstacle(os.path.join(Settings.IMAGE_PATH, "car1.1.png"), -350, 50, -3, 0, (80, 60)),
        MovingObstacle(os.path.join(Settings.IMAGE_PATH, "car1.1.png"), 550, 50, -3, 0, (80, 60)),
        MovingObstacle(os.path.join(Settings.IMAGE_PATH, "truck.png"), 600, 220, -4, 0, (100, 100)),
        MovingObstacle(os.path.join(Settings.IMAGE_PATH, "car3.1.png"), 200, 250, -4, 0, (80, 60)),
        MovingObstacle(os.path.join(Settings.IMAGE_PATH, "car1.1.png"), 400, 480, -4, 0, (80, 60)),
        MovingObstacle(os.path.join(Settings.IMAGE_PATH, "car3.1.png"), 830, 125, -8, 0, (80, 60)),
        MovingObstacle(os.path.join(Settings.IMAGE_PATH, "car3.1.png"), 200, 550, -4, 0, (80, 60)),
        MovingObstacle(os.path.join(Settings.IMAGE_PATH, "truck.png"), 600, 530, -4, 0, (100, 100)),
        MovingObstacle(os.path.join(Settings.IMAGE_PATH, "car1.1.png"), -350, 600, -5, 0, (80, 60)),
        MovingObstacle(os.path.join(Settings.IMAGE_PATH, "car1.1.png"), 300, 600, -5, 0, (80, 60)),
    ]
 
    background_image = pygame.image.load(os.path.join(Settings.IMAGE_PATH, "Background.1.png")).convert()
    background_image = pygame.transform.scale(background_image, (Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT))
 
    player = Player(os.path.join(Settings.IMAGE_PATH, "kangroo.png"))
 
    paused = False
    running = True
    esc_last_pressed = 0
    score = 0  
 
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_ESCAPE:
                    now = time.time()
                    if now - esc_last_pressed < 0.5:
                        running = False
                    esc_last_pressed = now
 
        screen.blit(background_image, (0, 0))
 
        if not paused:
            keys = pygame.key.get_pressed()
            player.move(keys)
            player.draw(screen)
 
            if player.y <= 0:
                player.reset_position()
                score += 10  
                print("Neue Runde!")
                player.speed += 1  
 
            # Alle Hindernisse bewegen sich rückwärts
            for obstacle in obstacles:
                obstacle.move()
                obstacle.draw(screen)
 
                if obstacle.check_collision(player):
                    print("Kollision!")
                    player.reset_position()
 
            display_score(screen, score)
 
        else:
            draw_dark_overlay(screen)
 
        pygame.display.flip()
        clock.tick(Settings.FPS)
 
    pygame.quit()
 
if __name__ == "__main__":
    main() 