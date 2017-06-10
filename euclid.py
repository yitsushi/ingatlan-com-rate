#!/usr/bin/env python3

import numpy as np
from sklearn.ensemble import ExtraTreesClassifier, AdaBoostClassifier
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt

from database import Database

deps = [
        'area', 'price',
        'has_elevator', 'utility_cost',
        'has_appliances', 'is_furnished',
        'location_grid_id',
        'rooms_sum'
]


db = Database()

def generate_X_y(properties):
    X = []
    y = []

    for prop in properties:
        grid_id = calculate_grid_index(prop[10], prop[11])
        data = prop[1:7] + (grid_id, prop[7] + (prop[8] * 0.5))

        X.append(data)
        y.append(prop[13])

    return (np.array(X), np.array(y))

def calculate_grid_index(latitude, longitude):
    latitude = int((float(latitude) + 90) * 100)
    longitude = int((float(longitude) + 180) * 100)
    return (longitude * 180 * 100) + latitude

known_props = db.fetch_all("properties", decided=(-1,1), done=(0,0))
new_props = db.fetch_all("properties", decided=(0,0), done=(0,0))
X, y = generate_X_y(known_props)

m = len(deps)
n = len(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

print("%d train data, %d for validation" % (len(X_train), len(X_test)))

model = ExtraTreesClassifier()
#model = AdaBoostClassifier()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
acc = sum(y_pred == y_test) / float(y_test.shape[0])
print("Prediction accuracy on unseen data: %.3f%%" % (acc*100))

maybe = 0
for prop in new_props:
    lX, ly = generate_X_y([prop])
    v = model.predict(lX)
    db.update_prediction("properties", "id", prop[0], int(v[0]))
    if int(v[0]) == 1:
        maybe += 1

print("All unknown are updated. Scanned: {} | Maybe works: {}".format(len(new_props), maybe))

fig, ax = plt.subplots()
ind = np.arange(m)
width = 0.5
rects = ax.bar(ind, model.feature_importances_, width, color='r')
ax.set_ylabel('Importance')
ax.set_title('Relative importance of features')
ax.set_xticks(ind + width/2)
ax.set_xticklabels(deps, rotation=90)
plt.show()
