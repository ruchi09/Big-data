from pyspark.mllib.tree import DecisionTree, DecisionTreeModel
from pyspark.mllib.classification import NaiveBayes, NaiveBayesModel
from pyspark.mllib.util import MLUtils
from pyspark import SparkContext


def NaiveBayes_classification(training,test):
    print "\n\n-----------------------------------------------------------------------------"
    print "          Naive Bayes"
    print "-----------------------------------------------------------------------------\n\n"

    # Train a naive Bayes model.
    model = NaiveBayes.train(training, 1.0)

    # Make prediction and test accuracy.
    predictionAndLabel = test.map(lambda p: (model.predict(p.features), p.label))
    accuracy = 1.0 * predictionAndLabel.filter(lambda pl: pl[0] == pl[1]).count() / test.count()
    print('model accuracy {}'.format(accuracy))




def DecisionTree_classifier(trainingData,testData):
    print "\n\n-----------------------------------------------------------------------------"
    print "          Decision tree"
    print "-----------------------------------------------------------------------------\n\n"

    model = DecisionTree.trainClassifier(trainingData, numClasses=2, categoricalFeaturesInfo={},
                                     impurity='gini', maxDepth=5, maxBins=32)

    # Evaluate model on test instances and compute test error
    predictions = model.predict(testData.map(lambda x: x.features))
    labelsAndPredictions = testData.map(lambda lp: lp.label).zip(predictions)
    testErr = labelsAndPredictions.filter(
        lambda lp: lp[0] != lp[1]).count() / float(testData.count())
    print('Test Error = ' + str(testErr))
    print('Learned classification tree model:')
    print(model.toDebugString())





if __name__ =="__main__":
    sc = SparkContext("local", "first app")
    # Load and parse the data file.
    data = MLUtils.loadLibSVMFile(sc, "./sample_libsvm_data.txt")

    # Split data approximately into training (60%) and test (40%)
    training, test = data.randomSplit([0.6, 0.4])


    NaiveBayes_classification(training,test)
    DecisionTree_classifier(training,test)
