import sys, argparse, os

def prog_type(byte):
    if byte == int("F6", 16):
        return "Movie Studio"
    elif byte == int("EF", 16):
        return "VEGAS Pro"
    else:
        return "Unknown"

def type_hex(type):
    if type == "vf" or type == 1:
        return "MS", [int("F6", 16), int("1B", 16), int("3C", 16), int("53", 16), int("35", 16), int("D6", 16), int("F3", 16), int("43", 16), int("8A", 16), int("90", 16), int("64", 16), int("B8", 16), int("87", 16), int("23", 16), int("1F", 16), int("7F", 16)]
    elif type == "veg" or type == 0:
        return "PRO", [int("EF", 16), int("29", 16), int("C4", 16), int("46", 16), int("4A", 16), int("90", 16), int("D2", 16), int("11", 16), int("87", 16), int("22", 16), int("00", 16), int("C0", 16), int("4F", 16), int("8E", 16), int("DB", 16), int("8A", 16)]
    else:
        return

def main(args):
    if args.input:
        inputfile = args.input
    if os.path.exists(inputfile):
        with open(inputfile, "rb") as fp:
            test = bytearray(fp.read())
    else:
        print("Input file doesn't exist!")
        exit()
    project = prog_type(test[0x18])
    print("Project file version: " + project + " " + str(test[0x46]) + ".0")
    if not args.version:
        answer = ""
    else:
        answer = args.version
    while answer not in ["8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18"]:
        answer = str(input("Which version of VEGAS would you like it to be spoofed to? [8-18]: "))
    if not args.type:
        answer2 = ""
        while answer2 not in ["veg", "vf"]:
            answer2 = input("Would you like it to be VEGAS Pro or Movie Studio? [veg,vf]: ").lower()
    else:
        answer2 = args.type
    filename_prefix, typehex = type_hex(answer2)
    test[0x18:0x27] = typehex
    test[0x46] = int(answer)
    filename_wo_ext = os.path.basename(os.path.splitext(inputfile)[0])
    if args.output:
        outputfile = args.output
    else:
        outputfile = os.path.abspath(os.path.dirname(inputfile)) + "/" + filename_prefix + "_V" + answer + "_" + str(filename_wo_ext) + "." + answer2
    with open(outputfile, 'wb') as target:
    	target.write(test)
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help="input file", metavar='<input>', required=True)
    parser.add_argument('-o', '--output', help="output file, defaults to '(MS,VEG)_(version)_(original name).(vf,veg)'", metavar='<output>')
    parser.add_argument('-v', '--version', help="output file version", metavar='<version>')
    parser.add_argument('-t', '--type', help="output file type, vf/veg", metavar='<type>')
    args = parser.parse_args()
    main(args)
