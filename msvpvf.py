import struct, sys, argparse, os
from pathlib import Path

def main(argv):
    global inputfile
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help="input file", metavar='<input>', required=True)
    parser.add_argument('-o', '--output', help="output file, defaults to '(MS,VEG)_(version)_(original name).(vf,veg)'", metavar='<output>')
    args = parser.parse_args()
    if args.input:
        inputfile = args.input

    if os.path.exists(inputfile):
        fp = open(inputfile, "rb")
        tes = fp.read()
        fp.close()
        test = bytearray(tes)
    else:
        print("File doesn't exist!")
        exit()
    print("Project file version: " + str(test[0x46]) + ".0")
    answer = ""
    while answer not in ["8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18"]:
        print("Which version of VEGAS would you like it to be spoofed to? [8-18]: ", end = "")
        answer = input().lower()
    answer2 = ""
    while answer2 not in ["veg", "vf"]:
        print("Would you like it to be VEGAS Pro or Movie Studio? [veg,vf]: ", end = "")
        answer2 = input().lower()
    if answer2 == "vf":
        filename_prefix = "MS"
        test[0x18] = int("F6", 16)
        test[0x19] = int("1B", 16)
        test[0x1A] = int("3C", 16)
        test[0x1B] = int("53", 16)
        test[0x1C] = int("35", 16)
        test[0x1D] = int("D6", 16)
        test[0x1E] = int("F3", 16)
        test[0x1F] = int("43", 16)
        test[0x20] = int("8A", 16)
        test[0x21] = int("90", 16)
        test[0x22] = int("64", 16)
        test[0x23] = int("B8", 16)
        test[0x24] = int("87", 16)
        test[0x25] = int("23", 16)
        test[0x26] = int("1F", 16)
        test[0x27] = int("7F", 16)
    elif answer2 == "veg":
        filename_prefix = "PRO"
        test[0x18] = int("EF", 16)
        test[0x19] = int("29", 16)
        test[0x1A] = int("C4", 16)
        test[0x1B] = int("46", 16)
        test[0x1C] = int("4A", 16)
        test[0x1D] = int("90", 16)
        test[0x1E] = int("D2", 16)
        test[0x1F] = int("11", 16)
        test[0x20] = int("87", 16)
        test[0x21] = int("22", 16)
        test[0x22] = int("00", 16)
        test[0x23] = int("C0", 16)
        test[0x24] = int("4F", 16)
        test[0x25] = int("8E", 16)
        test[0x26] = int("DB", 16)
        test[0x27] = int("8A", 16)
    test[0x46] = int(answer)
    filename_wo_ext = Path(inputfile).with_suffix('')
    if args.output:
        outputfile = args.output
    else:
        outputfile = filename_prefix + "_V" + answer + "_" + str(filename_wo_ext) + "." + answer2
    if os.path.exists(outputfile):
        answer3 = ""
        while answer3 not in ["y", "n", "yes", "no"]:
            print(f"{outputfile} already exists. Overwrite it? [y/n]: ", end = "")
            answer3 = input().lower()
        if answer3 in ["y", "yes"]:
            os.remove(outputfile)
        else:
            sys.exit()
    target = open(outputfile, 'wb')
    target.write(test)
    target.close()

if __name__ == "__main__":
    main(sys.argv[1:])
