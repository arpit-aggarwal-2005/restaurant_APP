import random
import pandas as pd
import numpy as np

# Generating synthetic dataset
def generate_dataset(num_instances):
    data = {
        'experience': np.random.randint(0, 21, size=num_instances),
        'written_score': np.random.randint(0, 101, size=num_instances),
        'interview_score': np.random.randint(0, 101, size=num_instances),
        'leaves_last_year': np.random.randint(0, 21, size=num_instances),
        'increment': np.random.randint(5000, 50001, size=num_instances)
    }
    return pd.DataFrame(data)

# Splitting dataset into training, testing, and validation sets
def split_dataset(dataset):
    train_data, test_data, val_data = np.split(dataset.sample(frac=1), [int(.7*len(dataset)), int(.9*len(dataset))])
    return train_data, test_data, val_data

# Calculate Euclidean distance between two data points
def euclidean_distance(point1, point2):
    return np.linalg.norm(point1 - point2)

# Implement KNN algorithm
def knn(train_data, test_instance, k):
    distances = []
    for _, train_instance in train_data.iterrows():
        dist = euclidean_distance(train_instance[:-1], test_instance[:-1])
        distances.append((train_instance, dist))
    distances.sort(key=lambda x: x[1])
    neighbors = [item[0][-1] for item in distances[:k]]
    return sum(neighbors) / k

# Calculate RMSE
def calculate_rmse(predictions, actual_values):
    squared_error = np.square(np.subtract(predictions, actual_values)).mean()
    rmse = np.sqrt(squared_error)
    return rmse

# Generate dataset
dataset = generate_dataset(10000)

# Split dataset
train_data, test_data, val_data = split_dataset(dataset)

# Test KNN with some test instances
k_value = 5
predictions = [knn(train_data, test_instance, k_value) for _, test_instance in test_data.iterrows()]

# Calculate RMSE
actual_values = test_data['increment']
rmse = calculate_rmse(predictions, actual_values)

print("RMSE:", rmse)
