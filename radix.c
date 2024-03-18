#include <stdio.h>
#include <string.h>

#define MAX_LEN 100
#define RANGE 256

void counting_sort(char arr[][MAX_LEN], int n, int exp) {
    char output[n][MAX_LEN];
    int count[RANGE + 1] = {0};

    for (int i = 0; i < n; i++)
        count[arr[i][exp]]++;

    for (int i = 1; i < RANGE; i++)
        count[i] += count[i - 1];

    for (int i = n - 1; i >= 0; i--) {
        strcpy(output[count[arr[i][exp]] - 1], arr[i]);
        count[arr[i][exp]]--;
    }

    for (int i = 0; i < n; i++)
        strcpy(arr[i], output[i]);
}

void radix_sort(char** a, int n) {
    char arr[n][MAX_LEN];
    for (int i = 0; i < n; i++){
        strcpy(arr[i], *(a + i));
        printf("%s\n", a[i]);
    }
    int max_len = 0;
    for (int i = 0; i < n; i++) {
        int len = strlen(arr[i]);
        if (len > max_len)
            max_len = len;
    }

    for (int exp = max_len - 1; exp >= 0; exp--)
        counting_sort(arr, n, exp);
    /*
    for (int i = 0; i < n; i++){
        for (int j = 0; j < strlen(arr[i]); j++){
            printf("%c", arr[i][j]);
        }
        printf("\n");
    }
    */
}

int square(int a, int b){
    return a * b;
}

int main() {
    char** arr = {"apple", "banana", "cherry", "date", "fig", "grape"};
    int n = 6;
    printf("%d\n", n);
    radix_sort(arr, n);
    printf("%d\n", n);
    for (int i = 0; i < n; i++)
        //printf("%s\n", arr[i]);

    system("pause");
    return 0;

}
