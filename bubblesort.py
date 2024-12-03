import random
from zenithview import display
import logging
import time

def bubble_sort(arr, dp: display.Display):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        dp.update(arr)
        time.sleep(0.01)
        if not swapped:
            break
    dp.release(arr)
    return arr

width, height = 1000, 500

visual = display.Display(
    width=width,
    height=height,
    loggingLevel=logging.DEBUG,
    soundDuration=0.005,
    sonification=False,
    caption="Bubble Sort",
    algorithmName="Bubble Sort",
    cutoffFrequency=440,
    attack=0.5,
    release=1.5,
)

arr = [random.randint(110, 440) for _ in range(100)]

visual.preprocess(arr)

sorted_arr = bubble_sort(arr, visual)
print(f"Array sorted in {visual.finishTime} seconds")

