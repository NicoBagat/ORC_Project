# PYTHON LIBRARIES
import torch
import torch.nn as nn

class SP_NNmodel(nn.Module):
    """Single Pendulum NN"""
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(2, 64), nn.ReLU(),    # Input layer
            nn.Linear(64, 64), nn.ReLU(),   # Hidden layers
            nn.Linear(64, 1)                # Output layer
        )
    
    def forwars(self, x):
        return self.net(x)

class DP_NNmodel(nn.Module):
    """Double Pendulum NN"""
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(4, 128), nn.ReLU(),   # Input layer
            nn.Linear(128, 128), nn.ReLU(), # Hidden layers
            nn.Linear(128, 1)               # Output layer
        )
    
    def forward(self, x):
        return self.net(x)