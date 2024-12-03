from zenithview import Display
import random
import time

# define the cocktail shaker sort function
def cocktail_shaker_sort(array: list[int], display: Display):
    n = len(array)
    swapped = True

    while swapped:
        swapped = False
        # forward pass
        for i in range(0, n - 1):
            if array[i] > array[i + 1]:
                array[i], array[i + 1] = array[i + 1], array[i]
                swapped = True
            
            time.sleep(0.0005)  # control the speed of visualization
        display.update(array)  # update the display at each change

        if not swapped:
            break

        swapped = False
        # backward pass
        for i in range(n - 2, -1, -1):
            if array[i] > array[i + 1]:
                array[i], array[i + 1] = array[i + 1], array[i]
                swapped = True
            
            time.sleep(0.0005)  # control the speed of visualization
        display.update(array, inverseDelta=True)  # update the display at each change

    display.release(array)

    print(f"Sorted array: {array}")
    print(f"Sorting time: {display.finishTime} seconds")

# initialize the display
width = 800
height = 600
display = Display(width=width, height=height, caption="Cocktail Shaker Sort Visualization", sonification=True, soundDuration=0.01)

# generate a random array of integers to sort
array = random.sample(range(10, 440), 100)

# start the sorting visualization
cocktail_shaker_sort(array, display)

