#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Function to print the array
void printArray(int arr[], int n) {
    for (int i = 0; i < n; i++)
        printf("%d ", arr[i]);
    printf("\n");
}

void insertionSort(int arr[], int n) {
    int i, key, j;

    printf("\n--- Insertion Sort Steps ---\n");
    for (i = 1; i < n; i++) {
        key = arr[i];
        j = i - 1;

        printf("\nStep %d: Insert %d into the sorted subarray [0..%d]\n", i, key, i-1);

        while (j >= 0 && arr[j] > key) {
            printf("Comparing %d > %d: true, shifting %d to the right\n", arr[j], key, arr[j]);
            arr[j + 1] = arr[j];
            j = j - 1;
            printArray(arr, n);
        }
        arr[j + 1] = key;
        printf("Placed %d at position %d\n", key, j+1);
        printArray(arr, n);
    }
}

int main() {
    int n;

    printf("Enter number of elements in the array: ");
    scanf("%d", &n);

    if (n <= 0) {
        printf("Array size must be positive.\n");
        return 1;
    }

    int *arr = (int *)malloc(n * sizeof(int));
    if (arr == NULL) {
        printf("Memory allocation failed.\n");
        return 1;
    }

    srand(time(NULL));

    printf("\nGenerated Array: ");
    for (int i = 0; i < n; i++) {
        arr[i] = rand() % 1000 + 1;  // random positive int (1–1000)
        printf("%d ", arr[i]);
    }
    printf("\n");

    clock_t start, end;
    start = clock();

    insertionSort(arr, n);

    end = clock();
    double time_taken = ((double)(end - start)) / CLOCKS_PER_SEC;

    printf("\nSorted Array: ");
    printArray(arr, n);
    printf("Time taken: %f seconds\n", time_taken);

    free(arr);
    return 0;
}
