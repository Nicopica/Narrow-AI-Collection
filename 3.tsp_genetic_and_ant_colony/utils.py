import sys
from math import sqrt

from Assignment3.Location import Location

DATA_PATH = "data/berlin52.txt"

def readData(path):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return file.readlines()

    except FileNotFoundError:
        exit(f"Error: The file '{path}' was not found.")

def get_locations():
    raw_data = readData(DATA_PATH)
    # just some formating. list[list[int]]
    return [[int(float(elem.strip())) for elem in line] for line in [line.split() for line in raw_data]]




