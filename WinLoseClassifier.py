from sklearn.multiclass import OneVsRestClassifier, OneVsOneClassifier
from sklearn.svm import *
from sklearn.metrics import *
from sklearn.ensemble import *
from sklearn.linear_model import *
from sklearn.externals import joblib
import numpy as np
from random import shuffle
from GameManager import GameManager
import os.path
from FeaturesConverter import FeaturesConverter

class WinLoseClassifier:

	def __init__(self, testing_mode = False):
		self._testing_mode = testing_mode
		self._dump_file_name = 'Data/Dataset/trained_model.pkl'

	def load_data(self):

		conv = FeaturesConverter()

		input_file_values = [line.strip('\n').split(',') for line in open('Data/Dataset/connect-4.data', 'r').readlines()]
		shuffle(input_file_values)

		map_val = {}
		map_val['b'] = GameManager.class_3
		map_val['x'] = GameManager.class_1
		map_val['o'] = GameManager.class_2
		map_label = {}
		map_label['win'] = 1
		map_label['loss'] = 2
		map_label['draw'] = 3


		if self._testing_mode:
			testing_samples_count = 6000
			input_training_values = input_file_values[0:len(input_file_values) - testing_samples_count]
			input_testing_values = input_file_values[len(input_file_values) - testing_samples_count:]
			self._testing_values = np.array([conv.list_to_features_vector([map_val[k] for k in v[:len(v) - 1]]) for v in input_testing_values])
			self._testing_labels = np.array([map_label[v[-1]] for v in input_testing_values])
		else:
			input_training_values = input_file_values

		self._training_values = np.array([conv.list_to_features_vector([map_val[k] for k in v[:len(v) - 1]]) for v in input_training_values])
		self._training_labels = np.array([map_label[v[-1]] for v in input_training_values])

	def train(self):
		if os.path.isfile(self._dump_file_name) and not self._testing_mode:
			self._clf = joblib.load(self._dump_file_name)
		else:
			self.load_data()
			simple_classifier = GradientBoostingClassifier(max_depth=6, n_estimators=300)
			#simple_classifier = LogisticRegression(max_iter = 100)
			#simple_classifier = SVC(max_iter = 100)
			self._clf = OneVsRestClassifier(simple_classifier, n_jobs=3)
			self._clf.fit(self._training_values, self._training_labels)
			joblib.dump(self._clf, self._dump_file_name, compress=9)

	def test(self):
		if self._testing_mode:
			return self._clf.score(self._testing_values, self._testing_labels)
		else:
			return 0.0

	# 1 Win
	# 2 Lose
	# 3 Draw
	def get_decision(self, sample):
		return self._clf.predict(np.array([sample]))[0]

	def get_class_probability(self, sample, n):
		return self._clf.predict_proba(np.array([sample]))[0][n - 1]
