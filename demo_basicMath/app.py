#Required modules
import csv

#filePath：path to file
filePath = "demo.csv"

#file: Files to be operated
file = csv.reader(open(filePath,'r'))

#contene: list that store the data, each row is one element
content = []

#Store data in list 'content'
for line in file:
    content.append(line)

mean = []
sum = 0
num = 0
average = 0
#get the mean
for row in range(0, len(content)):
    sum = 0
    for column in range(0, len(content[row])):
        sum += float(content[row][column])

    average = sum/len(content[row])
    mean.append(average)
    print(content[row], " average:" , mean[row])









