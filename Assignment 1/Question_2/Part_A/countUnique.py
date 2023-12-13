import pandas

AP = 0
data = pandas.read_csv("/home/shubham21099/WN/Assignment_1/Question_2/Input.csv")

src = list(data['Source']     .apply(lambda x: x.split()[0] if isinstance(x, str) else "").unique())
dst = list(data['Destination'].apply(lambda x: x.split()[0] if isinstance(x, str) else "").unique())

print("Total Unique Mac Addresses are:", len(set(src + dst)) - 2)

data = pandas.read_csv("/home/shubham21099/WN/Assignment_1/Question_2/Input_AP.csv")

AP = len(set(list(data['Source'].unique()) + list(data['Destination'].unique())))

data = pandas.read_csv("/home/shubham21099/WN/Assignment_1/Question_2/Input.csv")

print("Total Unique Access Points are:", AP)
print("Total Unique Clients are:", len(set(list(data['Source'].apply(lambda x: x.split()[0] if isinstance(x, str) else "").unique()))) - 1 - AP)