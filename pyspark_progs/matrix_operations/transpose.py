from pyspark.mllib.linalg import Matrices
from pyspark.mllib.linalg.distributed import BlockMatrix
from pyspark import SparkContext
from pyspark.mllib.linalg.distributed import CoordinateMatrix, MatrixEntry
from pyspark.mllib.linalg.distributed import IndexedRow, IndexedRowMatrix
from pyspark.sql import SparkSession


def print_rowmat(mat):
    for i in range(0,mat.numRows()):
        print ""
        for j in range(0,mat.numCols()):
            print mat.rows.collect()[i][j],



sc = SparkContext("local","transpose")
spark = SparkSession(sc)

indexedRows = sc.parallelize([(0, [1, 2, 3]), (1, [4, 5, 6]),
                              (2, [7, 8, 9]), (3, [10, 11, 12])])

hasattr(indexedRows, "toDF")
# Create an IndexedRowMatrix from an RDD of IndexedRows.
mat = IndexedRowMatrix(indexedRows).toCoordinateMatrix()

print "\n\nMatrix:\n"
print_rowmat(mat.toRowMatrix())
print "\n\n Transpose:\n"
print_rowmat( mat.transpose().toRowMatrix())
