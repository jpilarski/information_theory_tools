import sys
import re
import random
import string

def validate_arguments():
    if len(sys.argv) != 4:
        print("Use: python 01_NLA_letters.py \"corpus.txt\" \"number of characters at the output\" \"output.txt\"")
        exit(1)
    
    arg_input = sys.argv[1]
    arg_size = sys.argv[2]
    arg_output = sys.argv[3]
    args = []

    try:
        with open(arg_input, "r", encoding="utf-8") as file:
            text = file.read()
            text = ' '.join(word for word in text.split() if word.isalpha() and word.islower())
            args.append(text)
    except:
        print("Wrong input file")
        exit(1)

    try:
        arg_size = int(arg_size)
        if arg_size <= 0:
            raise ValueError
        args.append(arg_size)
    except ValueError:
        print("The second argument must be a positive integer")
        exit(1)

    try:
        with open(arg_output, "w", encoding="utf-8"):
            pass
        args.append(arg_output)
    except:
        print("Wrong output file")
        exit(1)

    if arg_input == arg_output:
        print("The input file cannot be the output file")
        exit(1)

    return args

def average_length(text):
    words = text.split()
    if not words:
        return 0.0
    sum_chars = sum(len(word) for word in words)
    return sum_chars / len(words)

def decode_char(char):
    if char == ' ':
        return 0
    else:
        return ord(char) - 96

def print_percentage_1(chars, numbers):
    print()
    print("Occurence of individual characters:")
    print()
    sum_all = sum(numbers)
    for i in range(len(numbers)):
        percentage = round(numbers[i] / sum_all * 100, 5)
        print(f"\'{chars[i]}\': {percentage:.5f}%\t", end="")
        if i % 9 == 8:
            print()
    print()

def print_percentage_2(chars, matrix):
    print()
    print("Occurrence of the column character after the row character:")
    print()
    for char in chars:
        print(f"\t\'{char}\'", end="")
    print()
    for i in range(len(matrix)):
        print(f"\'{chars[i]}\'", end="")
        sum_row = sum(matrix[i])
        for j in range(len(matrix[i])):
            percentage = round(matrix[i][j] / sum_row * 100, 2)
            print(f"\t{percentage:.2f}%", end="")
        print()
    print()

def print_and_save(text, str_out, out_file):
    print()
    print(str_out)
    print()
    print(f"Average word length = {round(average_length(str_out), 2)}")
    print()
    print(f"Average word length in corpus = {round(average_length(text), 2)}")
    print()
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(str_out)
    exit()

