import json
import os

from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import numpy as np

# Read in data
X_train = np.genfromtxt("data/train_features.csv")
y_train = np.genfromtxt("data/train_labels.csv")
X_test = np.genfromtxt("data/test_features.csv")
y_test = np.genfromtxt("data/test_labels.csv")

# Fit a model
depth = 10
clf = RandomForestClassifier(max_depth=depth, random_state=42, n_estimators=1000)
clf.fit(X_train, y_train)

acc = clf.score(X_test, y_test)
print(acc)

# Save metrics to a text file
metrics = f"Accuracy: {acc:10.4f}\n"
with open("metrics.txt", "w") as outfile:
    outfile.write(metrics)

# Generate and save confusion matrix plot
predictions = clf.predict(X_test)
cm = confusion_matrix(y_test, predictions, labels=clf.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=clf.classes_)
disp.plot(cmap=plt.cm.Blues, values_format=".4g")  # Display the confusion matrix
plt.title("Confusion Matrix")
plt.savefig("plot.png")
plt.show()  # Show the plot before saving
