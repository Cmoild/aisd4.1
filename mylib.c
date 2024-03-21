#include <stdio.h>
#include <string.h>
#include <wchar.h>
#include <stdlib.h>
//#pragma warning(disable : 4996)

#define MAX_LEN 10000
#define RANGE WCHAR_MAX

void counting_sort(wchar_t** arr, int n, int exp) {
    wchar_t** output = (wchar_t**)malloc(n * sizeof(wchar_t*));
    for (int i = 0; i < n; i++){
        output[i] = (wchar_t*)malloc(MAX_LEN * sizeof(wchar_t));
        //wcscpy_s(output[i], 3, L"aaa");
    }
    int count[RANGE + 1] = {0};

    for (int i = 0; i < n; i++)
        count[exp < wcslen(arr[i]) ? arr[i][exp] + 1 : 0]++;

    for (int i = 1; i < RANGE; i++)
        count[i] += count[i - 1];

    for (int i = n - 1; i >= 0; i--) {
        wcscpy(output[count[exp < wcslen(arr[i]) ? arr[i][exp] + 1 : 0] - 1], arr[i]);
        count[exp < wcslen(arr[i]) ? arr[i][exp] + 1 : 0]--;
    }

    for (int i = 0; i < n; i++)
        wcscpy(arr[i], output[i]);

    for (int i = 0; i < n; i++) {
        free(output[i]);
    }
    free(output);
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

int cmp_str(const void* a, const void* b){
    const wchar_t* p1 = *(wchar_t**)a;
    const wchar_t* p2 = *(wchar_t**)b;
    return wcscmp(p1, p2);
}

wchar_t** sort(wchar_t** arr, int n){
    qsort(arr, n, sizeof(wchar_t*), cmp_str);
    return arr;
}
/*
int main(void) {
    wchar_t arr[][MAX_LEN] = {L"BANANA", L"ANANAB", L"NANABA", L"ANABAN", L"NABANA", L"ABANAN"};
    wchar_t** arr2 = (wchar_t**)malloc(6 * sizeof(wchar_t*));
    wchar_t** arr3;
    for (int i = 0; i < 6; i++){
        arr2[i] = (wchar_t*)malloc(MAX_LEN * sizeof(wchar_t));
        wcscpy(arr2[i], arr[i]);
    }
    
    //arr3 = radix_sort(arr2, 6);
    sort(arr2, 6);
    for (int i = 0; i < 6; i++){
        printf("%ls\n", arr2[i]);
    }

    for (int i = 0; i < 6; i++) {
        free(arr2[i]);
        
    }
    free(arr2);
    return 0;
}
*/