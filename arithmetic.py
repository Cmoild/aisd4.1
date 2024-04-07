def arithmetic_encoding(data, precision):
    lower = 0
    upper = 1
    range_size = 1

    for symbol in data:
        symbol_range = range_size // len(data)
        symbol_index = ord(symbol)
        lower += symbol_range * symbol_index
        upper = lower + symbol_range
        range_size = upper - lower

    return lower

def arithmetic_decoding(encoded_value, precision, data_length):
    data = ""
    lower = 0
    upper = 1
    range_size = 1

    for _ in range(data_length):
        symbol_range = range_size / data_length
        symbol_index = (encoded_value - lower) / symbol_range
        symbol_char = chr(symbol_index)
        data += symbol_char

        lower += symbol_range * symbol_index
        upper = lower + symbol_range
        range_size = upper - lower

    return data

# Example usage
data = "hello"
precision = 8
result = arithmetic_encoding(data, precision)
print(result)
print(arithmetic_decoding(result, precision, len(data)))
