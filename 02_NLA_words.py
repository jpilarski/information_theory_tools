import sys
import random
from collections import defaultdict, Counter

def validate_arguments():
    if len(sys.argv) != 4:
        print("Use: python 02_NLA_words.py \"corpus.txt\" \"number of characters at the output\" \"output.txt\"")
        exit(1)
    arg_input = sys.argv[1]
    arg_size = sys.argv[2]
    arg_output = sys.argv[3]
    args = []
    try:
        with open(arg_input, "r", encoding="utf-8") as file:
            text = file.read()
            words = text.split()
            args.append(words)
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

if __name__ == "__main__":
    data = validate_arguments()
    words = data[0]
    out_size = data[1]
    out_file = data[2]
    words_counter = Counter(words)
    sorted = words_counter.most_common()
    one_word = defaultdict(Counter)
    two_words = defaultdict(Counter)
    for i in range(len(words)-2):
        current = words[i]
        next = words[i+1]
        one_word[current][next] += 1
        twos = (words[i], words[i+1])
        next = words[i+2]
        two_words[twos][next] += 1
    print("A) First-order approximation")
    print("B) Approximation based on first-order Markov source")
    print("C) Approximation based on second-order Markov source")
    choice = input("Choose method: ")
    if choice == "A":
        count = 0
        keys = list(words_counter.keys())
        weights = list(words_counter.values())
        print("Fifty most frequent words:")
        for i in range(50):
            print(f"\t{i+1}: {sorted[i][0]}: {sorted[i][1]} times, {round(100*sorted[i][1]/len(words), 2)}%")
        for i in range(6000):
            count += sorted[i][1]
        print(f"6000 most popular words is {round(100*count/len(words), 2)}% of all words")
        for i in range(6000, 30000):
            count += sorted[i][1]
        print(f"30000 most popular words is {round(100*count/len(words), 2)}% of all words")
        size = 0
        words_out = []
        while(size<out_size):
            words_out.append(random.choices(keys, weights=weights, k=1)[0])
            size = size + len(words_out[-1]) + 1
        with open(out_file, "w", encoding="utf-8") as f:
            for word in words_out:
                f.write(word)
                f.write(" ")
                print(f"{word} ", end="")
        exit()
    elif choice == "B":
        keys = list(words_counter.keys())
        weights = list(words_counter.values())
        words_out = []
        words_out.append(random.choices(keys, weights=weights, k=1)[0])
        size = len(words_out[-1]) + 1
        while(size<out_size):
            last = words_out[-1]
            keys = list(one_word[last].keys())
            weights = list(one_word[last].values())
            words_out.append(random.choices(keys, weights=weights, k=1)[0])
            size = size + len(words_out[-1]) + 1
        with open(out_file, "w", encoding="utf-8") as f:
            for word in words_out:
                f.write(word)
                f.write(" ")
                print(f"{word} ", end="")
        exit()
    elif choice == "C":
        keys = list(words_counter.keys())
        weights = list(words_counter.values())
        words_out = []
        words_out.append(random.choices(keys, weights=weights, k=1)[0])
        size = len(words_out[-1]) + 1
        last = words_out[-1]
        keys = list(one_word[last].keys())
        weights = list(one_word[last].values())
        words_out.append(random.choices(keys, weights=weights, k=1)[0])
        size = len(words_out[-1]) + 1
        while(size<out_size):
            last = (words_out[-2], words_out[-1])
            if last in two_words:
                keys = list(two_words[last].keys())
                weights = list(two_words[last].values())
                words_out.append(random.choices(keys, weights=weights, k=1)[0])
                size = size + len(words_out[-1]) + 1
            else:
                last = words_out[-1]
                keys = list(one_word[last].keys())
                weights = list(one_word[last].values())
                words_out.append(random.choices(keys, weights=weights, k=1)[0])
                size = size + len(words_out[-1]) + 1
        with open(out_file, "w", encoding="utf-8") as f:
            for word in words_out:
                f.write(word)
                f.write(" ")
                print(f"{word} ", end="")
        exit()