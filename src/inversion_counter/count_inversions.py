
import argparse

def main(filename):
    num_list = []
    with open(filename, 'r') as fp:
        for row in fp:
            num_list.append(int(row))

    sorted_list, inversions = sort_and_count(num_list, len(num_list))
    print('sorted', sorted_list)
    print('inversions', inversions)
        
def sort_and_count(num_list, length):
    if length <= 1:
        return num_list, 0
    else:
        mid_point = length // 2
        l_half = num_list[:mid_point]
        r_half = num_list[mid_point:]

        l_sorted, l_count = sort_and_count(l_half, len(l_half))
        r_sorted, r_count = sort_and_count(r_half, len(r_half))
        s_sorted, s_count = merge_and_count_split(l_sorted, r_sorted, len(l_sorted) + len(r_sorted))

        return s_sorted, l_count + r_count + s_count

def merge_and_count_split(l_array, r_array, length):
    split_inversions = 0
    merged_array = []
    left = l_array[:]
    right = r_array[:]

    for _k in range(length):
        if left and right:
            if left[0] < right[0]:
                merged_array.append(left.pop(0))
            else:
                merged_array.append(right.pop(0))
                split_inversions += len(left)
        elif left:
            merged_array.append(left.pop(0))
        else:
            merged_array.append(right.pop(0))
            split_inversions += len(left)

    return merged_array, split_inversions
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Inversions')
    parser.add_argument('-f', '--filename', required=True)
    args = parser.parse_args()
    main(args.filename)
