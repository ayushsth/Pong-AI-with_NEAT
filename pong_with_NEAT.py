import pygame
import sys
import neat
import math
import os
import pickle
import random
from pygame import mixer

os.chdir(os.path.dirname(os.path.abspath(__file__)))
mixer.init()
pygame.init()
clock = pygame.time.Clock()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

class PongGame:
    def __init__(self, screen):
        self.screen = screen
        self.score = 0
        self.game_over = False
        self.platform = pygame.Rect(WIDTH / 2 - 50, HEIGHT - 100, 100, 8)
        self.ball = pygame.Rect(WIDTH / 2 - 10, HEIGHT - 100 - 8 - 10 - 2, 20, 20)
        self.ball_speed_x = 0
        self.ball_speed_y = 0
        self.bounce_sfx = pygame.mixer.Sound("paddle_sound.wav")
        self.reset_ball()

    def reset_ball(self):
        self.score = 0
        self.ball.x = WIDTH / 2 - 10
        self.ball.y = HEIGHT - 100 - 8 - 10 - 2

        speed = 7
        
        angle_deg = random.uniform(225, 315)  # Angle between 225° (down-left) and 315° (down-right)
        angle_rad = math.radians(angle_deg)

        self.ball_speed_x = speed * math.cos(angle_rad)
        self.ball_speed_y = speed * math.sin(angle_rad)


    def reset_platform(self):
        self.platform.x = WIDTH / 2 - 50

    def text_on_screen(self):
        game_over = pygame.font.SysFont('times new roman', 50)
        game_over_surface = game_over.render('Game Over', True, RED)
        game_over_rect = game_over_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2))

        scoreboard = pygame.font.SysFont('times new roman', 40)
        scoreboard_surface = scoreboard.render(f'Score: {self.score}', True, WHITE)
        scoreboard_rect = scoreboard_surface.get_rect(center=(WIDTH / 2, 50))

        play_again = pygame.font.SysFont('times new roman', 30)
        play_again_surface = play_again.render('Press P to Play Again!!! Press X to QUIT!!!', True, RED)
        play_again_rect = play_again_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 50))

        self.screen.blit(scoreboard_surface, scoreboard_rect)

        if self.ball.y + self.ball.height >= HEIGHT:
            self.game_over = True
            self.ball_speed_x = 0
            self.ball_speed_y = 0
            self.screen.blit(game_over_surface, game_over_rect)
            self.screen.blit(play_again_surface, play_again_rect)

    def update_ball(self):
        if self.game_over:
            return
            
        self.ball.x += self.ball_speed_x
        self.ball.y += self.ball_speed_y
        
        if self.ball.x <= 0:
            self.ball.x = 0
            self.ball_speed_x *= -1
            self.bounce_sfx.play()

        elif self.ball.x + self.ball.width >= WIDTH:
            self.ball.x = WIDTH - self.ball.width
            self.ball_speed_x *= -1
            self.bounce_sfx.play()


        if self.ball.y <= 0:
            self.ball_speed_y *= -1
            self.bounce_sfx.play()

        if self.ball.y + self.ball.height >=HEIGHT:
            self.game_over=True
            self.ball_speed_x=0
            self.ball_speed_y=0
            return


        MAX_BOUNCE_ANGLE = math.radians(45)
        
        MIN_VERTICAL_SPEED = 3


        if self.platform.colliderect(self.ball) and self.ball_speed_y > 0:
            offset = (self.ball.centerx - self.platform.centerx) / (self.platform.width / 2)
            random_factor = random.uniform(-0.3, 0.3)  # Add randomness
            bounce_angle = offset * MAX_BOUNCE_ANGLE + random_factor

            speed = math.hypot(self.ball_speed_x, self.ball_speed_y)
            self.ball_speed_x = speed * math.sin(bounce_angle)
            self.ball_speed_y = -abs(speed * math.cos(bounce_angle))

            if abs(self.ball_speed_y) < MIN_VERTICAL_SPEED:
                vertical_sign = -1 if self.ball_speed_y < 0 else 1
                self.ball_speed_y = vertical_sign * MIN_VERTICAL_SPEED

                self.ball_speed_x = math.copysign(math.sqrt(max(speed**2 - self.ball_speed_y**2, 0)), self.ball_speed_x)

            self.ball.bottom = self.platform.top - 1
            self.score += 1
            self.bounce_sfx.play()


    def handle_events(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_x]:
            pygame.quit()
            sys.exit()

    def train_ai(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            output = net.activate((self.platform.x, self.ball.x, self.ball.y))
            if output[0] > 0.5:
                self.platform.x += 5
            elif output[0] < 0.5:
                self.platform.x -= 5

            self.platform.x = max(0, min(self.platform.x, WIDTH - self.platform.width))

            self.update_ball()

            if self.ball.y + self.ball.height >= HEIGHT:
                self.calculate_fitness(genome)
                break

            self.text_on_screen()
            self.draw()
            pygame.display.flip()
            clock.tick(60)

    def calculate_fitness(self, genome):
        genome.fitness += self.score

    def draw(self):
        self.screen.fill(BLACK)
        pygame.draw.rect(self.screen, WHITE, self.platform)
        pygame.draw.circle(self.screen, RED, (self.ball.x + self.ball.width // 2, self.ball.y + self.ball.height // 2), self.ball.width // 2)
        self.text_on_screen()

    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.game_over:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            self.reset_ball()
                            self.reset_platform()
                            self.game_over = False
                        elif event.key == pygame.K_x:
                            pygame.quit()
                            sys.exit()

            if not self.game_over:
                self.update_ball()
                self.handle_events()

            self.text_on_screen()
            self.draw()
            pygame.display.flip()
            clock.tick(60)

# Function to evaluate genomes and save the best one using pickle
def eval_genomes(genomes, config):
    width, height = 800, 600
    window = pygame.display.set_mode((width, height))

    best_genome = None
    best_score = -float("inf")

    for _, genome in genomes:
        genome.fitness = 0
        game = PongGame(window)
        game.train_ai(genome, config)
        if genome.fitness > best_score:
            best_score = genome.fitness
            best_genome = genome

    # Save the best genome to a file using pickle
    with open("best_genome.pkl", "wb") as f:
        pickle.dump(best_genome, f)
        print(f"Saved best genome with score: {best_score}")

def run_neat(config, checkpoint_file=None):
    if checkpoint_file and os.path.exists(checkpoint_file):
        print(f"Resuming from checkpoint: {checkpoint_file}")
        p = neat.Checkpointer.restore_checkpoint(checkpoint_file)
    else:
        p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(generation_interval=1, filename_prefix="NEAT Checkpoints/neat-checkpoint-"))

    p.run(eval_genomes, 50)


def test_ai(config, genome_file="best_genome.pkl"):
    if not os.path.exists(genome_file):
        print(f"Error: Genome file '{genome_file}' not found.")
        return

    with open(genome_file, "rb") as f:
        best_genome = pickle.load(f)

    if not best_genome or not best_genome.connections:
        print("Error: The genome is invalid or not properly trained.")
        return

    net = neat.nn.FeedForwardNetwork.create(best_genome, config)

    window = pygame.display.set_mode((WIDTH, HEIGHT))
    game = PongGame(window)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not game.game_over:
            output = net.activate((game.platform.x, game.ball.x, game.ball.y))
            if output[0] > 0.5:
                game.platform.x += 5
            elif output[0] < 0.5:
                game.platform.x -= 5

            game.platform.x = max(0, min(game.platform.x, WIDTH - game.platform.width))
            game.update_ball()
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_p]:
                game.reset_ball()
                game.reset_platform()
                game.game_over = False
            elif keys[pygame.K_x]:
                pygame.quit()
                sys.exit()

        game.text_on_screen()
        game.draw()
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    # OPTION 1: Train from 
    
    # run_neat(config)

    # OPTION 2: Resume training from checkpoint

    # run_neat(config, checkpoint_file='NEAT Checkpoints/neat-checkpoint-5')

    # OPTION 3: Extract and save best genome

    # checkpoint = neat.Checkpointer.restore_checkpoint('NEAT Checkpoints/neat-checkpoint-5')
    # best_genome = checkpoint.best_genome
    # if best_genome:
    #     with open("best_genome.pkl", "wb") as f:
    #         pickle.dump(best_genome, f)
    #     print("Best genome saved to best_genome.pkl")
    # else:
    #     print("No best genome found in checkpoint.")

    # OPTION 4: Test saved best genome
    
    test_ai(config)