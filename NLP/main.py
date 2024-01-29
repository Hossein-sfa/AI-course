from hazm import word_tokenize, Normalizer, Stemmer, Lemmatizer, POSTagger
from sklearn.decomposition import PCA
import numpy as np
import pickle
import csv

train = []
test = []
words = set()


# simple KNN classifier with Euclidean distance
class KNN:
    def __init__(self, k, trained, label):
        self.k = k
        self.trained = trained
        self.label = label

    @staticmethod
    def euclidean_distance(x1, x2):
        return np.sqrt(np.sum((x1 - x2) ** 2))

    def predict(self, test_reduced):
        predication = []
        for x in test_reduced:
            distances = [self.euclidean_distance(x, x_train) for x_train in self.trained]
            k_indices = np.argsort(distances)[:self.k]
            k_nearest_labels = [self.label[z] for z in k_indices]
            most_common = np.argmax(np.bincount(k_nearest_labels))
            predication.append(most_common)
        return np.array(predication)


# remove stop words
def is_useful(tag):
    return tag not in {'PUNCT', 'NUM', 'ADP', 'ADV', 'DET', 'INTJ', 'ADP,EZ', 'DET,EZ', 'SCONJ',
                       'VERB', 'PRON', 'CCONJ', 'NUM,EZ', 'PRON,EZ', 'ADV,EZ', 'CCONJ,EZ'}


# calculate f score
def f_score(label, prediction):
    true_positive = 0
    false_positive = 0
    false_negative = 0
    for la, p in zip(label, prediction):
        if la == p == 1:
            true_positive += 1
        elif la != p and la == 1:
            false_positive += 1
        elif la != p and la == 0:
            false_negative += 1
    precision = true_positive / (true_positive + false_positive)
    recall = true_positive / (true_positive + false_negative)
    return (2 * precision * recall) / (precision + recall)


# reading data from csv file that has 20000 rows
with open('nlp_train.csv', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    normalizer = Normalizer()
    stemmer = Stemmer()
    lemmatizer = Lemmatizer()
    tagger = POSTagger(model='pos_tagger.model')
    i = 0
    for row in reader:
        if i == 0:
            i += 1
            continue
        tokens = word_tokenize(normalizer.normalize(row[1]))
        stemmed = [stemmer.stem(i) for i in tokens]
        lemmatized = [lemmatizer.lemmatize(i) for i in stemmed]
        cleaned = [i[0] for i in tagger.tag(lemmatized) if is_useful(i[1])]
        if i <= 8000 or 10000 < i <= 18000:
            train.append(cleaned)
            words |= set(cleaned)
        elif 8000 < i <= 10000 or 18000 < i <= 20000:
            test.append(cleaned)
        i += 1
# calculating document term matrix
print('DTM')
labels = [1] * 8000 + [0] * 8000  # 1 for sports and 0 for politics
test_labels = [1] * 2000 + [0] * 2000
words = list(words)
DTM = [[train[i].count(words[j]) for j in range(len(words))] for i in range(len(train))]
DTM_test = [[test[i].count(words[j]) for j in range(len(words))] for i in range(len(test))]
# reducing with PCA with n_components = 800
print('PCA')
# for training and testing data:
pca = PCA(n_components=800, copy=False)
fitted_pca = pca.fit(DTM)
transformed_pca = pca.transform(DTM)
pca_test = pca.transform(DTM_test)
# saving the transformed pcas for later use
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(labels, open('labels.pkl', 'wb'))
pickle.dump(fitted_pca, open('fitted_pca.pkl', 'wb'))
pickle.dump(transformed_pca, open('transformed_pca.pkl', 'wb'))
# applying KNN classifier with k = 15
print('KNN')
knn = KNN(15, pca_test, labels)
predicate = knn.predict(test)
accuracy = f_score(test_labels, predicate)
print(accuracy)
