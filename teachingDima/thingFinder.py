file = open(
    'C:\\Users\\jakda\\Documents\\Work\\Experiments\\teachingDima\\Updated_Medicaid.txt', 'r')

charCount = 0
notFound = True
lineCharCount = 0

for item in file:

    lineCharCount += charCount - lineCharCount

    for char in item:

        charCount += 1

        if charCount == 1535 and notFound:

            print("Beginning of Line Char Count: ", lineCharCount)
            print("Char Count: ", charCount)
            print("Line: ", item)
            print(' ' * (charCount - lineCharCount - 1 + 6), "^")
            print("Offending Char", char)
