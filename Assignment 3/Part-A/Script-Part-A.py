import csv
import statistics
import matplotlib.pyplot as plt


RTT_OFDM = []
RTT_OFDMA = []
stationLatenciesOFDM = []
stationLatenciesOFDMA = []


for i in range(1, 11):

    latencies = []
    sendingTime = []
    receiveTime = []


    with open('/home/shubham21099/WN/Assignment_3/Part-A/OFDMA/OFDMA-STA-' + str(i) + '.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
                sendingTime.append(float(row[1]))



    with open('/home/shubham21099/WN/Assignment_3/Part-A/OFDMA/OFDMA-AP-' + str(i) + '.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
                receiveTime.append(float(row[1]))


    for i in range(min(len(sendingTime), len(receiveTime))):
        if receiveTime[i] - sendingTime[i] <= 1:
            latencies.append(abs(receiveTime[i] - sendingTime[i]))

    stationLatenciesOFDMA.append(latencies)   


for i in range(1, 11):

    latencies = []
    sendingTime = []
    receiveTime = []


    with open('/home/shubham21099/WN/Assignment_3/Part-A/OFDM/OFDM-STA-' + str(i) + '.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
                sendingTime.append(float(row[1]))



    with open('/home/shubham21099/WN/Assignment_3/Part-A/OFDM/OFDM-AP-' + str(i) + '.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
                receiveTime.append(float(row[1]))


    for i in range(min(len(sendingTime), len(receiveTime))):
        latencies.append(abs(receiveTime[i] - sendingTime[i]))

    stationLatenciesOFDM.append(latencies)   


with open('/home/shubham21099/WN/Assignment_3/Part-A/OFDMA/RTT.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            if row[7] != "":
                RTT_OFDMA.append(float(row[7].split(',')[0]))


with open('/home/shubham21099/WN/Assignment_3/Part-A/OFDM/RTT.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            if row[7] != "":
                RTT_OFDM.append(float(row[7].split(',')[0]))


print("")



print("Median RTT for OFDM  = ", statistics.median(RTT_OFDM), "second")
print("Median RTT for OFDMA = ", statistics.median(RTT_OFDMA),"second", "\n")


plt.figure(figsize = (10, 6))
plt.boxplot(stationLatenciesOFDMA, labels = [i for i in range(1, 11)], vert = True)
plt.xlabel('Stations')
plt.ylabel('Packet Latencies (seconds)')
plt.title('Packet Latency Distribution with OFDMA Transmissions for both DL and UL')
plt.xticks(range(1, 11))
plt.grid(axis = 'y', linestyle = '--', alpha = 0.7)
plt.show()

plt.figure(figsize = (10, 6))
plt.boxplot(stationLatenciesOFDM, labels = [i for i in range(1, 11)], vert = True)
plt.xlabel('Stations')
plt.ylabel('Packet Latencies (seconds)')
plt.title('Packet Latency Distribution with OFDM Transmissions for both DL and UL')
plt.xticks(range(1, 11))
plt.grid(axis = 'y', linestyle = '--', alpha = 0.7)
plt.show()
