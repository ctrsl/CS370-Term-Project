#train classifiers made in createdataset.py
import pickle
from sklearn.ensemble import RandomForestClassifier 
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

#made in createdataset.py
data_dict = pickle.load(open('./data.pickle', 'rb'))

data = np.asarray(data_dict['data'])
labels = np.asarray(data_dict['labels'])


#call train_test_split on our x and y values from dataset
#split data and labels into to 2 different sets (training set and test set for comparison)
#test_size = size of test set
#shuffle = shuffling the data (good practice for training)
#stratify = split the data set but keep the same proportion of the different labels, (from training to test)
x_train,x_test,y_train,y_test  = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)

model = RandomForestClassifier()

#train classifier
model.fit(x_train, y_train)

y_predict = model.predict(x_test)

#see how model performs
score = accuracy_score(y_predict,y_test)

print('{}% of samples were classified correctly'.format(score*100))

f = open('model.p', 'wb')
pickle.dump({'model': model}, f)
f.close()
