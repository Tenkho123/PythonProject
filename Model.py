import torch
import torch.nn as nn
import torch.optim as optim
import os

class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = torch.relu(self.linear1(x))
        x = self.linear2(x)
        return x

    def save(self, file_name="model.pth"):
        model_folder_path = "./model"
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)
        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)

class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, done):
        # Convert inputs to tensors
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        
        # Ensure `done` is a tensor or a batched input
        if isinstance(done, int):  # If `done` is scalar, wrap it in a list
            done = [done]
        done = torch.tensor(done, dtype=torch.bool)
    
        # Handle single-sample case (add batch dimension if needed)
        if len(state.shape) == 1:
            state = state.unsqueeze(0)
            next_state = next_state.unsqueeze(0)
            action = action.unsqueeze(0)
            reward = reward.unsqueeze(0)
            done = done.unsqueeze(0)
    
        pred = self.model(state)
        target = pred.clone()
    
        for idx in range(len(done)):
            action_idx = action[idx].item()  # Get the index of the chosen action
            Q_new = reward[idx].item()  # Immediate reward for the action
            
            if not done[idx]:  # Add discounted future reward if not done
                Q_new += self.gamma * torch.max(self.model(next_state[idx])).item()
            
            target[idx, action_idx] = Q_new  # Update target value for chosen action
    
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()
        self.optimizer.step()
