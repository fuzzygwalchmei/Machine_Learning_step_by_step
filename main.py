from pandas import read_csv
from pandas.plotting import scatter_matrix
from matplotlib import pyplot
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

# Load dataset
url = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/iris.csv'
names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
dataset = read_csv(url, names=names)

pyplot.style.use('ggplot')

# Sumarise the Dataset
# Shape
print('Shape')
print(dataset.shape)

# Head
print('Head')
print(dataset.head(20))

# Descriptions
print("Describe")
print(dataset.describe())

# Class Distribution
print('Class Distribution')
print(dataset.groupby('class').size())

# Box and Whiskers plot
dataset.plot(kind ='box', subplots=True, layout=(2, 2), sharex=False, sharey=False)
pyplot.show()

# Histograms
dataset.hist()
pyplot.show()

# Scatter plot matrix
scatter_matrix(dataset)
pyplot.show()

# Split out validation dataset
array = dataset.values
X = array[:,0:4]
Y = array[:,4]
X_train, X_validation, Y_train, Y_validation = train_test_split(X, Y, test_size=0.20, random_state=1)

# Test options and evaluation metric
kfold = StratifiedKFold(n_splits=10, random_state=1)
#cv_results = cross_val_score(model, X_train, Y_train, cv=kfold, scoring='accuracy')

# Spot check Algorithms
models = []
models.append(('LR', LogisticRegression(solver='liblinear', multi_class='ovr')))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC(gamma='auto')))

# Evaluate each model in turn
results = []
names = []
for name, model in models:
    kfold = StratifiedKFold(n_splits=10, random_state=1)
    cv_results = cross_val_score(model, X_train, Y_train, cv=kfold, scoring='accuracy')
    results.append(cv_results)
    names.append(name)
    print(f'{name}: {cv_results.mean()} ({cv_results.std()})')

# Compare Algorithms
pyplot.boxplot(results, labels=names)
pyplot.title('Algorith Comparison')
pyplot.show()


# Make predictions on validation dataset
model = SVC(gamma='auto')
model.fit(X_train, Y_train)
predictions = model.predict(X_validation)

# Evaluate predictions
print(accuracy_score(Y_validation, predictions))
print(confusion_matrix(Y_validation, predictions))
print(classification_report(Y_validation, predictions))

