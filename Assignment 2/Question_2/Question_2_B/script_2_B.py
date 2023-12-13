import csv
import matplotlib.pyplot as plt

windows_C3 = []
windows_W4 = []
throughputs_C3 = []
throughputs_W4 = []

totalBytes = 0
currentWindow = 0.011


with open('C3_TCP.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)
    
    for row in reader:
        if float(row[1]) < currentWindow:
            totalBytes = totalBytes + int(row[5])

        else:
            throughputs_C3.append(totalBytes * 8 / 0.001)
            totalBytes = 0
            totalBytes = totalBytes + int(row[5])
            windows_C3.append(currentWindow)
            currentWindow = currentWindow + 0.001


totalBytes = 0
currentWindow = 1.920


with open('W4_TCP.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)
    
    for row in reader:
        if float(row[1]) < currentWindow:
            totalBytes = totalBytes + int(row[5])

        else:
            throughputs_W4.append(totalBytes * 8 / 0.001)
            totalBytes = 0
            totalBytes = totalBytes + int(row[5])
            windows_W4.append(currentWindow)
            currentWindow = currentWindow + 0.001


plt.plot(windows_C3, throughputs_C3, marker = '.', color = 'RED')
plt.title('Throughput for Client C3')
plt.xlabel('Windows (second)')
plt.ylabel('Throughput (bits/second)')
plt.yticks(throughputs_C3)
plt.show()


plt.plot(windows_W4, throughputs_W4, marker = '.', color = 'RED')
plt.title('Throughput for Client W4')
plt.xlabel('Windows (second)')
plt.ylabel('Throughput (bits/second)')
plt.yticks(throughputs_W4)
plt.show()


print(f"\nMean Throughput for Client C3 = {sum(throughputs_C3) / len(throughputs_C3):.3f} bits/second\n")
print(f"Mean Throughput for Client W4 = {sum(throughputs_W4) / len(throughputs_W4):.3f} bits/second\n")