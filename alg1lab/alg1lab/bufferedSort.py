from basicSort import Sorter
import os
import math

class BufferedSorter(Sorter):
    def __init__(self, path_a: str, path_b: str, path_c: str, n: int):
        #n - кількість чисел в буфері
        super().__init__(path_a, path_b, path_c)
        self.iteration = 0  #ітерація
        self.split_n = 1  #кількість частин записаних у функції розділення
        self.n = n  #кількість чанків в буфері
        try:
            self.iter_max = math.ceil(math.log2(os.stat(self.path_a).st_size / 32 / self.n))
        except ValueError:
            self.iter_max = 1
        except FileNotFoundError:
            self.iter_max = 1

    def create_random_file(self, n: int, max_n: int):       #створення файла
        super().create_random_file(n, max_n)
        self.iter_max = math.ceil(math.log2(os.stat(self.path_a).st_size / 32 / self.n))

    def copy_from_file(self, path: str):                    #копіювання файла
        super().copy_from_file(path)
        self.iter_max = math.ceil(math.log2(os.stat(self.path_a).st_size / 32 / self.n))

    def buffered_sort(self):
        self._buffered_prepare()
        for _ in range(self.iter_max):
            self._buffered_distribute()
            self._buffered_merge()
            self.iteration += 1
            self.split_n *= 2
        self.iteration = 0
        self.split_n = 1

    def _buffered_prepare(self):
        """Зчитати частинами файл А, записати відсортовані частини у тимчасовий файл, скопіювати до файла A"""
        tmp = open("tmp", "wb")
        a = open(self.path_a, "rb")
        buffer = []
        for _ in range(self.n):
            x = a.read(32)
            if not x:
                break
            buffer += x,
        while buffer:
            buffer.sort()
            for x in buffer:
                tmp.write(x)
            del buffer
            buffer = []
            for _ in range(self.n):
                x = a.read(32)
                if not x:
                    break
                buffer += x,
        tmp.close()
        a.close()
        self.copy_from_file("tmp")
        os.remove("tmp")

    def _buffered_distribute(self):
        #Розподілення між файлами частинами розміру n на 2**ітерація в рядок
        a = open(self.path_a, "rb")
        b = open(self.path_b, "wb")
        c = open(self.path_c, "wb")
        i = True
        j = 1
        while True:
            for _ in range(self.n):
                x = a.read(32)
                if not x:
                    a.close(), b.close(), c.close()
                    return
                b.write(x) if i else c.write(x)
            j += 1
            if j > self.split_n:
                i = not i
                j = 1

    def _buffered_merge(self):
        #Уже відомо що ми маємо серії розміру n на 2**ітерація після розподілу, тому ми можемо не визначати кінець серії
        a = open(self.path_a, "wb")
        b = open(self.path_b, "rb")
        c = open(self.path_c, "rb")
        lim = self.n * self.split_n
        curr_b = b.read(32)
        curr_c = c.read(32)
        i_b = 0
        i_c = 0
        while i_b < lim or i_c < lim:
            if curr_b <= curr_c:
                a.write(curr_b)
                i_b += 1
                curr_b = b.read(32)
            else:
                a.write(curr_c)
                curr_c = c.read(32)
                i_c += 1
            #Якщо закінчились серії, то записуємо решту чисел з другого файла
            if i_b == lim:
                while i_c < lim:
                    a.write(curr_c)
                    curr_c = c.read(32)
                    i_c += 1
            elif i_c == lim:
                while i_b < lim:
                    a.write(curr_b)
                    i_b += 1
                    curr_b = b.read(32)
        while curr_b and curr_c:
            i_b = 0
            i_c = 0
            while i_b < lim or i_c < lim:
                if curr_b <= curr_c:
                    a.write(curr_b)
                    i_b += 1
                    curr_b = b.read(32)
                else:
                    a.write(curr_c)
                    curr_c = c.read(32)
                    i_c += 1
                if i_b == lim:
                    while i_c < lim:
                        a.write(curr_c)
                        curr_c = c.read(32)
                        i_c += 1
                elif i_c == lim:
                    while i_b < lim:
                        a.write(curr_b)
                        i_b += 1
                        curr_b = b.read(32)
        #Запис серії, що залишилась
        while curr_b:
            a.write(curr_b)
            curr_b = b.read(32)
        #Запис серії, що залишилась
        while curr_c:
            a.write(curr_c)
            curr_c = c.read(32)

        a.close(), b.close(), c.close()

