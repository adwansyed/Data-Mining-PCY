# -*- coding: utf-8 -*-
"""
@title: PCY
@author: Adwan Salahuddin Syed
"""

# import libraries
import time
import itertools

pairs_hashtable = {}
frequent_pairs = {}
num_buckets = 10
num_baskets = 10
support_threshold = 0.2
bitmap = [0]*num_buckets

# Hash function for frequent pairs hash table
def hash_pair(n1, n2):
    return ((n1*n1) + (n2*n2)) % num_buckets

def pcy(baskets, tHold, start):

##### PASS 1 ###################################################################

    # Generate singletons with counts
    singletons = {}
    for transaction in baskets:
        for item in transaction.split():
            if item not in singletons:
                singletons[item] = 1
            else:
                singletons[item] += 1

    # Prune frequent_single_items from singletons
    frequent_single_items = {}
    for key in singletons:
        if singletons[key] > (len(baskets) * tHold):
            frequent_single_items[key] = singletons[key]

    # Store frequent_singletons to prepare for data manipulation on list
    frequent_singletons = []
    for key in frequent_single_items:
        for item in key.split(','):
            if item not in frequent_singletons:
                frequent_singletons.append(item)

    for key in itertools.combinations(frequent_singletons, 2):
        # hash function taking input key and putting in a map
        hash_value = hash_pair(int(key[0]), int(key[1]))
        if hash_value in pairs_hashtable:
            pairs_hashtable[hash_value] = pairs_hashtable[hash_value] + 1
        else:
            pairs_hashtable[hash_value] = 1

##### BETWEEN PASSES ###########################################################

    for key in sorted(pairs_hashtable.keys()):
        if pairs_hashtable[key] >= 2:
            bitmap[key] = 1

##### PASS 2 ###################################################################

    for i in range(0, len(frequent_singletons)):
        for j in range(i+1, len(frequent_singletons)):
            hash_value = hash_pair(int(frequent_singletons[i]), int(frequent_singletons[j]))
            if bitmap[hash_value] > 0:
                # add pair
                candidate_pair = frequent_singletons[i] + ", " + frequent_singletons[j]
                if candidate_pair not in frequent_pairs:
                    frequent_pairs[candidate_pair] = 0
                else:
                    frequent_pairs[candidate_pair] = frequent_pairs[candidate_pair] + 1

    print(frequent_pairs)

    # Display timestamp
    print (" ")
    print(time.time()-start, ': Generated frequent pairs')

#-------------------------------------------------------------------------------

# Runs pcy on file with designated baskets. Records timestamps
def run(tHold, num_baskets, file_name):

    dataset_file = file_name
    num_lines = sum(1 for line in open(dataset_file))
    print('Number of lines: ', num_lines)

    basket_size = num_lines/num_baskets
    print('Basket size: ', basket_size)

    list_of_baskets = []
    basket = []

    count = 0 # Counter
    basket_count = 0
    with open(dataset_file) as file:
        for line in file:
            basket.append(line)
            if count > basket_size:
                list_of_baskets.append(basket)
                basket.clear()
                basket.append(line)
                basket_count+=1
                count = 0
            count+=1
        list_of_baskets.append(basket)
        basket_count+=1
    print('Number of baskets: ', len(list_of_baskets))

    total_time = 0
    for i in range (0, len(list_of_baskets)):
        # Start the clock
        start = time.time()
        pcy(list_of_baskets[i], tHold, start)
        end = time.time()
        print('Time taken in seconds for basket %d: ' % (i), end - start)
        total_time += (end - start)
    print('Total time taken to run: ', total_time)


run(support_threshold, num_baskets, 'retail.dat')
#run(support_threshold, num_baskets, 'netflix.data')
