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

struct lz77_tuple{
    int offset;
    int length;
    wchar_t symbol;
};

typedef struct lz77_tuple lz77_tuple;

#define SEARCH_BUFFER_SIZE 5
#define LOOKAHEAD_BUFFER_SIZE 10

lz77_tuple* lz77_encode(wchar_t* str) {
    lz77_tuple* out = (lz77_tuple*)malloc((wcslen(str)) * sizeof(lz77_tuple));
    //lz77_tuple out[11];
    //for (int i = 0; i < wcslen(str); i++) out[i] = (lz77_tuple){0, 0, str[i]};
    int pos = 0;
    printf("%d\n", sizeof(lz77_tuple));
    int string_len = wcslen(str);
    int buf = 0;
    int offset = 0, length = 0;
    while (pos < string_len){
        for (int i = 0, j = 0; (j < SEARCH_BUFFER_SIZE) && (i > 0); i--, j++){
            int curlen = 0;
            offset = 0;
            if (str[pos] == str[pos - i]){
                offset = pos - i;
                for (int k = 0; (k < j) && (pos + k < string_len); k++){
                    if (str[pos + k] == str[pos - i + k]){
                        curlen++;
                    }
                    else break;
                }
                if (curlen > length){
                    length = curlen;
                    offset = pos - i;
                }
                printf("%d\n", curlen);
            }
        }

        out[buf] = (lz77_tuple){offset, length, str[pos]};
        pos = length + pos + 1;
        buf++;
    }

    for (int i = 0; i < wcslen(str); i++) {
        printf("%c %d %d\n", out[i].symbol, out[i].offset, out[i].length);
    }
    //free(out);
    return out;
}


int main(void) {
    wchar_t* str = L"abracadabra";
    lz77_encode(str);
}
