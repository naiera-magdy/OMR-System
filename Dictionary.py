

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
    "t_2_2": "\meter<\"2/2\">",
    "t_2_4": "\meter<\"2/4\">",
    "t_3_4": "\meter<\"3/4\">",
    "t_3_8": "\meter<\"3/8\">",
    "t_4_4": "\meter<\"4/4\">",
    "t_6_8": "\meter<\"6/8\">",
    "t_9_8": "\meter<\"9/8\">",
    "t_12_8": "\meter<\"12/8\">"
}

notesWithHeads = ["a_4","a_1","a_2","a_8","b_8","a_16","b_16","a_32","b_32"]
specialShapes = ["sharp","natural","flat","double_sharp","double_flat"]

# noteObject = [X-pos , The note Name , IsHollow ]
# shapeObject = [ The shape label , (X_min,X_max) ]
def TranslateStaff(shapeObject,noteObject):
    FinalOutput = "[ "
    for shape in shapeObject:

        if shape[0] in notesWithHeads:
            x_min = shape[1][0]
            x_max = shape[1][1]

            for note in noteObject:
                if note[0] >= x_min and note[0] <= x_max:
                    FinalOutput += note[1] + shapesNames[shape[0]] + " "

        elif shape[0] == "dot":
            FinalOutput += shapesNames[shape[0]]

        elif shape[0] == "chord":
            x_min = shape[1][0]
            x_max = shape[1][1]

            FinalOutput += "{"
            for note in noteObject:
                if note[0] >= x_min and note[0] <= x_max:
                    FinalOutput += note[1] + ","
            FinalOutput = FinalOutput[:-1]
            FinalOutput += "}"

        else:
            FinalOutput += shapesNames[shape[0]] + " "

    FinalOutput += "],\n"

    return FinalOutput
