#include <stdio.h>
#include <string.h>
#include <wchar.h>
#include <stdlib.h>
#include <locale.h>

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

char** radix_sort(/*char a[][MAX_LEN], */int n) {
    int max_len = 0;
    char arr[][MAX_LEN] = {"apple", "banana", "apricot", "date", "fig", "grape"};

    for (int i = 0; i < n; i++) {
        int len = strlen(arr[i]);
        if (len > max_len)
            max_len = len;
    }

    for (int exp = max_len - 1; exp >= 0; exp--)
        counting_sort(arr, n, exp);

    char** ret = (char**)malloc(sizeof(char*) * n);
    for (int i = 0; i < n; i++){
        ret[i] = (char*)malloc(sizeof(char) * MAX_LEN);
        strcpy(ret[i], arr[i]);
    }
    return ret;
}
/*
int main() {
    //wchar_t* arr = {L"apple", L"banana", L"слон", L"date", L"fig", L"grape"};
    char b[][MAX_LEN] = {"apple", "banana", "apricot", "date", "fig", "grape"};
    char** arr = (char**)malloc(sizeof(char*) * 6);
    for (int i = 0; i < 6; i++){
        arr[i] = (char*)malloc(sizeof(char) * 100);
    }
    
    char** arr = (char**)malloc(sizeof(char*) * 6);
    for (int i = 0; i < 6; i++){
        arr[i] = (char*)malloc(sizeof(char) * 100);
        arr[i] = b[i];
    }
    //arr = b;
    int n = 6;
    printf("%d\n", n);
    system("pause");
    //setlocale(LC_ALL, "C.UTF-8");
    //printf("%d\n", n);
    //radix_sort(arr, n);
    //printf("%d\n", n);
    for (int i = 0; i < n; i++){
        printf("%s\n", arr[i]);
    }
    
    arr = radix_sort(b, 6);
    for (int i = 0; i < 6; i++){
        printf("%s\n", arr[i]);
    }
    system("pause");
    return 0;

}
*/