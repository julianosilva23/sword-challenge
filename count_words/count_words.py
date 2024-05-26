import time
import string
from multiprocessing import Pool

class CountWords:
    def __init__(self, file_path) -> None:
        self.file_path = file_path

    def is_number(self, string_test:str) -> bool:
        try:
            int(string_test)
            float(string_test)

            return True
        except ValueError:
            return False


    def process_line(self, line:list):
        local_bag_of_words = {}
        tokens = line.split()

        for token in tokens:

            token = token.translate(str.maketrans('', '', string.punctuation)).lower()
            token = token.translate(str.maketrans('', '', string.digits))
            token = token.translate(str.maketrans('', '', '°•ªº′'))

            if self.is_number(token):
                continue

            if len(token.strip()) == 0:
                continue

            if token not in local_bag_of_words:
                local_bag_of_words[token] = 0

            local_bag_of_words[token] += 1
        return local_bag_of_words

    def read_lines(self, block_size=100):
        with open(self.file_path, mode="r") as file:
            for line in file:
                    yield line

def merge_dicts(dict_list:dict) -> dict:
    final_bag_of_words = {}
    for d in dict_list:
        for key, value in d.items():
            if key not in final_bag_of_words:
                final_bag_of_words[key] = 0
            final_bag_of_words[key] += value
    return final_bag_of_words

def quick_sort_desc(items):
    if len(items) <= 1:
        return items

    pivot = items[len(items) // 2][1]
    left = [(k, v) for k, v in items if v > pivot]
    middle = [(k, v) for k, v in items if v == pivot]
    right = [(k, v) for k, v in items if v < pivot]

    return quick_sort_desc(left) + middle + quick_sort_desc(right)

def sort_dict_by_value(d):
    items = list(d.items())
    sorted_items = quick_sort_desc(items)
    return dict(sorted_items)
    

file_path = 'database/input/wikipedia_brasil.txt'

count_words = CountWords(file_path=file_path)

start_time = time.time()

lines = list(count_words.read_lines())

with Pool(10) as p:
    results = p.map(count_words.process_line, lines)

final_bag_of_words = sort_dict_by_value(merge_dicts(results))

file_name = file_path.split('/')[-1]
with open(f'database/output/occurrence_words_{file_name}.txt', 'w') as text_file:
    text_file.write('word occurrence\n')

    for word, ocurrence in final_bag_of_words.items():
        text_file.write(f'{word} {ocurrence}\n')
    
end_time = time.time()
execution_time = end_time - start_time
print(f"Tempo de execução: {execution_time:.4f} segundos")
# Tempo de execução: 0.0032 segundos
# Tempo de execução: 0.0365 segundos