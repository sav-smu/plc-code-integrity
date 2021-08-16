
import os
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
import joblib
input_path=os.path.abspath('..')+"\data\plc1_input.npy"
output_path=os.path.abspath('..')+"\data\plc1_output.npy"
model_path=os.path.abspath('..')+"\model\plc1_NN.pkl"

X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y,random_state=1)
# print X_train
# print X_test
print (X_test[:1])
clf = MLPClassifier(random_state=0, max_iter=3000).fit(X_train, y_train)
joblib.dump(clf, model_path)
# clf.predict_proba(X_test[:1])
print (clf.predict(X_test))
print (clf.score(X_test, y_test))