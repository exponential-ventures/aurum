#!/usr/bin/env python
# -*- coding: utf-8 -*-
##
## ----------------
## |              |
## | CONFIDENTIAL |
## |              |
## ----------------
##
## Copyright Exponential Ventures LLC (C), 2019 All Rights Reserved
##
## Author: Adriano Marques <adriano@xnv.io>
##
## If you do not have a written authorization to read this code
## PERMANENTLY REMOVE IT FROM YOUR SYSTEM IMMEDIATELY.
##

import aurum as au

from examples.benchmark import Benchmark
benchmark = Benchmark('Black Friday without catalysis')

benchmark.start()

import logging

from os.path import split, join

import pandas as pd

from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

benchmark.add_label('end_imports')

logging.basicConfig(level=logging.DEBUG)

benchmark.add_label('end_log_config')

au.use_datasets("black_friday.csv")

bf_file = join(split(__file__)[0], "datasets", "black_friday.csv")
print(f"Processing file '{bf_file}' without using the Catalysis acceleration framework.")
bf = pd.read_csv(bf_file)

benchmark.add_label('file_loaded_into_memory')

au.parameters(test_size=0.15, random_state=0, n_estimators=1000)

X = bf.iloc[:, 0:6].values
y = bf.iloc[:, 9].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=au.test_size, random_state=au.random_state)

benchmark.add_label('data_splitted')

#################################
# Encoding non-numerical columns
x_train_encoder = LabelEncoder()
X_train[:, 0] = x_train_encoder.fit_transform(X_train[:, 0])
X_train[:, 1] = x_train_encoder.fit_transform(X_train[:, 1])
X_train[:, 3] = x_train_encoder.fit_transform(X_train[:, 3])
X_train[:, 4] = x_train_encoder.fit_transform(X_train[:, 4])

x_test_encoder = LabelEncoder()
X_test[:, 0] = x_test_encoder.fit_transform(X_test[:, 0])
X_test[:, 1] = x_test_encoder.fit_transform(X_test[:, 1])
X_test[:, 3] = x_test_encoder.fit_transform(X_test[:, 3])
X_test[:, 4] = x_test_encoder.fit_transform(X_test[:, 4])

benchmark.add_label('labels_encoded')

######################
# Scaling all columns
X_train_scaler = StandardScaler()
X_test_scaler = StandardScaler()

X_train = X_train_scaler.fit_transform(X_train)
X_test = X_test_scaler.fit_transform(X_test)

benchmark.add_label('values_scaled')

#################################
# Training and error measurement
regressor = RandomForestRegressor(n_estimators=au.n_estimators, random_state=au.random_state)
regressor.fit(X_train, y_train)
benchmark.add_label('training_finished')

y_pred = regressor.predict(X_test)
error = mean_absolute_error(y_test, y_pred)


au.register_metrics(error=error)
au.end_experiment()

benchmark.add_label('end_of_script')

benchmark.end()

benchmark.print()
