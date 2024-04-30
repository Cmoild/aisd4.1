#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <wchar.h>
#include <string.h>
#include <stdbool.h>

typedef struct prob {
    unsigned lower;
    unsigned upper;
    unsigned denominator;
} prob;

static prob model[WCHAR_MAX];

int* get_freqs_and_chars(wchar_t* str, int len) {
    int* frequencies = (int*)calloc(WCHAR_MAX, sizeof(int));
    
    for (int i = 0; i < len; i++) {
        frequencies[str[i]]++;
    }

    return frequencies;
}

void InitModel(wchar_t* str, int len) {
    int* freqs = get_freqs_and_chars(str, len);
    unsigned lastLower = 0;
    
    for (int i = 0; i < WCHAR_MAX; i++) {
        if (freqs[i] > 0) {
            model[i].lower = lastLower;
            model[i].upper = lastLower + freqs[i];
            //
            lastLower = model[i].upper;
            model[i].denominator = len;
        }
    }

    free(freqs);
}

void output_bit_plus_pending(bool bit, int* pending_bits)
{
    //printf("%c\n", bit + '0' );
    //printf("%d -- pbit\n", *pending_bits);
    while ( *pending_bits-- ){
        //printf("%c\n", !bit + '0' );
    }
}

prob getProbability(wchar_t c) {
    return model[c];
}

int main(){
    //unsigned int high = 0xFFFFFFFFU;
    unsigned int high = 59049;
    unsigned int low = 0;
    int pending_bits = 0;
    int* ppending = &pending_bits;
    wchar_t c;
    wchar_t* input = L"abcdefghijklmnopqrstuvwxyz";

    InitModel(input, 9);

    
    for ( c = *input; c != '\0'; c = *++input ) {
        unsigned range = high - low;
        prob p = getProbability(c);
        high = low + (range * p.upper)/p.denominator;
        low = low + (range * p.lower)/p.denominator;
        /*
        for ( ; ; ) {
            if ( high < 0x80000000U ) {
                output_bit_plus_pending( 0, ppending );
                low <<= 1;
                high <<= 1;
                high |= 1;
            } else if ( low >= 0x80000000U ) {
                output_bit_plus_pending( 1, ppending );
                low <<= 1;
                high <<= 1;
                high |= 1;
            } else if ( low >= 0x40000000 && high < 0xC0000000U ){
                pending_bits++;
                low <<= 1;
                low &= 0x7FFFFFFF;
                high <<= 1;
                high |= 0x80000001;
            } 
            else{
                break;
            }
        }
        */
        printf("%d %d %c\n", low, high, c);
    }
    
    return 0;
}