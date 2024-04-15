#include <stdio.h>
#include <string.h>
#include <wchar.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>

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

#define RUN_LENGTH 65535
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


/*
int main()
{
    int  num, i;
    wchar_t* a[] = {L"\"MC", L"MC\"", L"C\"M"};
    wchar_t* data = L"\"MC";
    num = 3;

    //a = (wchar_t**)malloc(sizeof(wchar_t*) * num);
    //for(i=0;i<num;i++)

        //scanf("%ls",&a[i]);
    
    mergesort(a, 0, num-1);
    
    printf("\nSorted array :\n");
    for(i=0;i<num;i++)
        printf("%ls ",a[i]);
    
    BWT_MTF(data, num);
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