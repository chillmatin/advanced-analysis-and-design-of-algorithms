#include <stdio.h>
#include <stdlib.h>
#include <unistd.h> // For sleep function
#include <time.h>

// Function to print the array
void printArray(int arr[], int size) {
    for (int i = 0; i < size; i++)
        printf("%d ", arr[i]);
    printf("\n");
}

// Merge two sorted subarrays arr[l..m] and arr[m+1..r]
void merge(int arr[], int l, int m, int r) {
    int i, j, k;
    int n1 = m - l + 1; // Size of left subarray
    int n2 = r - m;     // Size of right subarray

    // Create temporary arrays
    int *L = (int*)malloc(n1 * sizeof(int));
    int *R = (int*)malloc(n2 * sizeof(int));

    // Copy data to temp arrays L[] and R[]
    for (i = 0; i < n1; i++)
        L[i] = arr[l + i];
    for (j = 0; j < n2; j++)
        R[j] = arr[m + 1 + j];

    printf("Merging left: ");
    for (i = 0; i < n1; i++) printf("%d ", L[i]);
    printf("and right: ");
    for (j = 0; j < n2; j++) printf("%d ", R[j]);
    printf("\n");
    sleep(1); // Pause to visualize merging step

    // Merge the temp arrays back into arr[l..r]
    i = 0; // Initial index of first subarray
    j = 0; // Initial index of second subarray
    k = l; // Initial index of merged subarray
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            arr[k] = L[i];
            i++;
        } else {
            arr[k] = R[j];
            j++;
        }
        k++;
        printArray(arr, r + 1); // Show progress after each insertion
        sleep(1);
    }

    // Copy the remaining elements of L[], if any
    while (i < n1) {
        arr[k] = L[i];
        i++;
        k++;
        printArray(arr, r + 1);
        sleep(1);
    }

    // Copy the remaining elements of R[], if any
    while (j < n2) {
        arr[k] = R[j];
        j++;
        k++;
        printArray(arr, r + 1);
        sleep(1);
    }

    // Free temporary arrays
    free(L);
    free(R);
}

// Recursive merge sort function
void mergeSort(int arr[], int l, int r) {
    if (l < r) {
        // Find the middle point
        int m = l + (r - l) / 2;

        printf("Dividing: ");
        for (int i = l; i <= r; i++) printf("%d ", arr[i]);
        printf("\n");
        sleep(1); // Pause to visualize division

        // Sort first and second halves
        mergeSort(arr, l, m);
        mergeSort(arr, m + 1, r);

        // Merge the sorted halves
        merge(arr, l, m, r);
    }
}

int main() {
    int n;
    printf("Enter array size: ");
    scanf("%d", &n);

    int *arr = (int*)malloc(n * sizeof(int));
    if (arr == NULL) {
        printf("Memory allocation failed.\n");
        return 1;
    }

    // Seed random number generator
    srand((unsigned int)time(NULL));
    for (int i = 0; i < n; i++) {
        arr[i] = rand() % 101; // Random number between 0 and 1000
    }
    int arr_size = n;

    printf("Original array:\n");
    printArray(arr, arr_size);
    sleep(1);

    // Call mergeSort on the entire array
    mergeSort(arr, 0, arr_size - 1);

    printf("Sorted array:\n");
    printArray(arr, arr_size);
    return 0;
}