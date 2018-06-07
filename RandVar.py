import random
import math

class RandVar:

    @staticmethod
    def exp(lam):
        '''Inverse transform sampling'''
        return math.log(1 - random.random()) / -lam

    @staticmethod
    def customDistr(table):
        '''Inverse transform sampling'''
        
        if not RandVar.checkTable(table):
            print "not a valid table"
            return

        cumSum = [0] * len(table)
        cumSum[0] = table[0][1]
        for i in range(1, len(table)):
            cumSum[i] = table[i][1] + cumSum[i - 1]

        y = random.random()
        for j in range(len(table)):
            if y < cumSum[j]:
                x = table[j][0]
                break
        return x


    @staticmethod
    def checkTable(table):
        if not isinstance(table, list):
            return False

        else:
            for i in table:
                if not isinstance(i, list) or len(i) != 2 or not isinstance(i[0], float) or not isinstance(i[1], float):
                    return False

        sumProb = 0
        currVal = float('-inf')
        for i in table:
            if i[0] > currVal:
                currVal = i[0]
                sumProb += i[1]

            else:
                return False

        if sumProb == 1:
            return True
        else:
            return False
'''
def main():
    x = [[5 ,0.03], [10, 0.13], [20, 0.22], [40, 0.12], [70, 0.17], [100, 0.08], [110, 0.20], [115, 0.05]]
    y = RandVar.customDistr(x)
    print y
    a = 0
    for i in y:
        if i == 5:
            a += 1
    print a
    plt.hist(y, 120, normed = True)
    plt.show()

main()
'''
