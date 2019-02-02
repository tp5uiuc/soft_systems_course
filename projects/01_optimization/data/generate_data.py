__doc__ = """Python script for generating the data needed for solving the knapsack problem
given as part of problem 1 in the 2019_cmo project 1"""

import numpy as np

N_ITEMS = 50
NU = 10
RAND = 5.0


# Part one : Generate random data, with knapsack capacity = 2 * NU
def gen_one_data(fname):
    item_weights = np.random.randint(low=1, high=NU + 1, size=N_ITEMS)
    item_values = np.random.randint(low=1, high=NU + 1, size=N_ITEMS)
    bag_capacity = 2 * NU
    n_items = N_ITEMS

    # print(item_weights, item_values, bag_capacity)
    np.savez(
        fname,
        capacity=bag_capacity,
        n_items=N_ITEMS,
        item_values=item_values,
        item_weights=item_weights)


# Part two : Generate correlated data with knapsack capacity  = 0.5 * sigma(W)
def gen_two_data(fname):
    item_weights = np.random.randint(low=1, high=NU + 1, size=N_ITEMS)
    item_values = item_weights + RAND
    bag_capacity = 0.5 * np.sum(item_weights)

    # print(item_weights, item_values, bag_capacity)

    np.savez(
        fname,
        capacity=bag_capacity,
        n_items=N_ITEMS,
        item_values=item_values,
        item_weights=item_weights)


def load_data(fname):
    """ Loads to see whether the data is right"""

    temp_dict = np.load(fname)
    for key, val in temp_dict.items():
        print(key, val)


def main():
    # Call the functions to generate the data here
    one_file_name = 'A'

    # gen_one_data(one_file_name)
    load_data(one_file_name + '.npz')

    two_file_name = 'B'

    # gen_two_data(two_file_name)
    load_data(two_file_name + '.npz')


if __name__ == '__main__':
    main()
