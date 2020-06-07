file = open(
    'C:\\Users\\Jonathan\\Documents\\GitHub\\Experiments\\teachingDima\\Updated_Medicaid.txt', 'r')

charCount = 0
notFound = True

for item in file:

    for char in item:

        charCount += 1

        if charCount == 1535 and notFound:

            print("Line: ", item, '\n')
            print("Offending Char", char, '\n')
