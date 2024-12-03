import random, time
from zenithview import display
import logging

def insertion_sort(arr, dp: display.Display):
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        # Move elements of arr[0..i-1], that are greater than key, to one position ahead
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
        dp.update(arr)
        time.sleep(0.001)
    dp.release(arr)
    return arr

width, height = 1000, 500

visual = display.Display(width, height, loggingLevel=logging.DEBUG, soundDuration=0.005, sonification=True)

cap = int(height - height / 10)
arr = [random.randint(0, cap) for i in range(500)]
random.shuffle(arr)

visual.preprocess(arr)

sorted_arr = insertion_sort(arr, visual)
print(f"Array sorted in {visual.finishTime} seconds")