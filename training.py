
import os
from sklearn import svm
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
import data_process
from data_process.data_process import actuators_data_process
from data_process.data_process import stages_data_process
import joblib
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score, GridSearchCV

def actuator_select(input_path,output_path,plc_index,actuator_index):
    X,y=actuators_data_process(input_path,output_path,plc_index,actuator_index)
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=0)
    return X_train, X_test, y_train, y_test

def stage_select(input_path,output_path,plc_index):
    X,y=stages_data_process(input_path,output_path,plc_index)
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=0)
    return X_train, X_test, y_train, y_test

def multiclass_nn_model_training(X_train,y_train,model_path,max_iter):
    clf = MLPClassifier(random_state=0, max_iter=max_iter).fit(X_train, y_train)
    joblib.dump(clf, model_path)

def multiclass_nn_model_testing(X_test,y_test,model_path):
    clf = joblib.load(model_path)
    print(clf.score(X_test, y_test))

def multiclass_svm_model_training(X_train,y_train,model_path):
    clf = svm.SVC(C=1000,kernel='rbf',gamma='0.001').fit(X_train, y_train)
    joblib.dump(clf, model_path)

def multiclass_svm_model_testing(X_test,y_test,model_path):
    clf = joblib.load(model_path)
    print(clf.score(X_test, y_test))


def binary_svm_model_training(X_train,y_train,model_path):
    clf = svm.SVC(kernel='rbf').fit(X_train,y_train)
    joblib.dump(clf, model_path)

def binary_svm_model_testing(X_test,y_test,model_path):
    clf=joblib.load(model_path)
    print (clf.predict(X_test))
    print (clf.score(X_test, y_test))

def multiclass_nn_training(length,input_path,output_path):
    for i in range(0,4):
        plc_index = i
        X_train, X_test, y_train, y_test = stage_select(input_path, output_path, plc_index)
        model_path="model/nn_stage"+str(i+1)+"length"+str(length)+".pkl"
        multiclass_nn_model_training(X_train,y_train,model_path,1000)
        multiclass_nn_model_testing(X_test, y_test, model_path)




def muticlass_svm_training(length,input_path,output_path):
    for i in range(0,4):
        plc_index = i
        X_train, X_test, y_train, y_test = stage_select(input_path, output_path, plc_index)
        model_path="model/svm_stage"+str(i+1)+"length"+str(length)+".pkl"
        multiclass_svm_model_training(X_train,y_train,model_path)
        multiclass_svm_model_testing(X_test, y_test, model_path)

if __name__ == '__main__':
    length=10000
    input_path = "data/plc_input_length"+str(length)+".npy"
    output_path ="data/plc_output_length"+str(length)+".npy"



    # params_grid = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
    #                 'C': [1, 10, 100, 1000]},
    #                {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]
    # X_train, X_test, y_train, y_test = stage_select(input_path, output_path, 0)
    # svm_model = GridSearchCV(SVC(), params_grid, cv=5)
    # svm_model.fit(X_train, y_train)
    # print('Best score for training data:', svm_model.best_score_, "\n")
    #
    # # View the best parameters for the model found using grid search
    # print('Best C:', svm_model.best_estimator_.C, "\n")
    # print('Best Kernel:', svm_model.best_estimator_.kernel, "\n")
    # print('Best Gamma:', svm_model.best_estimator_.gamma, "\n")

    # plc_index=1
    # actuator_index=2
    # X_train, X_test, y_train, y_test=actuator_select(input_path,output_path,plc_index,actuator_index)
    # print (y_train)
    # svm_model_training(X_train,y_train,model_path)
    # svm_model_testing(X_test, y_test, model_path)
# X,y=actuators_data_process(input_path,output_path,0,0)
#
# # print (X)
# # print (y)
# X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y,random_state=0)




# clf = MLPClassifier(random_state=1, max_iter=3000).fit(X_train, y_train)
# joblib.dump(clf, model_path)
# # clf.predict_proba(X_test[:1])
# print (clf.predict(X_test))
# print (clf.score(X_test, y_test))