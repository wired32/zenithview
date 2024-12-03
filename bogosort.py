# this is stupid

from zenithview import display
import random, time

def bogo_sort(visual: display.Display, arr: list):
    while True:
        random.shuffle(arr)
        visual.update(arr)
        if sorted(arr) == arr:
            break

    return arr


width, height = 1000, 500

visual = display.Display(width, height, sonification=True, soundDuration=0.1)

cap = int(height - height / 10)
arr = [random.randint(0, cap) for i in range(50)]
random.shuffle(arr)

sorted_arr = bogo_sort(visual, arr)

visual.release(sorted_arr)

print(f"Array sorted in {visual.finishTime} seconds")
