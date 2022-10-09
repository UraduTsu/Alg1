from bufferedSort import BufferedSorter
import time
import pickle

def main(numbersNumber):
    sorter = BufferedSorter("a.bin", "b.bin", "c.bin", 1024**3//16)
    sorter.create_random_file(1024**3//32, 10**6)
    sortTime = time.time()
    sorter.buffered_sort()
    print("Sorting time: " , time.time() - sortTime, "seconds")

def uselessFunc():
    with open("a.bin", "rb") as fileA:
        for _ in range (100):
            if int.from_bytes(fileA.read(32), byteorder="big") != 0:
                print("\t", int.from_bytes(fileA.read(32), byteorder="big"), end = "")
        print("")
def stupidFunc():
    cheeseFlag = input('Type "cheese" if you want to create and sort a file: ')
    if cheeseFlag == "cheese":
        numbersNumber = input('Type number of numbers in file: ')
        main(numbersNumber)
    cheeseFlag2 = input('Type "cheese" if you want to show 100 first elements of file: ')
    if cheeseFlag2 == "cheese":
        uselessFunc()
    cheeseFlag3 = input('Type "cheese" if you run program again: ')
    if cheeseFlag3 == "cheese":
        stupidFunc()

stupidFunc()