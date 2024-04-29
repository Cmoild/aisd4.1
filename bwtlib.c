#include <stdio.h>
#include <string.h>
#include <wchar.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>
#include "libsais16.h"

void mergesort(wchar_t* a[],int i,int j);
void merge(wchar_t* a[],int i1,int j1,int i2,int j2);

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

//#define RUN_LENGTH 65535
#define RUN_LENGTH 1000000
static wchar_t* temp[RUN_LENGTH];

typedef struct BWT_return {
    wchar_t* str;
    int index;
} BWT_return;



BWT_return BWT(wchar_t* data, int len) {
    //int len = wcslen(data);
    wchar_t** arr = (wchar_t**)malloc(len * sizeof(wchar_t*));
    
    for (int i = 0; i < len; i++) {
        
        
        arr[i] = ShiftedArray(data, i);
        
    }
    //sort(arr, len);
    
    
    mergesort(arr, 0, len - 1);
    
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

typedef struct BWT_MTF_return {
    unsigned short* arr;
    //uint16_t arr[RUN_LENGTH];
    int index;
} BWT_MTF_return;

BWT_MTF_return BWT_MTF(wchar_t* data, int len) {
    
    //BWT_return ret = BWT(data, len);
    //********USING LIBSAIS***********
    
    BWT_return ret;
    uint16_t* resbwt = (uint16_t*)malloc(len * sizeof(uint16_t));
    int32_t* tmp = (int32_t*)malloc(len * sizeof(int32_t));
    ret.index = libsais16_bwt(data, resbwt, tmp, len, 0, NULL);
    ret.str = resbwt;
    
    //********************************
    data = ret.str;
    MoveToFront(data, len);
    
    BWT_MTF_return result;
    int k = 0;
    result.arr = data;
    /*
    for (int i = 0; i < len; i++) {
        result.arr[i] = (unsigned short)data[i];
        
    }
    */
    result.index = ret.index;
    //printf("%d\n", k);
    return result;
}

uint16_t* UNBWT(uint16_t* data, int len, int ind) {
    int32_t* tmp = (int32_t*)malloc(len * sizeof(int32_t));
    libsais16_unbwt(data, data, tmp, len, NULL, ind);
    return data;
}


/*
int main()
{
    
    wchar_t* s = (wchar_t*)malloc(RUN_LENGTH * sizeof(wchar_t));
    FILE* f;
    f = _wfopen(L"C:\\Users\\cold1\\vscpr\\aisd\\aisd4.1\\texts\\enwik7.txt", L"r");
    fread(s, 2, RUN_LENGTH, f);
    
    int16_t* res = (int16_t*)malloc(RUN_LENGTH * sizeof(int16_t));
    int32_t* tmp = (int32_t*)malloc(RUN_LENGTH * sizeof(int32_t));
    int x = libsais16_bwt(s, res, tmp, 6, 0, NULL);
    printf("%d\n", x);
    
    return 0;
}
*/

void mergesort(wchar_t* a[],int i,int j)
{
    int mid;
        
    if(i<j)
    {
        mid=(i+j)/2;
        
        #pragma omp parallel sections 
        {

            #pragma omp section
            {
                mergesort(a,i,mid);        //left recursion
            }

            #pragma omp section
            {
                mergesort(a,mid+1,j);    //right recursion
            }
        }

        merge(a,i,mid,mid+1,j);    //merging of two sorted sub-arrays
    }
}

void merge(wchar_t* a[],int i1,int j1,int i2,int j2)
{
    //wchar_t** temp = (wchar_t**)malloc(RUN_LENGTH * sizeof(wchar_t*));
    //wchar_t* temp[RUN_LENGTH];    //array used for merging
    
    //temp = (wchar_t**)calloc(RUN_LENGTH, sizeof(wchar_t*));
    
    int i,j,k;
    i=i1;    //beginning of the first list
    j=i2;    //beginning of the second list
    k=0;
    
    while(i<=j1 && j<=j2)    //while elements in both lists
    {
        //if(a[i]<a[j])
        if(wcscmp(a[i],a[j])<0)
            temp[k++]=a[i++];
        else
            temp[k++]=a[j++];
    }
    
    while(i<=j1)    //copy remaining elements of the first list
        temp[k++]=a[i++];
        
    while(j<=j2)    //copy remaining elements of the second list
        temp[k++]=a[j++];
        
    //Transfer elements from temp[] back to a[]
    for(i=i1,j=0;i<=j2;i++,j++)
        a[i]=temp[j];

    
}