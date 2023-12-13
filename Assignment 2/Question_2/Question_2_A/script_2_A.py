import csv
import matplotlib.pyplot as plt

sendingTime = []
receiveTime = []
latency__C3 = []
latency__W4 = []

with open('C3_UDP.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)

    for row in reader:
        if row[4] != "ICMP":
            sendingTime.append(float(row[1]))
        

with open('C1_C3_UDP.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)

    for row in reader:
        if row[4] != "ICMP":
            receiveTime.append(float(row[1]))


for i in range(len(sendingTime)):
    latency__C3.append(receiveTime[i] - sendingTime[i])


sendingTimee = {}
receiveTimee = {}


with open('W4_UDP.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)

    for row in reader:
        if int(row[7]) not in sendingTimee:
            sendingTimee.update({int(row[7]): float(row[1])})


with open('C1_W4_UDP.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)

    for row in reader:
        receiveTimee.update({int(row[7].split(' ')[1].split('(')[1].split(')')[0]): float(row[1])})


for keys in sendingTimee:
    if keys in receiveTimee and keys != 1:
        latency__W4.append(receiveTimee[keys] - sendingTimee[keys])
        if(receiveTimee[keys] - sendingTimee[keys] == 0.08371600000000257):
            print(keys)
            

plt.plot(range(1, len(latency__C3) + 1), latency__C3, marker = '.', color = 'RED')
plt.title('Latency for Client C3')
plt.xlabel('Packets')
plt.ylabel('Latency (second)')
plt.show()


plt.plot(range(1, len(latency__W4) + 1), latency__W4, marker = '.', color = 'RED')
plt.title('Latency for Client W4')
plt.xlabel('Packets')
plt.ylabel('Latency (second)')
plt.show()


print(f"\nMean Latency for Client C3 = {sum(latency__C3) / len(latency__C3):.7f} second\n")
print(f"Mean Latency for Client W4 = {sum(latency__W4) / len(latency__W4):.7f} second\n")