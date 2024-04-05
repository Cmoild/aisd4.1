#include <stdio.h>
#include <string.h>
#include <wchar.h>
#include <stdlib.h>
#include <math.h>
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
    unsigned short offset;
    unsigned short length;
    wchar_t symbol;
} lz77_tuple;

typedef struct lz77_result {
    lz77_tuple* result;
    int numberOfElements;
} lz77_result;

#define SEARCH_BUFFER_SIZE 65535
#define LOOK_AHEAD_BUFFER_SIZE 256

lz77_result lz77_encode(wchar_t* str, int stringLength) {
    lz77_tuple* out = (lz77_tuple*)malloc((stringLength + 1) * sizeof(lz77_tuple));
    wchar_t* buffer = (wchar_t*)calloc(SEARCH_BUFFER_SIZE, sizeof(wchar_t));
    printf("Start encode\n");
    int numOfElements = 0;
    int cur_buffer_size = 0;
    int pos = 0;
    int string_len = stringLength;
    int buf = 0;
    unsigned short offset = 0, length = 0;

    while (pos < string_len) {
        if (pos % 10000 == 0) printf("%d\n", pos);
        for (int i = 0; i < cur_buffer_size; i++) {
            if (str[pos] == buffer[i]) {
                unsigned short cur_len = 0;
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
                    if (cur_len == LOOK_AHEAD_BUFFER_SIZE) break;
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
    //wchar_t* result = (wchar_t*)calloc(stringLength + 1, sizeof(wchar_t));
    wchar_t* result = (wchar_t*)calloc(stringLength * 2 + 1, sizeof(wchar_t));
    int pos = 0;
    printf("String length: %d\n", stringLength);
    printf("Last tuple %d %d %c\n", in[numOfTuples - 1].offset, in[numOfTuples - 1].length, in[numOfTuples - 1].symbol);
    printf("Num of tuples: %d\n", numOfTuples);
    stringLength = 0;
    for (int i = 0; i < numOfTuples; i++) {
        lz77_tuple cur = in[i];
        if (i == 15299911) printf("%d\n", i);
        //int curPos = pos - cur.offset;
        stringLength += cur.length;
        for (int j = 0; j < cur.length; j++) {

            if (i == 15299911) printf("%d\n", j);
            result[pos] = result[pos - cur.offset];
            pos++;

        }
        result[pos] = cur.symbol;
        stringLength++;
        if (i % 100000 == 0) printf("%f\n", (float)i/(float)numOfTuples * 100);
        pos++;
    }
    return result;
}

char* decToBinary(int n)
{
    unsigned char* binaryNum = (unsigned char*)calloc(9, sizeof(unsigned char));
    binaryNum[8] = '\0';

    int i = 0;
    int j = 7;
    while (j >= 0) {
        binaryNum[j] = (unsigned char)(n % 2) + '0';
        n = n / 2;
        j--;
        i++;
    }

    return binaryNum;
}

int binaryToDec(unsigned char* byteStr) {
    int res = 0;
    for (int i = 0; i < 8; i++) {
        res += ((int)byteStr[7 - i] - '0') * (int)pow(2, i);
    }

    return res;
}

void WriteBinaryIntoFile(const char* path, char* binaryCode) {
    FILE* file;
    file = fopen(path, "ab");
    if (file == NULL) {
        printf("Error opening file!\n");
        printf("%s\n", path);
        return;
    }
    unsigned len = strlen(binaryCode);
    len = len + ((len % 8 == 0) ? 0 : (8 - len % 8));
    unsigned char* code = (unsigned char*)malloc(sizeof(char) * len);
    int i;
    for (i = 0; i < strlen(binaryCode); i++) {
        code[i] = binaryCode[i];
    }
    for (; i < len; i++) {
        code[i] = '0';
    }
    unsigned char* buffer = (char*)malloc(sizeof(char) * len / 8);
    for (i = 0; i < len; i += 8) {
        char* chr = (char*)malloc(sizeof(char) * 9);
        for (int j = 0; j < 8; j++) {
            chr[j] = code[i + j];
        }
        chr[8] = '\0';
        buffer[i / 8] = (unsigned char)binaryToDec(chr);
        free(chr);
    }
    free(code);
    fwrite(buffer, sizeof(unsigned char), len / 8, file);
    fclose(file);
}

unsigned char* GetBinaryCodeFromFile(const char* path, int pos, int maxLen) {
    FILE* file;
    file = fopen(path, "rb");
    unsigned len = 0;
    fseek(file, 0L, SEEK_END);
    if (file == NULL) {
        printf("Error opening file!\n");
        return NULL;
    }
    //printf("File size: %d\n", ftell(file));
    if (pos > ftell(file)) {
        return NULL;
    }
    if (ftell(file) > pos + maxLen) {
        len = maxLen;
        fseek(file, pos, SEEK_SET);
    }
    else {
        len = ftell(file) - pos;
        fseek(file, pos, SEEK_SET);
    }
    unsigned char* buffer = (unsigned char*)malloc(sizeof(char) * len);
    fread(buffer, sizeof(char), len, file);
    fclose(file);
    unsigned char* ret = (unsigned char*)malloc(sizeof(char) * len * 8 + 1);
    ret[len * 8] = '\0';
    for (int i = 0; i < len; i++) {
        char* cur = decToBinary((int)buffer[i]);
        for (int j = 0; j < 8; j++) {
            ret[i * 8 + j] = cur[j];
        }
        free(cur);
    }
    free(buffer);

    return ret;
}