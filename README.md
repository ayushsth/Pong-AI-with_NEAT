# Pong-AI-with_NEAT
Pong Game with NEAT AI

In this project, the classic Pong Game has been enhanced with AI with the help of NEAT(NeuroEvolution of Augmenting Topologies) algorithm. The AI learns to control the paddle and hit the ball and constantly improve its performance through various generations.

## Features

-Classic Pong game developed with the help of Pygame.
-Paddle is controlled by AI which is trained with the help of NEAT Algorithm.
-Sound Effects of ball hitting the paddle.
-Checkpoint that saves and resumes the training process.

## Requirements

-Python
-Pygame
-NEAT-Python

### Installation

1) Clone this repository:
   https://github.com/ayushsth/Pong-AI-with_NEAT
   cd Pong-AI-with_NEAT

2) Install this:
   pip install pygame neat-python

### Running the Game

python pong_with_NEAT.py

Press P to Play Again
Press X to Quit

### Training AI

Uncomment this section in the code:
run_neat(config)

### Resume Training from Checkpoint

Uncomment this section and specify the checkpoint file:
run_neat(config, checkpoint_file='NEAT Checkpoints/neat-checkpoint-5')

### Things to consider
-Make sure NEAT-Python is installed.
-Sound effects are located in right folder.
-If training, the checkpoints are saved to correct folder.
