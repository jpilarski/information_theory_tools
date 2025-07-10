import sys
import math
from bitarray import bitarray
from collections import Counter

original_file = ""
encoded_file = ""
code = ""
decoded_file = ""
binary = True
huffman = False
lzw = False

def to_code(size, number):
    return bin(number)[2:].zfill(size)

def traverse_tree(node, path, freq_map, output):
    if isinstance(node[0], str):
        symbol = node[0]
        output.append([symbol, freq_map[symbol], path])
    else:
        traverse_tree(node[0], path + "0", freq_map, output)
        traverse_tree(node[1], path + "1", freq_map, output)

def create_lzw_code():
    global original_file
    all_codes = sorted(set(original_file))
    code_table = [[[val], idx] for idx, val in enumerate(all_codes)]
    return code_table

def dialog():
    if binary:
        print("Current coding: fixed-length binary")
    elif huffman:
        print("Current coding: Huffman")
    else:
        print("Current coding: LZW")
    print(" 1) Load original file")
    print(" 2) Load encoded file")
    print(" 3) Load code")
    print(" 4) Encode")
    print(" 5) Decode")
    if lzw == False:
        print(" 6) Create code")
    print(" 7) Save encoded file")
    print(" 8) Save decoded file")
    print(" 9) Save code")
    print("10) Clear environment")
    if binary:
        print("11) Switch to Huffman (will clear environment)")
    else:
        print("11) Switch to fixed-length binary (will clear environment)")
    if lzw:
        print("12) Switch to Huffman (will clear environment)")
    else:
        print("12) Switch to LZW (will clear environment)")
    print("13) Exit")
    return(input("Select mode: "))

def load_original():
    print("Load original file")
    global original_file
    if original_file != "":
        decision = input("Original file already exists. Type [yes] to overwrite: ")
        if decision != "yes":
            return
    filename = input("Name of the file: ")
    original_file = ""
    try:
        if lzw == False:
            with open(filename, "r", encoding="utf-8") as file:
                original_file = file.read()
        else:
            with open(filename, "rb") as file:
                bytes = file.read()
                original_file = list(bytes)
        print("Success")
    except:
        print("Error")

def load_encoded():
    print("Load encoded file")
    global encoded_file
    if encoded_file != "":
        decision = input("Encoded file already exists. Type [yes] to overwrite: ")
        if decision != "yes":
            return
    filename = input("Name of the file: ")
    encoded_file = ""
    try:
        binarr = bitarray()
        with open(filename, "rb") as file:
            binarr.fromfile(file)
        encoded_file = binarr.to01()
        print("Success")
    except:
        print("Error")

def load_code():
    print("Load code file")
    global code
    if code != "":
        decision = input("Code already exists. Type [yes] to overwrite: ")
        if decision != "yes":
            return
    filename = input("Name of the file: ")
    code = ""
    try:
        code = []
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                line = line.rstrip("\n")
                if not line:
                    continue
                parts = line.split("\t")
                symbol = eval(parts[0])
                if lzw == False:
                    code.append([symbol, parts[1], parts[2]])
                else:
                    code.append([[int(parts[0])], parts[1]])
        print("Success")
    except:
        print("Error")

def encode_file():
    print("Encode file")
    global original_file, code, encoded_file
    if original_file == "":
        print("No original file")
        return
    if code == "" and lzw == False:
        print("No code to encode")
        return
    if encoded_file != "":
        decision = input("Encoded file already exists. Type [yes] to overwrite: ")
        if decision != "yes":
            return
    if lzw == False:
        code_map = {c[0]: c[2] for c in code}
        encoded_file = "".join(code_map[char] for char in original_file if char in code_map)
        encoded_file += code_map["END"]
    else:
        try:
            limiter_input = input("Dictionary max size (2^n, 0=unlimited): ")
            limiter = int(limiter_input)
            if limiter != 0:
                limiter = 2 ** limiter
        except:
            print("Invalid limiter value")
            return
        code = create_lzw_code()
        advanced_code = {tuple(c[0]): c[1] for c in code}
        index = max(advanced_code.values()) + 1
        encoded_list = []
        w = (original_file[0],)
        for i in range(1, len(original_file)):
            k = original_file[i]
            wk = w + (k,)
            if wk in advanced_code:
                w = wk
            else:
                encoded_list.append(advanced_code[w])
                if limiter == 0 or len(advanced_code) < limiter:
                    advanced_code[wk] = index
                    index += 1
                w = (k,)
        encoded_list.append(advanced_code[w])
        max_index = max(advanced_code.values())
        code_length = math.ceil(math.log2(max_index + 1))
        for i in range(len(code)):
            code[i][1] = to_code(code_length, code[i][1])
        encoded_file = "".join(to_code(code_length, idx) for idx in encoded_list)
    if len(encoded_file) > 80:
        print(f"First 80 bits of encoded file:\n{encoded_file[:80]}")
    else:
        print(f"Encoded file:\n{encoded_file}")

