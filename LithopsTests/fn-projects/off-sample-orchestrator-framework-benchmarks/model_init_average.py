import json
import os

# Directory containing the JSON files (replace with your directory path)
main_directory = "benchmarks_3008/time_results_3_8_23"

# Function to calculate the average time_model_init for a folder
def calculate_average_for_folder(folder_path):
    # Initialize a list to store the individual averages
    individual_averages = []

    # Loop through the JSON files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            with open(os.path.join(folder_path, filename), "r") as file:
                data = json.load(file)
                if ("time_model_init" in data):
                    time_model_init_values = data["time_model_init"]
                    average_time_model_init = sum(time_model_init_values) / len(time_model_init_values)
                    individual_averages.append(average_time_model_init)

    # Calculate the average for the folder
    folder_average = sum(individual_averages) / len(individual_averages)

    return folder_average

# Create a dictionary to store folder names and their corresponding averages
folder_averages = {}

# Loop through the subdirectories (e.g., cold_50, cold_100, cold_200)
for folder_name in os.listdir(main_directory):
    folder_path = os.path.join(main_directory, folder_name)
    if os.path.isdir(folder_path):
        folder_average = calculate_average_for_folder(folder_path)
        folder_averages[folder_name] = folder_average

# Sort the folder averages from largest to smallest
sorted_folder_averages = dict(sorted(folder_averages.items(), key=lambda item: item[1], reverse=True))

warm_average=0
warm_count=0
cold_average=0
cold_count=0
# Print the sorted folder averages
for folder_name, average in sorted_folder_averages.items():
    print(f"Average time_model_init for {folder_name}: {average}")
    if "cold" in folder_name:
        cold_average=cold_average+average
        cold_count=cold_count+1
    elif "warm" in folder_name:
        warm_average=warm_average+average
        warm_count=warm_count+1
cold_average=cold_average / cold_count
warm_average=warm_average / warm_count
print("COLD AVERAGE:",cold_average)
print("WARM AVERAGE:",warm_average)