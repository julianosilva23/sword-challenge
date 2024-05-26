import json
import random
import time
from datetime import datetime, timedelta
from pyspark.sql import SparkSession
import pyspark.sql.types as T
from multiprocessing import Pool

start_time = time.time()

def process_line(line):
    bag_of_words = {}
    tokens = line.split(" ")

    for token in tokens:
        bag_of_words = count_words(bag_of_words, token)

    print(bag_of_words)

def read_lines(file_path):
    with open(file_path, mode="r") as file:
        for line in file:
            yield line

def count_words(bag_of_words, word):
    if word not in bag_of_words.keys():
        bag_of_words[word] = 0

    bag_of_words[word] = bag_of_words[word] + 1

    return bag_of_words

file_path = 'database/input/wikipedia_brasil.txt'

with Pool(10) as p:
    results = p.map(process_line, read_lines(file_path))

print(len(results))
end_time = time.time()

execution_time = end_time - start_time
print(f"Tempo de execução: {execution_time:.4f} segundos")
