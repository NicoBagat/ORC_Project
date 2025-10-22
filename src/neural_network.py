import torch 
import torch.nn as nn
from src.utils import load_config

class NeuralNetwork(nn.Module):
    def __init__(self, nn_input, nn_hidden_dim, nn_output_dim, activation=nn.ReLU(), ub=1):
        
        def forward(self, x):
        
        def initialize_weights(self):
            
         @classmethod
         def from_config(cls, config_path):
             
             config=load_config(config_path)
             input_size = config["ocp"]