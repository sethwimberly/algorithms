'''
Created on Aug 25, 2013

@author: Seth Wimberly
'''
import argparse


def q_sort(array, start, length, pivot_function):
    '''
    Quicksort:
    @param array: an array containing all elements of the array to be sorted
    @param start: The index of the first element of the array or sub-array to be sorted
    @param length: The length of the array or sub-array
    @param pivot_function: The function to be used in calculating the pivot
    @return: The number of comparison made in this recersive call and all subsequent recursive calls
    '''

    # if the lenght of the array is 1 return 0, (Base Case)
    if length == 1:
        return 0

    end_index = start + length - 1

    # determine pivot
    pivot_index = pivot_function(array, start, end_index)

    # move the pivot to the front of the array
    swap(array, pivot_index, start)
    pivot_index = partition(array, start, end_index)

    # initialize count to be the number of comparisons made at this step
    count = end_index - start

    left_half_length = pivot_index - start
    if left_half_length > 0:
        # if the length of the left half is greater than 0 recurse on the left side
        count += q_sort(array, start, left_half_length, pivot_function)

    right_half_length = end_index - pivot_index
    if right_half_length > 0:
        # if the length of the right half is greater than 0 recurse on the right side
        count += q_sort(array, pivot_index + 1, right_half_length, pivot_function)

    return count


def partition(array, start, end):
    '''
    Partition the array based on the pivot value in the start position.
    ie. move everything less than the pivot to the front of the array, 
    then swqp the pivot and the last value smaller than it
    @param array: the entire array
    @param start: where the sub array begins (also the position of the pivot value)
    @param end: the index of the last value in the array
    '''
    partition_value = array[start]
    partitioned_index = start + 1

    # loop each value starting with the value after the pivot
    for array_index in range(partitioned_index, end + 1):
        # if the current value is less than the pivot move it to the beginning of the array
        if array[array_index] < partition_value:

            swap(array, partitioned_index, array_index)
            partitioned_index += 1

    # move the pivot value to the proper position
    swap(array, start, partitioned_index - 1)
    return partitioned_index - 1


def choose_pivot_first(array, start, end):
    return start


def choose_pivot_last(array, start, end):
    return end


def choose_pivot_median(array, start, end):
    '''
    Chooses a pivot value based on the median of the first, last and middle element in the array
    if first = 7, middle = 2, and last = 5, the median of {2, 5, 7} or 5 will be returned
    @param array: the array
    @param start: the index of the first element in the the subarray
    @param end: the index of the last element in the subarray
    '''
    middle_offset = (end - start) // 2

    middle_index = start + middle_offset
    first = array[start]
    last = array[end]
    middle = array[middle_index]

    median_opts = [first, middle, last]
    median_val = sorted(median_opts)[1]
    median_index = start

    if middle == median_val:
        median_index = middle_index
    elif last == median_val:
        median_index = end

    return median_index


def swap(array, index1, index2):
    '''
    Swap two values in an array
    @param array: the array
    @param index1: the index of the first element to be swapped
    @param index2: the index of the second element to be swapped
    @return: None
    '''
    tmp = array[index1]
    array[index1] = array[index2]
    array[index2] = tmp


def main(filename, pivot_num=0):
    num_list = []
    with open(filename, 'r') as fp:
        for row in fp:
            num_list.append(int(row))
    print('sorting', num_list)
    pivot_functions = [choose_pivot_first, choose_pivot_median, choose_pivot_last]
    comp = q_sort(num_list, 0, len(num_list), pivot_functions[pivot_num])
    print(num_list)
    print(comp)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='QuickSort')
    parser.add_argument('-f', '--filename', required=True)
    parser.add_argument('-p', '--pivot-num', default=0, type=int,
                        help='The index of the pivot to choose from the list [choose_pivot_first, choose_pivot_median, choose_pivot_last]')
    args = parser.parse_args()
    main(args.filename, args.pivot_num)
