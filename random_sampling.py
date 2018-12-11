import random
import matplotlib.pyplot as plt
import numpy as np
import json
import operator
import sys

count = {}


def parse_input_file(file_name):
    cum_freq = []
    total = 0
    input_map = {}
    with open(file_name) as input:
        for num, line in enumerate(input):
            input_map[num] = line
            total += int(line.split()[1])
            cum_freq.append(total)
    return cum_freq, total, input_map

    
def get_index(cum_frequency, fre_val):
    start = 0
    end = len(cum_frequency) - 1
    while (start < end):
        mid = int((end + start)/2)
        if fre_val <= cum_frequency[mid] and mid > 0 and fre_val > cum_frequency[mid - 1]:
            return mid
        elif fre_val > cum_frequency[mid]:
            start = mid + 1
        else:
            end = mid - 1
    return start


def sample(cum_frequency, total, sample_points):
    sample_dict = {}
    sample_cut_off_index = 0
    sample_cut_off_value = 0
    for x in range(sample_points):
        rand_fre_value = int(random.randrange(total))
        index = get_index(cum_frequency, rand_fre_value)
        if (sample_dict.__contains__(int(index))):
            sample_dict[index] = int(sample_dict.get(index)) + 1
            if (sample_dict[index] > sample_cut_off_value):
                sample_cut_off_value = sample_dict[index]
                sample_cut_off_index = index
        else:
            sample_dict[index] = 1


    if (count.__contains__(int(sample_cut_off_index))):
        count[sample_cut_off_index] = int(count.get(sample_cut_off_index)) + 1
    else:
        count[sample_cut_off_index] = 1




def main():
    file_name = sys.argv[1]
    cum_freq, total, input_mapping = parse_input_file(file_name)
    num_lines = sum(1 for line in open(file_name))

    for x in range(1000):
        print("Round - " + str(x))
        sample(cum_freq, total, int(num_lines/10))
    

    print("Sampled cut-offs  are - " + str(json.dumps(count)))

    promising_cut_off_key = max(count.items(), key=operator.itemgetter(1))[0] 
    robust_cut_off_key = sorted(count.keys())[-1]

    print("Promising cut-off - " + str(promising_cut_off_key) + " - " + str(input_mapping[promising_cut_off_key]))
    print("Robust cut-off - " + str(robust_cut_off_key) + " - " + str(input_mapping[robust_cut_off_key]))
    
    
    rank = []
    frequency = []
    entry_num = 1
    for entry in sorted(count):
        rank.append(entry_num)
        entry_num += 1
        frequency.append(count[entry])

    plt.title("Barcode Frequency Distribution")
    plt.ylabel("Frequency")
    plt.xlabel("Rank")
    plt.plot(rank, frequency)
    plt.show()
    



if __name__ == "__main__":
    main()
