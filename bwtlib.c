#include <stdio.h>
#include <string.h>
#include <wchar.h>
#include <stdlib.h>
#include <math.h>



int cmp_str(const void* a, const void* b) {
    const wchar_t* p1 = *(wchar_t**)a;
    const wchar_t* p2 = *(wchar_t**)b;
    return wcscmp(p1, p2);
}

wchar_t** sort(wchar_t** arr, int n) {
    qsort(arr, n, sizeof(wchar_t*), cmp_str);
    return arr;
}

wchar_t* ShiftedArray(const wchar_t* orig, const int shift) {
    int len = wcslen(orig);
    wchar_t* shifted = (wchar_t*)calloc(len + 1, sizeof(wchar_t));

    for (int i = 0; i < len - shift; i++) {
        shifted[i] = orig[i + shift];
    }
    for (int i = 0; i < shift; i++) {
        shifted[i + len - shift] = orig[i];
    }
    return shifted;
}

typedef struct BWT_return {
    wchar_t* str;
    int index;
} BWT_return;

BWT_return BWT(wchar_t* data, int len) {
    //int len = wcslen(data);
    wchar_t** arr = (wchar_t**)malloc(len * len * sizeof(wchar_t*));
    for (int i = 0; i < len; i++) {
        arr[i] = ShiftedArray(data, i);
    }
    sort(arr, len);
    //radix_sort(arr, len);
    wchar_t* ret = (wchar_t*)calloc(len + 1, sizeof(wchar_t));
    int ind = 0;
    for (int i = 0; i < len; i++) {
        ret[i] = arr[i][len - 1];
        if (wcscmp(data, arr[i]) == 0) ind = i;
        free(arr[i]);
    }
    free(arr);
    BWT_return res = (BWT_return){ ret, ind };
    return res;
}

void ShiftRight(wchar_t str[], int ind) {
    for (int i = ind; i >= 1; i--) {
        str[i] = str[i - 1];
    }
}

void MoveToFront(wchar_t* data, int len) {
    wchar_t alph[WCHAR_MAX] = {0};
    for (int i = 0; i < WCHAR_MAX; i++) {
        alph[i] = (wchar_t)i;
    }
    for (int i = 0; i < len; i++) {
        int index = 0;
        for (int j = 0; j < WCHAR_MAX; j++) {
            if (data[i] == alph[j]) {
                index = j;
                break;
            }
        }
        ShiftRight(alph, index);
        alph[0] = data[i];
        data[i] = (wchar_t)index;
    }
}

#define RUN_LENGTH 16383

typedef struct BWT_MTF_return {
    unsigned short arr[RUN_LENGTH];
    int index;
} BWT_MTF_return;

BWT_MTF_return BWT_MTF(wchar_t* data, int len) {
    BWT_return ret = BWT(data, len);
    data = ret.str;
    MoveToFront(data, len);
    
    BWT_MTF_return result;
    for (int i = 0; i < len; i++) {
        result.arr[i] = (unsigned short)data[i];
    }
    result.index = ret.index;
    return result;
}

