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

typedef struct lz77_tuple {
    int offset;
    int length;
    wchar_t symbol;
} lz77_tuple;

typedef struct lz77_result {
    lz77_tuple* result;
    int numberOfElements;
} lz77_result;

#define SEARCH_BUFFER_SIZE 2048

lz77_result lz77_encode(wchar_t* str) {
    lz77_tuple* out = (lz77_tuple*)malloc((wcslen(str)) * sizeof(lz77_tuple));
    wchar_t buffer[SEARCH_BUFFER_SIZE];
    int numOfElements = 0;
    int cur_buffer_size = 0;
    int pos = 0;
    int string_len = wcslen(str);
    int buf = 0;
    int offset = 0, length = 0;

    while (pos < string_len) {

        for (int i = 0; i < cur_buffer_size; i++) {
            if (str[pos] == buffer[i]) {
                int cur_len = 0;
                int j = i;
                while (pos + cur_len < string_len){
                    //printf("%c", buffer[j]);
                    if (j >= 0 && buffer[j] == str[pos + cur_len]) {
                        cur_len++;
                    }
                    else if (str[pos + cur_len] == buffer[i] && i - cur_len == -1) {
                        j = i;
                        cur_len++;
                    }
                    else {
                        break;
                    }
                    j--;
                }
                if (cur_len > length) {
                    length = cur_len;
                    offset = i + 1;
                }

            }
        }

        if ((cur_buffer_size < SEARCH_BUFFER_SIZE) && (length + pos + 1 <= SEARCH_BUFFER_SIZE)) cur_buffer_size = length + pos + 1;
        else cur_buffer_size = SEARCH_BUFFER_SIZE;

        out[buf] = (lz77_tuple){ offset, length, str[pos + length] };
        numOfElements++;

        pos += length + 1;

        for (int i = 0; i < cur_buffer_size; i++) {
            buffer[i] = str[pos - i - 1];
        }

        buf++;
        offset = length = 0;
    }

    lz77_result result = (lz77_result){ out, numOfElements };
    
    return result;
}

wchar_t* lz77_decode(lz77_tuple* in, int numOfTuples, int stringLength) {
    wchar_t* result = (wchar_t*)calloc(stringLength + 1, sizeof(wchar_t));
    int pos = 0;
    for (int i = 0; i < numOfTuples; i++) {
        lz77_tuple cur = in[i];
        //int curPos = pos - cur.offset;
        for (int j = 0; j < cur.length; j++) {
            result[pos] = result[pos - cur.offset];
            pos++;
        }
        result[pos] = cur.symbol;
        pos++;
    }
    return result;
}
