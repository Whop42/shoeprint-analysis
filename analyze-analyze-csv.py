csv_file = open("data-csv.csv")

data = [[]]

csv_data = []
for line in csv_file:
    if "print" in csv_data:
        continue
    csv_data.append(line.replace("\n", "").split(","))

def get_shvi_from_filenames(f1, f2):
    for i in csv_data:
        if i[0].strip() == f1 and i[1].strip() == f2:
            return abs(float(i[2].strip()))
    return 0

angles = [
    15,
    30,
    45,
    60,
    70
]

originals = []
for i in csv_data:
    if "-" not in i[0] and (i[0], csv_data.index(i)) not in originals:
        oi = [i[0] for i in originals]
        if i[0] not in oi:
            originals.append((i[0], csv_data.index(i)))

angled = []
for i in originals:
    oa = [i[0]]
    for angle in angles:
        oa.append(i[0].replace(".csv", "") + "-" + str(angle) + ".csv")
    angled.append(oa)

diffs = []

for i in range(0, len(originals)):
    diff = []
    for a in angled[i]:
        diff.append(get_shvi_from_filenames(originals[i][0], a))
    diffs.append((originals[i][0], diff))

averages = []
for i in range(0, len(angled[0])):
    averages.append(0)
for d in diffs: # for every diff
    for i in range(0, len(d[-1])): # for every index in every diff
        averages[i] += d[-1][i]

for average in averages:
    average /= len(diffs[0][-1])

print(f"differences: {diffs}")
print(f"average differences: {averages}")

