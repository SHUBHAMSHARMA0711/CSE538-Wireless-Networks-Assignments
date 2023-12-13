import pandas

data = pandas.read_csv("/home/shubham21099/WN/Assignment_1/Question_2/Input_AP.csv")

AP = set(list(data['Source'].unique()))

data = pandas.read_csv("/home/shubham21099/WN/Assignment_1/Question_2/Input.csv")

macs = list(data['Source'])
ssth = list(data['Signal strength (dBm)'])

average_signal_strength = {}

for index, mac in enumerate(macs):
    mac = mac.split()[0] if isinstance(mac, str) else ""
    
    if mac in average_signal_strength and mac not in AP and mac != "":
        average_signal_strength[mac].append(int(ssth[index].split()[0]))

    elif mac not in AP and mac != "":
        average_signal_strength[mac] = [int(ssth[index].split()[0])]

for mac, strengths in average_signal_strength.items():
    print("Average Signal Strength of", mac, "is:", round(sum(strengths) / len(strengths), 2), "dBm")