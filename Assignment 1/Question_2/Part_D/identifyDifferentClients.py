import pandas

data = pandas.read_csv("/home/shubham21099/WN/Assignment_1/Question_2/Input_AP.csv")

AP = set(list(data['Source'].unique()))

data = pandas.read_csv("/home/shubham21099/WN/Assignment_1/Question_2/Input.csv")

uniqueMac = []
totalCount = {}
macs = list(data['Source'])
types = list(data['PHY type'])
uniqueTypes = set(list(data['PHY type']))

for index, mac in enumerate(macs):
    mac = mac.split()[0] if isinstance(mac, str) else ""
    
    if types[index] in totalCount and mac not in AP and mac != "" and mac not in uniqueMac:
        totalCount[types[index]] = totalCount[types[index]] + 1
        uniqueMac.append(mac)

    elif types[index] not in totalCount and mac not in AP and mac != "" and mac not in uniqueMac:
        totalCount[types[index]] = 1
        uniqueMac.append(mac)

for i in totalCount:
    print(i.split()[0], ":", totalCount[i])