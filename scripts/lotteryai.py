# Import necessary libraries
import numpy as np
import json
import tensorflow as tf
from tensorflow import keras
from keras import layers
from datetime import datetime
from dateutil.relativedelta import relativedelta
from scripts.scrapedata import scrape_date_from
# from art import text2art

# Function to print the introduction of the program
def print_intro():
    # Generate ASCII art with the text "LotteryAi"
    # ascii_art = text2art("LotteryAi")
    # Print the introduction and ASCII art
    print("============================================================")
    print("LotteryAi")
    print("Created by: Maracas")
    print("Licence : MIT License")
    print("Support my work:")
    print("BTC: 1A61DMroJQ246Sw7YXFUA1Ai4uNp6Yitce")
    print("ETH: 0x4830332B68e88b48fA2Ee5ab21D3a5A1D5E8cC48")
    print("BNB: bnb1wfwf8z03d7dz9ur453khxhg2ez64nuy5ymdx0v")
    print("============================================================")
    # print(ascii_art)
    print("Lottery prediction artificial intelligence")


def get_area_name(area_code):
    with open('data/area_code.json') as file:
        area_codes = json.load(file)
    return area_codes[area_code]

def load_lotteries_for(area_code):
    with open('data/output.json') as file:
        lot_data = json.load(file)

    lotteries = [item['title'] for item in lot_data if item['area'] == get_area_name(area_code)]
    ret_val = list(set(lotteries))
    # data = np.array(lotteries)   
    return ret_val

def load_data_for(area, title):
    with open('data/output.json') as file:
        lot_data = json.load(file)

    nums_list = [list(map(int, item['nums'])) for item in lot_data if item['area'] == get_area_name(area) and item['title'] == title]
    return np.array(nums_list)  

# Function to load data from a file and preprocess it
def load_data(area, title):    
    data = load_data_for(area, title)   
    # Replace all -1 values with 0
    data[data == -1] = 0
    # Split data into training and validation sets
    train_data = data[:int(0.8*len(data))]
    val_data = data[int(0.8*len(data)):]
    # Get the maximum value in the data
    max_value = np.max(data)
    return train_data, val_data, max_value

# Function to create the model
def create_model(num_features, max_value):
    # Create a sequential model
    model = keras.Sequential()
    # Add an Embedding layer, LSTM layer, and Dense layer to the model
    model.add(layers.Embedding(input_dim=max_value+1, output_dim=64))
    model.add(layers.LSTM(256))
    model.add(layers.Dense(num_features, activation='softmax'))
    # Compile the model with categorical crossentropy loss, adam optimizer, and accuracy metric
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

# Function to train the model
def train_model(model, train_data, val_data):
    # Fit the model on the training data and validate on the validation data for 100 epochs
    history = model.fit(train_data, train_data, validation_data=(val_data, val_data), epochs=100)

# Function to predict numbers using the trained model
def predict_numbers(model, val_data, num_features):
    # Predict on the validation data using the model
    predictions = model.predict(val_data)
    # Get the indices of the top 'num_features' predictions for each sample in validation data
    indices = np.argsort(predictions, axis=1)[:, -num_features:]
    # Get the predicted numbers using these indices from validation data
    predicted_numbers = np.take_along_axis(val_data, indices, axis=1)
    return predicted_numbers

# Function to print the predicted numbers
def print_predicted_numbers(predicted_numbers):
   # Print a separator line and "Predicted Numbers:"
   print("============================================================")
   print("Predicted Numbers:")
   # Print only the first row of predicted numbers
   print(', '.join(map(str, predicted_numbers[0])))
   print("============================================================")

def check_update():
    with open('data/output.json') as file:
        lot_data = json.load(file)
    
    max_date = max(lot_data, key=lambda x: datetime.strptime(x['date'], "%A, %B %d, %Y"))['date']
    latest_date = datetime.strptime(max_date, "%A, %B %d, %Y")
    current_date = datetime.now()
    return (current_date - latest_date).days, latest_date.strftime("%A, %B %d, %Y")

def update_database(latest_date):
    start_date = datetime.strptime(latest_date, "%A, %B %d, %Y") + relativedelta(days=1)
    end_date = datetime.now()

    with open('data/output.json') as file:
        allData = json.load(file)

    with open('data/area_code.json') as file:
        area_codes = json.load(file)      

    for dt in range(int((end_date - start_date).days) + 1):
        current_date = start_date + relativedelta(days=dt)
        for code in area_codes:
            result = scrape_date_from(code, area_codes[code], current_date.year, 
                                      current_date.month, current_date.day)
            allData = np.concatenate((allData, result))
            allData = allData.tolist()
    
    with open('data/output.json', 'w') as file:
        json.dump(allData, file)

    return start_date

def get_prediction(area_code, title):
    # Print introduction of program 
   print_intro()
   
   # Load and preprocess data 
   train_data, val_data, max_value = load_data(area_code, title)
   
   # Get number of features from training data 
   num_features = train_data.shape[1]
   
   # Create and compile model 
   model = create_model(num_features, max_value)
   
   # Train model 
   train_model(model, train_data, val_data)
   
   # Predict numbers using trained model 
   predicted_numbers = predict_numbers(model, val_data, num_features)
   
   # Print predicted numbers 
   return map(str, predicted_numbers[0])


# Main function to run everything   
def main():
   # Print introduction of program 
   print_intro()
   
   # Load and preprocess data 
   train_data, val_data, max_value = load_data('Arizona', 'Pick 3')
#    print(max_value)
#    load_data('Arizona', 'Pick 3')
   
   # Get number of features from training data 
   num_features = train_data.shape[1]
   
   # Create and compile model 
   model = create_model(num_features, max_value)
   
   # Train model 
   train_model(model, train_data, val_data)
   
   # Predict numbers using trained model 
   predicted_numbers = predict_numbers(model, val_data, num_features)
   
   # Print predicted numbers 
   print_predicted_numbers(predicted_numbers)

# Run main function if this script is run directly (not imported as a module)
if __name__ == "__main__":
   main()