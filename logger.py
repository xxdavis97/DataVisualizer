import pandas as pd
import os.path

def logDf(df, name=""):
    cols = df.columns
    index = df.index
    values = df.values
    if not os.path.exists("dfLog.txt"):
        with open("dfLog.txt", "w+") as f:
            f.write(name + "\n")
            f.write("  ")
            for col in cols:
                f.write(str(col) + " ")
            f.write("\n")
            for i in range(len(values)):
                f.write(str(index[i])+ " ")
                for j in range(len(values[i])):
                    f.write(str(values[i][j]) + " ")
                f.write("\n")
            f.close()
    else:
        with open("dfLog.txt", "a") as f:
            f.write("\n\n\n")
            f.write(name + "\n")
            f.write(" ")
            for col in cols:
                f.write(str(col) + " ")
            f.write("\n")
            for i in range(len(values)):
                f.write(str(index[i])+ " ")
                for j in range(len(values[i])):
                    f.write(str(values[i][j]) + " ")
                f.write("\n")
            f.close()

def logError(e, funcName=""):
    if not os.path.exists("exceptionLog.txt"):
        with open("exceptionLog.txt", "w+") as f:
            f.write(funcName + ":\n")
            f.write("    " + str(e))
            f.close()
    else:
        with open("exceptionLog.txt", "a") as f:
            f.write("\n\n\n")
            f.write(funcName + ":\n")
            f.write("    " + str(e))
            f.close()

def logHTML(listOfElements, funcName=""):
    if not os.path.exists("htmlLog.txt"):
        with open("htmlLog.txt", "w+") as f:
            f.write(funcName + ":\n")
            for i in listOfElements:
                f.write(i + "\n")
            f.close()
    else:
        with open("htmlLog.txt", "a") as f:
            f.write("\n\n\n")
            f.write(funcName + ":\n")
            for i in listOfElements:
                f.write(i + "\n")
            f.close()