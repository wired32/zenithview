import random, time
import zenithview as display

def quick_sort(arr, dp: display.Display, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        pi = partition(arr, dp, low, high)
        dp.update(arr)
        quick_sort(arr, dp, low, pi - 1)  # Sort elements before partition
        quick_sort(arr, dp, pi + 1, high)  # Sort elements after partition
        
    time.sleep(0.01)
    return arr

def partition(arr, dp: display.Display, low, high):
    pivot = arr[high]
    i = low - 1 
    
    for j in range(low, high):
        if arr[j] < pivot:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]

    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

width, height = 1000, 500

visual = display.Display(
    width=width,
    height=height,
    sonification=True,
    soundDuration=0.005,
    algorithmName="Quick Sort",
    caption="Quick Sort Visualization",
)

arr = [i for i in range(500)]
random.shuffle(arr)

sorted_arr = quick_sort(arr, visual)

visual.release(sorted_arr)

print(f"Array sorted in {visual.finishTime} seconds")
