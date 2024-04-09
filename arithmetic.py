from huffman_c import get_probs

def arithmetic_encoding(data, probs, chars):
    print(probs, chars)
    left = 0
    right = 1
    total_size = sum(probs)
    segments = [0]
    segments += [probs[i] / total_size for i in range(0, len(probs))]
    segments = [segments[i] + segments[i-1] for i in range(1, len(probs))]
    print (segments)
    return

    for c in data:
        left += probs[chars.index(c)] / total_size
        if (chars.index(c) != len(probs) - 1):
            right += left + (probs[chars.index(c) + 1]) / total_size
        else:
            right = 1
        total_size = total_size/(right - left)
        print(left, right, total_size)
    
    return left


def arithmetic_decoding(left, probs, chars, data_length):
    data = ""
    right = 1
    total_size = sum(probs)


    for _ in range(data_length):
        print(left, right, total_size)

    return data

# Example usage
data = "hello"
probs, chars = get_probs(data, None)
precision = 8
result = arithmetic_encoding(data, probs, chars)
print(result)

