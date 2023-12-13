import pandas

data = pandas.read_csv("/home/shubham21099/WN/Assignment_1/Question_2/Input_AP.csv")

AP = set(list(data['Source'].unique()))

data = pandas.read_csv("/home/shubham21099/WN/Assignment_1/Question_2/Input.csv")

macs = list(data['Source'])
bitr = list(data['Data rate'])

average_bit_rate = {}

for index, mac in enumerate(macs):
    mac = mac.split()[0] if isinstance(mac, str) else ""
    
    if mac in average_bit_rate and mac not in AP and mac != "":
        average_bit_rate[mac].append(int(bitr[index]))

    elif mac not in AP and mac != "":
        average_bit_rate[mac] = [int(bitr[index])]

for mac, bitRate in average_bit_rate.items():
    print("Average Bit Rate of", mac, "is:", round(sum(bitRate) / len(bitRate), 2), "Mbps")