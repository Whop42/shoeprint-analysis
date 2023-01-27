import os
import itertools

base_path = os.path.join("data", "csvs")

csvs = os.listdir(base_path)
csvs.remove("empty.csv")

shvis = []
csv_file = open("data-csv.csv", "w")
def get_svhis(csv1, csv2):
    for shvi in shvis:
        if shvi[0] == csv2 and shvi[1] == csv1:
            return

    files = [open(os.path.join(base_path, csv1)), open(os.path.join(base_path, csv2))]
    
    data = [[],[]]

    for file in files:
        for line in file:
            if "x" in line:
                continue
            x, y, z = line.replace("\n", "").strip().split(",")
            x = float(x)
            y = float(y)
            z = float(z)
            data[files.index(file)].append([x, y, z])
        file.close()

    for file in data:
        file = sorted(file, key=lambda x: (x[0],x[1]))

    diffs = []

    count = 0
    for i in range(0, len(data[0])):
        if not data[0][i][1] == -8.326672684688674e-17 and not data[1][i][1] == -8.326672684688674e-17:
            a = [data[0][i][1], data[1][i][1]]
            diff = abs(max(a) - min(a))

            diffs.append(abs(diff))
        else:
            diffs.append(-1)

    total = 0
    for diff in diffs:
        total += abs(diff)
    
    shvi = [csv1, csv2, abs(total / len(diffs))]
    csv_file.write(f"{shvi[0]}, {shvi[1]}, {shvi[2]}\n")
    shvis.append(shvi)

def comb(csvs):
    if len(csvs) == 2:
        yield [csvs]
    for csv1 in csvs[1:]:
        rest = [csv for csv in csvs if csv != csv1]
        for csv2 in rest:
            yield [csv1, csv2]

for csv1, csv2 in comb(csvs):
    get_svhis(csv1, csv2)

csv_file.close()