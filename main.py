"""
Даны две матрицы A и B размерности NxN. Необходимо вычислить их произведение: матрицу С.
C[i][j] = сумма по k от 1 до N A[i][k]*B[k][j].
Разработайте многопоточное приложение, выполняющее вычисление произведения матриц.
Элементы cij матрицы произведения С = A×B вычисляются параллельно p однотипными потоками.
Если некоторый поток уже вычисляет элемент cij матрицы C, то следующий приступающий к вычислению поток
выбирает для расчета элемент ci,j+1, если j<k, и ci+1,k, если j=k.
Выполнив вычисление элемента матрицы-произведения, поток проверяет, нет ли элемента, который еще не рассчитывается.
Если такой элемент есть, то приступает к его расчету.
В противном случае отправляет (пользовательское) сообщение о завершении своей работы и приостанавливает своё выполнение.
Главный поток, получив сообщения о завершении вычислений от всех потоков, выводит результат на экран и запускает поток,
записывающий результат в конец файла-протокола.
В каждом потоке должна быть задержка в выполнении вычислений (чтобы дать возможность поработать всем потокам).
Синхронизацию потоков между собой организуйте через критическую секцию или мьютекс.
Сделать диаграмму классов.
ДЗ сдается в виде ссылки на GitHub репозиторий с проектом.
Срок сдачи - 2 недели со дня занятия.
По вопросам обращаться в Slack к студентам, преподавателям и наставникам в канал группы

Критерии оценки:
1. Решение прислано в срок 1 балл
2. программа работает - 1 балл
3. Разработан тест - 1 балл

Минимальный балл для принятия - 2
"""

import time
import array
import threading

class MultithreadMultiplicator:
    mutex = threading.Lock()

    processing = 0
    elems = None

    def __init__(self, p=4):
        self.p = p

    def _multiply_thread(self, A, B):
        while True:
            with self.mutex:
                i = self.processing
                self.processing += 1

                if i >= A.size * A.size:
                    break

            # pause this thread
            time.sleep(0.5)
            
            row = A.get_row(i // A.size)
            col = B.get_col(i % A.size)
            el = sum([a * b for a, b in zip(row, col)])

            with self.mutex:
                self.elems[i] = el

    def multiply(self, A, B):
        if A.size != B.size:
            raise ValueError('Matrices must be the same size')

        self.elems = [0] * A.size * A.size

        # run threads
        threads = []
        for i in range(self.p):
            t = threading.Thread(target=self._multiply_thread, args=(A, B))
            threads.append(t)
            t.start()

        # wait while  threads
        for t in threads:
            t.join()

        return SquareMatrix(self.elems)
        
    
class SquareMatrix:
    def __init__(self, elems):
        self.size = int(len(elems)**0.5)

        if len(elems)**0.5 - self.size > 1e-15:
            raise ValueError('elements length must be NxN')

        self.elems = array.array('f', elems)

    def __str__(self):
        s = f'Matrix{self.size} ['
        for i, elem in enumerate(self.elems):
            if i % self.size == 0:
                s += '\n'
            s += f'{elem:>27.20f}'
        s += '\n]'
        return s

    def __eq__(self, other):
        return self.elems == other.elems
    

    def get_row(self, i):
        row_start = i * self.size
        return self.elems[row_start:row_start + self.size]

    def get_col(self, i):
        return self.elems[i::self.size]

    @staticmethod
    def read_csv(fname):
        elems = []
        with open(fname, 'rt') as f:
            for line in f:
                elems += map(float, line.split(','))
        return SquareMatrix(elems)

    def write_csv(self, fname):
        with open(fname, 'wt') as f:
            for i in range(self.size):
                f.write(','.join(map(str, self.get_row(i))) + '\n')


if __name__ == '__main__':
    # read data from std
    fst_file = input('first matrix file (mat1.csv): ') or 'mat1.csv'
    snd_file = input('second matrix file (mat2.csv): ') or 'mat2.csv'
    p = int(input('number of threads (4): ') or 4)

    A = SquareMatrix.read_csv(fst_file)
    print('First matrix is ', A)

    B = SquareMatrix.read_csv(snd_file)
    print('Second matrix is ', B)

    mul = MultithreadMultiplicator(p)
    print('computing...')
    C = mul.multiply(A, B)
    print('Result matrix is ', C)

    C.write_csv('result.csv')

