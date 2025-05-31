# Pong-AI-with_NEAT
Pong Game with NEAT AI

In this project, the classic Pong Game has been enhanced with AI with the help of NEAT(NeuroEvolution of Augmenting Topologies) algorithm. The AI learns to control the paddle and hit the ball and constantly improve its performance through various generations.

## Features

-Classic Pong game developed with the help of Pygame.<br>
-Paddle is controlled by AI which is trained with the help of NEAT Algorithm.<br>
-Sound Effects of ball hitting the paddle.<br>
-Checkpoint that saves and resumes the training process.<br>

## Requirements

-Python<br>
-Pygame<br>
-NEAT-Python<br>

### Installation

1) Clone this repository:<br>
```bash
   git clone https://github.com/ayushsth/Pong-AI-with_NEAT.git
   cd Pong-AI-with_NEAT
```

2) Install this:<br>
```bash
   pip install pygame neat-python
```

### Running the Game
```bash
python pong_with_NEAT.py
```

<br>
Press P to Play Again<br>
Press X to Quit

### Training AI

Uncomment this section in the code:<br>
```bash
run_neat(config)
```

### Resume Training from Checkpoint

Uncomment this section and specify the checkpoint file:<br>
```bash
run_neat(config, checkpoint_file='NEAT Checkpoints/neat-checkpoint-5')
```

### Things to consider
-Make sure NEAT-Python is installed.<br>
-Sound effects are located in right folder.<br>
-If training, the checkpoints are saved to correct folder.
