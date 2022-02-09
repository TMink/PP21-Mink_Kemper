
streamIn = open('../models/utm_coords/Schnitt 17-07/15_17-07 SE07011+012+013+014+015+016+017+018+019+020.obj', 'r')
streamOut = open('../models/shift_coords/Schnitt 17-07/new_test_15_17-07.obj', 'w')

content = ''
decimal_places = 6
count = 0

for line in streamIn:
    if line.startswith("#"):
        content = "# Neues Modell"
        streamOut.write(content)
    if line.startswith('v '):
        count += 1
        groups = line.split(" ")
        new_X = round(((float(groups[1]) / 100) - int(float(groups[1]) / 100)) * 100, decimal_places)
        new_Y = round(((float(groups[2]) / 100) - int(float(groups[2]) / 100)) * 100, decimal_places)
        content = '%s %s %s %s %s %s %s' % (groups[0], str(new_X), str(new_Y), groups[3], groups[4], groups[5], groups[6])
        streamOut.write(content)
    else:
        streamOut.write(line)