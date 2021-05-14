import pandas as pd
import os.path

def logDf(df, name=""):
    cols = df.columns
    index = df.index
    values = df.values
    if not os.path.exists("deprecated/dfLog.txt"):
        with open("deprecated/dfLog.txt", "w+") as f:
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
        with open("deprecated/dfLog.txt", "a") as f:
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

def logTwitterFile(lines):
    if not os.path.exists("twitterLog.txt"):
        with open("twitterLog.txt", "w+") as f:
            f.write(str(len(lines)) + "\n")
            f.close()
    else:
        with open("twitterLog.txt", "a") as f:
            f.write(str(len(lines)) + "\n")
            f.close()

def logTweets(tweet):
    if not os.path.exists("deprecated/tweetLog.txt"):
        with open("deprecated/tweetLog.txt", "wb+") as f:
            f.write(bytes(tweet, "utf16") + bytes("\n", "utf16"))
            f.close()
    else:
        with open("deprecated/tweetLog.txt", "ab") as f:
            f.write(bytes(tweet, "utf16") + bytes("\n", "utf16"))
            f.close()

def logTwitterError(status):
    if not os.path.exists("deprecated/twitterError.txt"):
        with open("deprecated/twitterError.txt", "w+") as f:
            f.write(str(status) + "\n")
            f.close()
    else:
        with open("deprecated/twitterError.txt", "a") as f:
            f.write(str(status) + "\n")
            f.close()

def logGarbageCollect():
    if not os.path.exists("garbageRun.txt"):
        with open("garbageRun.txt", "w+") as f:
            f.write("yes" + "\n")
            f.close()
    else:
        with open("garbageRun.txt", "a") as f:
            f.write("yes" + "\n")
            f.close()