def decode_file():
    print("Decode file")
    global code, encoded_file, original_file, decoded_file, binary, huffman
    if encoded_file == "":
        print("No file to decode")
        return
    if code == "":
        print("No code to decode")
        return
    if decoded_file != "":
        decision = input("Decoded file already exists. Type [yes] to overwrite: ")
        if decision != "yes":
            return
    if lzw == False:
        code_map = {c[2]: c[0] for c in code}
    decoded_file = ""
    decoded_symbols = []
    if binary:
        length = len(next(iter(code_map)))
        i = 0
        while i + length <= len(encoded_file):
            chunk = encoded_file[i:i+length]
            if chunk in code_map:
                symbol = code_map[chunk]
                if symbol == "END":
                    break
                decoded_symbols.append(symbol)
                i += length
        decoded_file = ''.join(decoded_symbols)
    elif huffman:
        i = 0
        length = 1
        while i + length <= len(encoded_file):
            chunk = encoded_file[i:i+length]
            if chunk in code_map:
                symbol = code_map[chunk]
                if symbol == "END":
                    break
                decoded_symbols.append(symbol)
                i += length
                length = 1
            else:
                length += 1
        decoded_file = ''.join(decoded_symbols)
    else:
        code_map = {c[1]: c[0] for c in code}
        code_length = len(next(iter(code_map))) 
        max_size = 2 ** code_length
        decoded_list = []
        advanced_code = dict(code_map)
        keys_list = sorted(advanced_code.keys())
        index = len(advanced_code)
        i = 0
        prev = None
        while i + code_length <= len(encoded_file):
            curr_code = encoded_file[i:i+code_length]
            i += code_length
            if curr_code in advanced_code:
                entry = advanced_code[curr_code]
            elif prev is not None:
                entry = advanced_code[prev] + [advanced_code[prev][0]]
            else:
                print("Error: invalid code during decoding")
                break
            decoded_list.extend(entry)
            if prev is not None and len(advanced_code) < max_size:
                new_key = to_code(code_length, index)
                new_value = advanced_code[prev] + [entry[0]]
                advanced_code[new_key] = new_value
                index += 1
            prev = curr_code
        decoded_file = decoded_list
    if len(decoded_file) > 80:
        print(f"First 80 chars of decoded file:\n{decoded_file[:80]}")
    else:
        print(f"Decoded file:\n{decoded_file}")
    if original_file == "":
        print("No original file to compare")
    else:
        if original_file == decoded_file:
            print("Correct decoding")
        else:
            print("Incorrect decoding")

def create_code():
    print("Create code")
    global code, original_file, binary, huffman
    if original_file == "":
        print("No file to create code")
        return
    if code != "":
        decision = input("Code already exists. Type [yes] to overwrite: ")
        if decision != "yes":
            return
    dict = Counter(original_file)
    dict["END"] = 1
    sorted_dict = sorted(dict.items(), key=lambda item: item[1], reverse=True)
    all_codes = len(dict)
    code = []
    if binary:
        length = math.ceil(math.log2(all_codes))
        for i, (d, value) in enumerate(sorted_dict):
            code.append([d, value, to_code(length, i)])
    else:
        total = sum(dict.values())
        pairs = [[[char], count / total] for char, count in dict.items()]
        pairs.sort(key=lambda x: x[1])
        while len(pairs) > 1:
            first = pairs.pop(0)
            second = pairs.pop(0)
            new_node = [[second[0], first[0]], first[1]+second[1]]
            pairs.append(new_node)
            pairs.sort(key=lambda x: x[1])
        tree = pairs[0]
        tree = tree[0]
        traverse_tree(tree, "", dict, code)
        code.sort(key=lambda x: x[1], reverse=True) 
    print("Code created")

def save_encoded():
    print("Save encoded")
    global encoded_file
    if encoded_file == "":
        print("No encoded text created")
    else:
        filename = input("Name of the file: ")
        try:
            bits = bitarray(encoded_file)
            with open(filename, "wb") as file:
                bits.tofile(file)
            print("Success")
        except:
            print("Error")

def save_decoded():
    print("Save decoded")
    global decoded_file
    if decoded_file == "":
        print("No decoded text created")
    else:
        filename = input("Name of the file: ")
        try:
            if lzw == False:
                with open(filename, "w", encoding="utf-8") as file:
                    file.write(decoded_file)
            else:
                with open(filename, "wb") as file:
                    file.write(bytes(decoded_file))
            print("Success")
        except:
            print("Error")

def save_code():
    print("Save code")
    global code
    if code == "":
        print("No code created")
    else:
        filename = input("Name of the file: ")
        try:
            with open(filename, "w", encoding="utf-8") as file:
                for c in code:
                    if lzw == False:
                        file.write(f"{repr(c[0])}\t{c[1]}\t{c[2]}\n")
                    else:
                        file.write(f"{c[0][0]}\t{c[1]}\n")
            print("Success")
        except:
            print("Error")

def switch_coding_11():
    global binary, huffman, lzw
    if binary:
        print("Switching to Huffman")
        binary = False
        huffman = True
        lzw = False
    else:
        print("Switching to fixed-length binary")
        binary = True
        huffman = False
        lzw = False

def switch_coding_12():
    global binary, huffman, lzw
    if lzw:
        print("Switching to Huffman")
        binary = False
        huffman = True
        lzw = False
    else:
        print("Switching to lzw")
        binary = False
        huffman = False
        lzw = True

def clear_environment():
    print("Clear environment")
    global original_file, encoded_file, code, decoded_file
    original_file = ""
    encoded_file = ""
    code = ""
    decoded_file = ""
    print("All data cleared")

if __name__ == "__main__":
    while(1):
        decision = dialog()
        if decision == "1":
            load_original()
        elif decision == "2":
            load_encoded()
        elif decision == "3":
            load_code()
        elif decision == "4":
            encode_file()
        elif decision == "5":
            decode_file()
        elif decision == "6" and lzw == False:
            create_code()
        elif decision == "7":
            save_encoded()
        elif decision == "8":
            save_decoded()
        elif decision == "9":
            save_code()
        elif decision == "10":
            clear_environment()
        elif decision == "11":
            switch_coding_11()
            clear_environment()
        elif decision == "12":
            switch_coding_12()
            clear_environment()
        elif decision == "13":
            sys.exit()
        else:
            print("Unknow command")