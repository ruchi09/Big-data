import pandas, scipy, numpy
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import Binarizer
from sklearn.preprocessing import StandardScaler
from sklearn import preprocessing
from sklearn.preprocessing import add_dummy_feature

df=pandas.read_csv( 'http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv ',sep=';')
array=df.values
#Separating data into input and output components
x=array[:,0:8]
y=array[:,8]

print("Min-max scaling")
print("Before min-max scaling")
print(x[0:5,:])
scaler=MinMaxScaler(feature_range=(0,1))
rescaledX=scaler.fit_transform(x)
numpy.set_printoptions(precision=3) #Setting precision for the output
print("After min-max scaling")
print(rescaledX[0:5,:])

print(" ")
print("Binarizing")
X = [[ 1., -1.,  2.],
[ 2.,  0.,  0.],
[ 0.,  1., -1.]]
print("Original data")
print(X)
transformer = Binarizer().fit(X)
print("After Binarizing")
print(transformer.transform(X))

print("  ")
print("Standardizing data")
data = [[0, 0], [0, 0], [1, 1], [1, 1]]
print("original data")
print(data)
scaler = StandardScaler()
scaler.fit(data)
print("Mean of the data")
print(scaler.mean_)
print("Standardized data")
print(scaler.transform(data))

print(" ")
le = preprocessing.LabelEncoder()
print("Labels:")
print(["paris", "paris", "tokyo", "amsterdam"])
le.fit(["paris", "paris", "tokyo", "amsterdam"])

print("Encodings for \n tokyo,amsterdam,paris::")
print(le.transform(["tokyo", "amsterdam", "paris"]) )

print("")
print("Adding dummy feature")


X = [[0,1],[1,1]]
print("Data :")
print(X)
print("adding dummy feature with value 5")
X=add_dummy_feature(X,value=5.0)
print(X)
