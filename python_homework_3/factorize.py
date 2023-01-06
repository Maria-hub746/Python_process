import multiprocessing
from multiprocessing import cpu_count
from time import time


def factorize(*number):
    cpu = multiprocessing.cpu_count()
    result_counts = []
    with multiprocessing.Pool(cpu) as pool:
        return pool.map(factorize_count, number)

def factorize_count(number):
    result_counts = []
    for i in range(1, number + 1):
        if number % i == False:
            result_counts.append(i)
    print(f'{number}: {result_counts}')


if __name__ == '__main__':
    timer = time()
    factorize(128, 255, 99999, 10651060)
    print(f'Done {time() - timer}')