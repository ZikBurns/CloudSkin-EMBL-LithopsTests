import math
import time
import json

def cold_pred(functions):
    duration=0.0208*functions + 5.2570
    return duration

def warm_pred(functions):
    duration = 0.0081 * functions + 0.0978
    return duration

def batch_pred(batch_size):
    duration = 0.1945 * batch_size - 0.1430
    return duration

MAX_FUNCTIONS = 950
num_images_list = [500, 1400, 8000, 20000, 50000, 80000, 150000, 300000, 1000000]
batch_size = 1
for num_images in num_images_list:
    start = time.time()
    all_combinations = []
    chunks = (num_images - 1) / 1
    chunks = math.ceil(chunks)
    config = {
        "cold": 1,
        "warm": 1,
        "warm_repetitions": chunks,
        "estimated_duration": cold_pred(1) + warm_pred(1) * chunks + (chunks+1)*batch_pred(1)
    }
    all_combinations.append(config)
    for cold_functions in range(100,MAX_FUNCTIONS+1,100):
        warm_functions = cold_functions
        chunks = (num_images-cold_functions) / warm_functions
        chunks = math.ceil(chunks)
        cold_duration = cold_pred(cold_functions)
        warm_duration = warm_pred(warm_functions)
        config={
            "cold":cold_functions,
            "warm":warm_functions,
            "warm_repetitions":chunks,
            "estimated_duration":cold_duration+warm_duration*chunks + (chunks+1)*batch_pred(1)
        }
        all_combinations.append(config)
    # maxDuration = max(all_combinations, key=lambda x:x['duration'])
    # print(maxDuration)
    minDuration = min(all_combinations, key=lambda x:x['estimated_duration'])
    solution = f"{minDuration['cold']} cold functions + {minDuration['warm']} warm functions x {minDuration['warm_repetitions']} times. Estimated duration: {round(minDuration['estimated_duration'])} seconds."
    end = time.time()
    print(f"Most optimal configuration for dataset of {num_images} images. {solution} (Estimation took {round((end-start)*1000, 2)} ms) ")


# with open('predictions.json', 'w') as f:
#     json.dump(all_combinations, f,indent=4 )
