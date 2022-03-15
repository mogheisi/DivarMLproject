from sklearn import tree
import mysql.connector
import re
import time

cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='project')
cursor = cnx.cursor()
query = "SELECT * FROM car_datas;"
cursor.execute(query)
x = []
y = []

car_name = input("enter the car's name: (like: 131 پراید)\n>>> ")
time.sleep(1)


for line in cursor:
    found = re.search(car_name, line[0])
    if found:
        x.append(line[2:4])
        y.append(line[4])

clf = tree.DecisionTreeClassifier()
m = clf.fit(x, y)

model = input("enter the car's model: (format: 1395)\n>>> ")
kilometers = input("enter the car's worked kilometers: (format: 150.000)\n>>> ")

new_data = [[kilometers, model]]
answer = clf.predict(new_data)
print('The price of the car should be around « %s » Toman.' % answer[0])

cnx.close()
