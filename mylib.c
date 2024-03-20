#include <stdio.h>
#include <string.h>
#include <wchar.h>
#include <stdlib.h>
#include <locale.h>

#define MAX_LEN 100
#define RANGE 256

void counting_sort(wchar_t** arr, int n, int exp) {
    wchar_t** output = (wchar_t**)malloc(sizeof(wchar_t*) * n);
    for (int i = 0; i < n; i++){
        output[i] = (wchar_t*)malloc(sizeof(wchar_t) * MAX_LEN);
        wcscpy(output[i], L"aaa");
    }
    int count[RANGE + 1] = {0};

    for (int i = 0; i < n; i++)
        count[arr[i][exp]]++;

    for (int i = 1; i < RANGE; i++)
        count[i] += count[i - 1];
    printf("first cpy\n");
    for (int i = n - 1; i >= 0; i--) {
        wcscpy(output[count[arr[i][exp]] - 1], arr[i]);
        count[arr[i][exp]]--;
    }
    printf("second cpy\n");
    for (int i = 0; i < n; i++)
        wcscpy(arr[i], output[i]);
}

wchar_t** radix_sort(wchar_t** arr, int n) {
    int max_len = 0;

    for (int i = 0; i < n; i++) {
        int len = wcslen(arr[i]);
        if (len > max_len)
            max_len = len;
    }

    for (int exp = max_len - 1; exp >= 0; exp--)
        counting_sort(arr, n, exp);

    return arr;
}

wchar_t* ret_str(wchar_t* str){
    return str;
}

wchar_t** example(wchar_t** arr, int n){
    for (int i = 0; i < n; i++){
        printf("%ls\n", arr[i]);
    }
    return arr;
}

int main(void) {
    wchar_t arr[][MAX_LEN] = {L"apple", L"banana", L"слон", L"date", L"fig", L"grape"};
    wchar_t** arr2 = (wchar_t**)malloc(sizeof(wchar_t*) * 6);
    printf("Before sorting:\n");
    for (int i = 0; i < 6; i++){
        arr2[i] = (wchar_t*)malloc(sizeof(wchar_t) * MAX_LEN);
        //wcscpy(arr2[i], arr[i]);
        arr2[i] = L"aaa";
        printf("%ls\n", arr2[i]);
    }
    printf("After sorting:\n");
    radix_sort(arr2, 6);
    for (int i = 0; i < 6; i++){
        printf("%ls\n", arr2[i]);
    }
    system("pause");
    return 0;
}
