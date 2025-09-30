import random
import time

def print_array(arr):
    print(" ".join(map(str, arr)))

def insertion_sort(arr):
    n = len(arr)
    print("\n--- Insertion Sort Steps ---")
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        print(f"\nStep {i}: Insert {key} into the sorted subarray [0..{i-1}]")

        while j >= 0 and arr[j] > key:
            print(f"Comparing {arr[j]} > {key}: true, shifting {arr[j]} to the right")
            arr[j + 1] = arr[j]
            j -= 1
            print_array(arr)

        arr[j + 1] = key
        print(f"Placed {key} at position {j+1}")
        print_array(arr)

if __name__ == "__main__":
    n = int(input("Enter number of elements in the array: "))
    if n <= 0:
        print("Array size must be positive.")
        exit(1)

    arr = [random.randint(1, 100) for _ in range(n)]
    print("\nGenerated Array:")
    print_array(arr)

    start = time.time()
    insertion_sort(arr)
    end = time.time()

    print("\nSorted Array:")
    print_array(arr)
    print(f"Time taken: {end - start:.6f} seconds")
