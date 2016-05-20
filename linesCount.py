import os
import datetime

# Config
FrequentlyUsedProjectPath = {
    "Together": "/Users/Geeprox/Workspace/Together/Code/Together",
}

TargetPath = FrequentlyUsedProjectPath["Together"]

TargetFileType = {
    ".swift",
    ".h",
    ".c",
    ".cpp",
    ".py"
}

EliminateFolders = {
    "Pods"
}

ConfigFilePath = "./.linesCount.dat"
# End config

# Data structure
FilesLinesCount = []
LastFilesLinesCount = []


def get_all_files(target_path):
    files_list = []
    for root, dirs, files in os.walk(target_path):
        if "." not in root:
            skip_this_root = False
            for eliminateFolder in EliminateFolders:
                if eliminateFolder in root:
                    skip_this_root = True
                    break
            if skip_this_root:
                continue

            for file_name in files:
                if file_name[0] != ".":
                    suffix = file_name.split(".")
                    if len(suffix) > 1:
                        file_type = "." + str(suffix[1])
                        if file_type in TargetFileType:
                            files_list.append(os.path.join(root, file_name))

    return files_list


def read_data_file():
    if os.path.isfile(ConfigFilePath):
        data_file = open(ConfigFilePath)

        data = data_file.readline().strip("\n")
        last_target_path = data

        if last_target_path == TargetPath:
            data = data_file.readline().strip("\n")

            while data:
                data_info_list = data.split(":")
                LastFilesLinesCount.append((data_info_list[0], int(data_info_list[1])))
                data = data_file.readline().strip("\n")

            data_file.close()
            return True
        else:
            data_file.close()
            return False
    else:
        return False


def save_data_file():
    data_file = open(ConfigFilePath, "w+")

    data = TargetPath + "\n"
    for file, lines in FilesLinesCount:
        data += file + ":" + str(lines) + "\n"

    data_file.write(data)
    data_file.close()


def int_difference(old, new):
    if old <= new:
        return "+" + str(new - old)
    else:
        return "-" + str(old - new)


# Run from here
Files = get_all_files(TargetPath)
FilePathLengthMax = 0
FormatSpaceLength = 20

ExistDataFile = read_data_file()

for File in Files:
    count = 0
    current_file = open(File, "r")
    try:
        line = current_file.readline()
        while line:
            count += 1
            line = current_file.readline()

    except UnicodeDecodeError:
        continue
    if len(str(File).replace(TargetPath, "...")) > FilePathLengthMax:
        FilePathLengthMax = len(str(File).replace(TargetPath, "..."))

    FilesLinesCount.append((File.replace(TargetPath, "..."), count))

SumLines = 0
LastSumLines = 0

if ExistDataFile:
    for FileName, Lines in LastFilesLinesCount:
        LastSumLines += Lines

if FilePathLengthMax < len(TargetPath):
    FilePathLengthMax = len(TargetPath)

os.system("clear")
print("LinesCount  --Geeprox".center(FilePathLengthMax + FormatSpaceLength) + "\n")
print(datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S"))
print("Target path: " + TargetPath)
print("=" * (FilePathLengthMax + FormatSpaceLength))
print("          Source file".ljust(FilePathLengthMax + FormatSpaceLength - 5) + "Lines")
print("-" * (FilePathLengthMax + FormatSpaceLength))

for FileName, Lines in FilesLinesCount:
    SumLines += Lines
    print(str(FilesLinesCount.index((FileName, Lines))).center(4), end="")

    if ExistDataFile:
        FoundLastFile = False
        FoundLastFileLines = 0
        for FileNameTemp, LinesTemp in LastFilesLinesCount:
            if FileNameTemp == FileName:
                FoundLastFile = True
                FoundLastFileLines = LinesTemp
                LastFilesLinesCount.remove((FileNameTemp, LinesTemp))
                break
        if FoundLastFile:
            print("[*] " + FileName.ljust(FilePathLengthMax + FormatSpaceLength - 12, "-") + str(Lines), end="")
            print(" (" + int_difference(FoundLastFileLines, Lines) + ")")
        else:
            print("[+] " + FileName.ljust(FilePathLengthMax + FormatSpaceLength - 12, "-") + str(Lines), end="")
            print(" (" + int_difference(FoundLastFileLines, Lines) + ")")
    else:
        print("[+] " + FileName.ljust(FilePathLengthMax + FormatSpaceLength - 12, "-") + str(Lines), end="")
        print(" (+" + str(Lines) + ")")

if ExistDataFile:
    if len(LastFilesLinesCount) != 0:
        print("-" * (FilePathLengthMax + FormatSpaceLength))
        for FileNameTemp, LinesTemp in LastFilesLinesCount:
            print("[-] " + FileNameTemp + " (" + str(LinesTemp) + ")")

print("=" * (FilePathLengthMax + FormatSpaceLength))

OutputTotal = "Total: " + str(SumLines)
if ExistDataFile:
    OutputTotal += "(" + int_difference(LastSumLines, SumLines) + ")"

print(OutputTotal.rjust(FilePathLengthMax + FormatSpaceLength + 4), end="\n\n")

save_data_file()
