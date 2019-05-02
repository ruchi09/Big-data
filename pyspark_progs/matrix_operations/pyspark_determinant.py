#!/usr/bin/python


from pyspark import SparkContext
from pyspark.mllib.linalg import Matrix, Matrices



def determinant(rows,mat):
    if rows<=0:
        return "invalid"
    else:
        if rows ==1:
            return mat[0]
        elif rows==2:
            mat = mat.toArray()
            # print "dsjfgbi", mat
            return mat[0][0]*mat[1][1] - mat[1][0]*mat[0][1]
        else:
            sum=0
            mat = mat.toArray()
            for i in range(0,rows):
                matrix = []
                for j in range(0,rows):
                    for k in range(1,rows):
                        if j!=i:
                            matrix.append(mat[k][j])

                # print matrix, rows
                matrix = Matrices.dense(rows-1,rows-1,matrix)

                # print "siudfoi",i,matrix.toArray()
                # print "--------------------------"
                # print "mat[0,i] =",mat[0][i]
                # print "deter =",determinant(rows-1,matrix)
                if i%2==0:
                    sum=sum + mat[0][i] * determinant(rows-1,matrix)
                else:
                    sum=sum - mat[0][i] * determinant(rows-1,matrix)
                # print sum

            return sum





# calculates and accumelates partial determinant with given first row element
def dist_deter(i):
    global mat
    global rows
    global det
    # sum = 0
    matrix = []
    # mat = mat.toArray()
    for j in range(0,rows):
        for k in range(1,rows):
            if j!=i:
                # z=0
                # print mat[k][j]
                matrix.append(mat[k][j])

    # print matrix, rows
    matrix = Matrices.dense(rows-1,rows-1,matrix)

    # print "siudfoi",i,matrix.toArray()
    # print "--------------------------"
    # print "mat[0,i] =",mat[0][i]
    # print "deter =",determinant(rows-1,matrix)

    sum = mat[0][i] * determinant(rows-1,matrix)
    if i%2==0:
        det+=sum
    else:
        det+=(0-sum)



if __name__ =="__main__":

    global rows
    global mat
    rows=3

    sc = SparkContext("local", "Determinant")

    # accumulator variable to accumulate final determinant value
    det = sc.accumulator(0)

    # dense matrix returns matrix in column major format hence
    # the entered values itself is fiven in column major so that
    # we can finally have a  row major matrix to operate on
    dm2 = Matrices.dense(rows, rows, [2,7,3,3,7,8,5,8,5])

    print "\n\nEntered matrix:\n", dm2.toArray()

    #here we are trying to divide work between workers. we divide first row
    # between them (calculate partial determinant for each item in first row)
    cols = sc.parallelize([i for i in range(0,rows)])

    mat =dm2.toArray()


    cols.foreach(dist_deter)

    # print "determinant", determinant(3,dm2) #to check correctness
    print "\n The determinant is:",det.value
