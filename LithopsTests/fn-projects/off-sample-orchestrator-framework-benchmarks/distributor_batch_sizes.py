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
num_images = 50000
batch_sizes = [1, 2, 4, 8, 16, 32, 64, 128, 256]
start = time.time()
all_combinations = []
for batch_size in batch_sizes:
    estimated_time_batch = batch_pred(batch_size)
    num_batches = math.ceil(num_images / batch_size)
    for cold_functions in range(50,MAX_FUNCTIONS+1,50):
        warm_functions = cold_functions
        chunks = (num_batches-cold_functions) / warm_functions
        chunks = math.ceil(chunks)
        if chunks ==0:
            break
        cold_duration = cold_pred(cold_functions)
        warm_duration = warm_pred(warm_functions)
        config={
            "cold":cold_functions,
            "warm":warm_functions,
            "warm_repetitions":chunks,
            "batch_size": batch_size,
            "estimated_duration":cold_duration+warm_duration*chunks + estimated_time_batch * (num_batches / cold_functions)
        }
        all_combinations.append(config)
minDuration = min(all_combinations, key=lambda x:x['estimated_duration'])
solution = f"Batch size: {minDuration['batch_size']}. {minDuration['cold']} cold functions + {minDuration['warm']} warm functions x {minDuration['warm_repetitions']} times. Estimated duration: {round(minDuration['estimated_duration'])} seconds."
end = time.time()
print(f"Most optimal configuration for dataset of {num_images} images. {solution} (Estimation took {round((end-start)*1000, 2)} ms) ")


# with open('predictions.json', 'w') as f:
#     json.dump(all_combinations, f,indent=4 )
