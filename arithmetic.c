#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <wchar.h>
#include <string.h>
#include <stdbool.h>

#define MAX(a,b) (((a)>(b))?(a):(b))

#define uchar_MAX 256
typedef unsigned char uchar;

typedef struct prob {
    unsigned lower;
    unsigned upper;
    unsigned denominator;
    uchar character;
} prob;

static prob model[uchar_MAX];

prob* PopulateModel(){
    return model;
}

int* get_freqs_and_chars(uchar* str, int len) {
    int* frequencies = (int*)calloc(uchar_MAX, sizeof(int));
    
    for (int i = 0; i < len; i++) {
        frequencies[str[i]]++;
    }

    for (int i = 0; i < uchar_MAX; i++) {
        if (frequencies[i] != 0) frequencies[i] = MAX((int)((float)frequencies[i]/len), 1);
    }

    return frequencies;
}

int* get_freqs(uchar* str, int len) {
    int* frequencies = (int*)calloc(uchar_MAX, sizeof(int));
    
    for (int i = 0; i < len; i++) {
        frequencies[str[i]]++;
    }

    return frequencies;
}

uchar InitModel(uchar* str, int len) {
    int* freqs = get_freqs_and_chars(str, len);
    uchar cWithLowestFreq = 255;
    unsigned denominator = 1;
    for (int i = 0; i < uchar_MAX; i++) {
        if (freqs[i] > 0) {
            denominator += freqs[i];
        }
        if (freqs[i] > freqs[cWithLowestFreq] && freqs[i] > 0) {
            cWithLowestFreq = i;
        }
    }
    unsigned lastLower = 0;
    
    for (int i = 0; i < uchar_MAX; i++) {
        if (freqs[i] > 0) {
            model[i].lower = lastLower;
            model[i].upper = lastLower + freqs[i];
            //
            lastLower = model[i].upper;
            model[i].denominator = denominator;
            model[i].character = i;
        }
    }

    free(freqs);

    return cWithLowestFreq;
}

prob getProbability(uchar c) {
    return model[c];
}

prob getChr(unsigned low){
    for (int i = 0; i < uchar_MAX; i++) {
        if (low >= model[i].lower && low < model[i].upper) {
            return model[i];
        }
    }
    return model[0];
}

unsigned ArithmeticEncoding(uchar* input, int len) {
    unsigned int high = 0xFFFFFFFFU;
    unsigned int low = 0;
    uchar c;
    
    for ( int i = 0; i < len; i++ ) {
        c = input[i];
        //printf("%c", c);
        unsigned range = high - low;
        prob p = getProbability(c);
        //printf("%d %d\n", range, p.denominator);
        high = low + (unsigned)((float)range * ((float)p.upper/p.denominator));
        low = low + (unsigned)((float)range * ((float)p.lower/p.denominator));
        //if (++i > 8) break;
        
        //printf("%d %d %c\n", low, high, c);
    }

    return low;
}

uchar* ArithmeticDecoding(unsigned low, uchar dictionary[], int len) {
    unsigned highd = 0xFFFFFFFFU;
    unsigned lowd = 0;
    uchar* input;
    uchar* output = (uchar*)malloc(len * sizeof(uchar) + 1);
    output[len] = '\0';
    for (int i = 0; i < len; i++) {
        unsigned range = highd - lowd;
        //printf("%d %d\n", highd, lowd);
        input = dictionary;
        for (uchar c = *input; c != '\0'; c = *++input ) {
            prob p = getProbability(c);
            
            unsigned highdec = (unsigned)((float)range * ((float)p.upper/p.denominator));
            unsigned lowdec = (unsigned)((float)range * ((float)p.lower/p.denominator));
            if (low >= lowd + lowdec && low < lowd + highdec) {
                //printf("%c", c);
                output[i] = c;
                highd = lowd + highdec;
                lowd = lowd + lowdec;
                break;
            }
        }
    }

    return output;
}

static int maxBlockSize = 5;
//[1561270730, 2173995872, 3641001144, 1961898668]
/*
int main(){

    uchar* input = "hello world";
    printf("%c\n", InitModel(input, 11));
    input = "hel";

    uchar dictionary[] = "helo wrd";

    unsigned low = ArithmeticEncoding(input, 3);
    printf("%d\n", low);
    uchar* output = ArithmeticDecoding(low, dictionary, 3);
    printf("%s\n", output);
    
    
    return 0;
}
*/
