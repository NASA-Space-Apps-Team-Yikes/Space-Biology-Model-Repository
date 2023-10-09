'''
PyTorch-based Transfer Learning Model for Space Biology Data

This script connects to an Amazon RDS PostgreSQL database to fetch data from the 'c3h_hej_data' table.
It focuses on predicting several gene expressions based on the 'bsl_0days_avg' field. The predicted fields include:
- flt_25days_avg
- flt_75days_avg
- gc_25days_avg
- gc_75days_avg
- viv_25days_avg
- viv_75days_avg

The data is first fetched from the database and preprocessed. It's then split into training, validation, and test datasets.
A feed-forward neural network model is then defined and trained using the training dataset.
Model performance is assessed during training using the validation set, and final evaluation is performed using the test set.

Requirements:
- PyTorch
- psycopg2
- sklearn
- matplotlib

Author: Doug Puccetti
Date: 10/08/2023
'''

import psycopg2
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Establish a connection to the database
def connect():
    # Attempting to establish a connection to the RDS PostgreSQL database
    try:
        conn = psycopg2.connect(host="model-zoo-space-apps.cqxs7dfl7szm.us-east-2.rds.amazonaws.com",
                                port="5432",
                                database="postgres",
                                user="",
                                password="")
        cursor = conn.cursor()
        print("Connected")
    except Exception as e:
        print("Connection failed: {}".format(e))  # Returns failure code
        return None, None  # If there's a failure, return None values

    return conn, cursor

# Fetch data from the specified table in the database
def fetch_data(cursor, table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    return cursor.fetchall()

def train_model(data):
    # Preprocess and Split Data
    # Extract input and output columns from the fetched data

    # Define a feed-forward neural network model structure
    class TransferModel(nn.Module):
        def __init__(self):
            super(TransferModel, self).__init__()
            # Define the layers and activation functions
            self.fc = nn.Sequential(
                nn.Linear(1, 64),  # Assuming bsl_0days_avg is 1-dimensional
                nn.ReLU(),
                nn.Linear(64, 128),
                nn.ReLU(),
                nn.Linear(128, 6)  # Output: flt_25days_avg, ..., viv_75days_avg
            )

        # Define the forward propagation of the model
        def forward(self, x):
            return self.fc(x)

    inputs = [item[1] for item in data]  # bsl_0days_avg values
    outputs = [item[2:] for item in data]  # Other column values

    # Convert inputs to a 2D array for pytorch and scikitlearn
    inputs = [[i] for i in inputs]

    # Normalize the data to have a mean of 0 and variance of 1
    input_scaler = StandardScaler()
    inputs = input_scaler.fit_transform(inputs)

    output_scaler = StandardScaler()
    outputs = output_scaler.fit_transform(outputs)


    # Split the data into training, validation, and test sets
    X_train, X_temp, y_train, y_temp = train_test_split(inputs, outputs, test_size=0.3, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

    # Convert the datasets into PyTorch tensors for compatibility with PyTorch
    X_train, y_train = torch.Tensor(X_train), torch.Tensor(y_train)
    X_val, y_val = torch.Tensor(X_val), torch.Tensor(y_val)
    X_test, y_test = torch.Tensor(X_test), torch.Tensor(y_test)

    # Define the Model Architecture

    model = TransferModel()
    # Define the loss function and optimizer for training
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    train_losses = []
    val_losses = []

    # Train the Model
    epochs = 100 # 100 is a good solid number as most deep learning models shouldnt need more than that to train.
    for epoch in range(epochs):
        # Training Phase
        model.train()
        optimizer.zero_grad()  # Reset gradients from previous iteration
        predictions = model(X_train)
        loss = criterion(predictions, y_train)
        loss.backward()  # Backpropagate the loss
        optimizer.step()  # Update the model weights

        # Validation Phase
        model.eval()
        with torch.no_grad():
            val_predictions = model(X_val)
            val_loss = criterion(val_predictions, y_val)
        print(f"Epoch {epoch+1}/{epochs} - Training Loss: {loss.item()} - Validation Loss: {val_loss.item()}")
        train_losses.append(loss.item())
        val_losses.append(val_loss.item())

    # Evaluate the Model
    model.eval()
    with torch.no_grad():
        test_predictions = model(X_test)
        # Calculate the Mean Squared Error on the test set to evaluate the model's performance
        test_loss = mean_squared_error(test_predictions.numpy(), y_test.numpy())
        print(f"Test Loss: {test_loss}")

    # Ploting the training data to show the model getting better over time
    plt.figure(figsize=(10, 6))
    plt.plot(train_losses, label="Training Loss", color="blue")
    plt.plot(val_losses, label="Validation Loss", color="red")
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.title("Training and Validation Loss over Epochs")
    plt.legend()
    plt.grid(True)
    plt.show()

    return model, input_scaler, output_scaler

def predict_new_data(bsl_value, model, input_scaler, output_scaler):
    # Preprocess the input value
    print("Predicting values...")
    bsl_value_scaled = input_scaler.transform([[bsl_value]])
    bsl_tensor = torch.Tensor(bsl_value_scaled)

    # Get predictions
    model.eval()
    with torch.no_grad():
        predictions = model(bsl_tensor)

    # Postprocess the predictions
    predicted_values = output_scaler.inverse_transform(predictions.numpy())
    return predicted_values[0]


if __name__ == '__main__':
    conn, cursor = connect()
    # data = fetch_data(cursor, "c3h_hej_data")
    data = fetch_data(cursor, "c57_6j_data")

    model, input_scaler, output_scaler = train_model(data)

    bsl_value = 9.352293386  # Replace with any value you want to test
    predicted_values = predict_new_data(bsl_value, model, input_scaler, output_scaler)
    print(f"Predicted values for bsl_0days_avg={bsl_value} are:")
    print(f"flt_25days_avg: {predicted_values[0]}")
    print(f"flt_75days_avg: {predicted_values[1]}")
    print(f"gc_25days_avg: {predicted_values[2]}")
    print(f"gc_75days_avg: {predicted_values[3]}")
    print(f"viv_25days_avg: {predicted_values[4]}")
    print(f"viv_75days_avg: {predicted_values[5]}")

    cursor.close()
    conn.close()