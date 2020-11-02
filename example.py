from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

import aurum as au

# Setup the parameters
au.parameters(test_size=0.15, random_state=4, n=12)

# Load the dataset
iris = load_iris()

# Store features matrix in X
X = iris.data

# Store target vector in y
y = iris.target

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=au.test_size, random_state=au.random_state)

# instantiate the model with the best known parameters
knn = KNeighborsClassifier(n_neighbors=int(au.n))

# train the model with X and y (not X_train and y_train)
knn_clf = knn.fit(X_train, y_train)

# get the accuracy for the classifier
a = knn.score(X_test, y_test)

print(f"Accuracy: {a}")
print(f"Au: n: {au.n}")

au.end_experiment()
