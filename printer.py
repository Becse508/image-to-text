from main import Log
from os import listdir
_log = Log()


INPUT_FOLDER = "output"

_log.info(f"Input folder: {INPUT_FOLDER}")
_log.info("If the image is wide, it might not have enough place and won't look good.")
input("Press Enter to contitue... ")

for filename in listdir(INPUT_FOLDER):
    _log.info(f"Printing {filename}")
    with open(INPUT_FOLDER + '/' + filename, encoding='utf-8') as f:
        line = f.readline()
        while line:
            print(line, end="")
            line = f.readline()
    
    input("Press enter to print the next file.")