if __name__ == "__main__":
    data = validate_arguments()
    text = data[0]
    out_size = data[1]
    out_file = data[2]

    print("Preparing data storage structures")
    str_out = ""
    characters = list(' ' + string.ascii_lowercase)
    length = len(text)
    power_1 = 27
    power_2 = 27**2
    power_3 = 27**3
    power_4 = 27**4
    power_5 = 27**5
    matrix_0 = [0] * 27
    matrix_1 = [[0] * 27 for _ in range(27)]
    matrix_3 = [[0] * 27 for _ in range(power_3)]
    matrix_5 = []
    for i in range(power_5):
        if i % (power_5 // 25) == 0:
            print(f"Progress = {(i * 100) // power_5}%")
        matrix_5.append([0] * 27)
    print("Structures created")
    print()

    print("Text processing")
    for i in range(length-5):
        if i % (length // 25) == 0:
            print(f"Progress = {(i * 100) // length}%")
        a = decode_char(text[i])
        b = decode_char(text[i+1])
        c = decode_char(text[i+2])
        d = decode_char(text[i+3])
        e = decode_char(text[i+4])
        f = decode_char(text[i+5])
        matrix_0[a] += 1
        matrix_1[a][b] += 1
        matrix_3[a*power_2+b*power_1+c][d] += 1
        matrix_5[a*power_4+b*power_3+c*power_2+d*power_1+e][f] += 1
    for i in range(length-5, length-3):
        a = decode_char(text[i])
        b = decode_char(text[i+1])
        c = decode_char(text[i+2])
        d = decode_char(text[i+3])
        matrix_0[a] += 1
        matrix_1[a][b] += 1
        matrix_3[a*power_2+b*power_1+c][d] += 1
    for i in range(length-3, length-1):
        a = decode_char(text[i])
        b = decode_char(text[i+1])
        matrix_0[a] += 1
        matrix_1[a][b] += 1
    matrix_0[decode_char(text[length-1])]
    print("Finished")
    print()

    print("A) Zero-order approximation")
    print("B) First-order approximation")
    print("C) Approximation based on first-order Markov source")
    print("D) Approximation based on third-order Markov source")
    print("E) Approximation based on fifth-order Markov source")
    choice = input("Choose method: ")
    
    if choice == "A":
        for _ in range(out_size):
            str_out += characters[random.randint(0, 26)]

    elif choice == "B":
        print_percentage_1(characters, matrix_0)

        for _ in range(out_size):
            str_out += random.choices(characters, weights=matrix_0, k=1)[0]
    
    elif choice == "C":
        print_percentage_2(characters, matrix_1)
        str_out += characters[random.randint(1, 26)]
        for _ in range(out_size-1):
            last = str_out[len(str_out)-1]
            temp_weights = matrix_1[decode_char(last)]
            if sum(temp_weights) > 0:
                str_out += random.choices(characters, weights=temp_weights, k=1)[0]
            else:
                str_out += random.choices(characters, weights=matrix_0, k=1)[0]
    
    elif choice == "D":
        str_out += "the"
        for _ in range(out_size-3):
            a = decode_char(str_out[len(str_out)-3])
            b = decode_char(str_out[len(str_out)-2])
            c = decode_char(str_out[len(str_out)-1])
            id = a * power_2 + b * power_1 + c
            temp_weights = matrix_3[id]
            if sum(temp_weights) > 0:
                str_out += random.choices(characters, weights=temp_weights, k=1)[0]
            else:
                temp_weights = [0] * 27
                for i in range(27):
                    for j in range(27):
                        temp_weights[j] += matrix_3[i*power_2+b*power_1+c][j]
                if sum(temp_weights) > 0:
                    str_out += random.choices(characters, weights=temp_weights, k=1)[0]
                else:
                    temp_weights = matrix_1[c]
                    if sum(temp_weights) > 0:
                        str_out += random.choices(characters, weights=temp_weights, k=1)[0]
                    else:
                        str_out += random.choices(characters, weights=matrix_0, k=1)[0]

    elif choice == "E":
        str_out += "probability"
        for _ in range(out_size-11):
            a = decode_char(str_out[len(str_out)-5])
            b = decode_char(str_out[len(str_out)-4])
            c = decode_char(str_out[len(str_out)-3])
            d = decode_char(str_out[len(str_out)-2])
            e = decode_char(str_out[len(str_out)-1])
            id = a * power_4 + b * power_3 + c * power_2 + d * power_1 + e
            temp_weights = matrix_5[id]
            if sum(temp_weights) > 0:
                str_out += random.choices(characters, weights=temp_weights, k=1)[0]
            else:
                temp_weights = [0] * 27
                for i in range(27):
                    for j in range(27):
                        temp_weights[j] += matrix_5[i*power_4+b*power_3+c*power_2+d*power_1+e][j]
                if sum(temp_weights) > 0:
                    str_out += random.choices(characters, weights=temp_weights, k=1)[0]
                else:
                    id = c * power_2 + d * power_1 + e
                    temp_weights = matrix_3[id]
                    if sum(temp_weights) > 0:
                        str_out += random.choices(characters, weights=temp_weights, k=1)[0]
                    else:
                        temp_weights = [0] * 27
                        for i in range(27):
                            for j in range(27):
                                temp_weights[j] += matrix_3[i*power_2+d*power_1+e][j]
                        if sum(temp_weights) > 0:
                            str_out += random.choices(characters, weights=temp_weights, k=1)[0]
                        else:
                            temp_weights = matrix_1[e]
                            if sum(temp_weights) > 0:
                                str_out += random.choices(characters, weights=temp_weights, k=1)[0]
                            else:
                                str_out += random.choices(characters, weights=matrix_0, k=1)[0]
    else:
        exit()

    print_and_save(text, str_out, out_file)