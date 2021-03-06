import random

shapesNames = {
    "clef": "",
    "a_4": "/4",
    "a_1": "/1",
    "a_2": "/2",
    "a_8": "/8",
    "b_8": "/8",
    "a_16": "/16",
    "b_16": "/16",
    "a_32": "/32",
    "b_32": "/32",
    "sharp": "#",
    "natural": "",
    "flat": "&",
    "double_sharp": "##",
    "double_flat": "&&",
    "dot": ".",
    "barline": "",
    "chord": "",
    "t_4_4": "\meter<\"4/4\">",
    "t_4_2": "\meter<\"4/2\">"
}

notesWithHeads = ["a_4", "a_1", "a_2", "a_8", "b_8", "a_16", "b_16", "a_32", "b_32"]
notesWithHeadsNames = ['c1','d1','e1','f1','g1','a1','b1','c2','d2','e2','f2','g2','a2','b2']
specialShapes = ["#", "##", "&&", "&"]
meters = ["\meter<\"4/2\">", "\meter<\"4/4\">"]

# noteObject = [X-pos , The note Name , IsHollow ]
# shapeObject = [ The shape label , (X_min,X_max) ]
def TranslateStaff(shapeObject, noteObject):
    FinalOutput = "[ "
    for shape in shapeObject:

        # TODO : split notesWithHeads into solid and hollow to avoid taking wrong points
        # TODO : if not found a point make random position
        if shape[0] in notesWithHeads:
            x_min = shape[1][0]
            x_max = shape[1][1]

            found = False

            for note in noteObject:
                if x_min <= note[0] <= x_max:
                    found = True
                    FinalOutput += note[1] + shapesNames[shape[0]] + " "

            if not found:
                index = random.randint(0,len(notesWithHeadsNames)-1)
                FinalOutput += notesWithHeadsNames[index] + shapesNames[shape[0]] + " "

        elif shape[0] == "dot":
            FinalOutput = FinalOutput.strip() + shapesNames[shape[0]] + " "

        elif shape[0] == "chord":
            x_min = shape[1][0]
            x_max = shape[1][1]

            chordArr = []
            for note in noteObject:
                if x_min <= note[0] <= x_max:
                    chordArr.append(note[1])

            chordArr = sorted(chordArr)

            FinalOutput += "{"
            for chord in chordArr:
                FinalOutput += chord + "/4" + ","

            if len(chordArr) != 0:
                FinalOutput = FinalOutput[:-1]
            FinalOutput += "} "

        else:
            FinalOutput += shapesNames[shape[0]] + " "

    FinalOutput += "]"

    return FinalOutput


def FixSpecialShapes(outputString):
    words = outputString.strip().split(' ')

    for i, word in enumerate(words):
        if word in specialShapes:
            if i == len(words) - 1:
                break
            else:
                if "/" in words[i + 1] and words[i + 1] not in meters:
                    index = 1
                    out = words[i + 1][:index] + word + words[i + 1][index:]
                    words.remove(words[i + 1])
                    words.insert(i + 1, out)

    modifiedOutputString = ""
    for word in words:
        if word not in specialShapes and word != '':
            modifiedOutputString += word + " "
    return modifiedOutputString
