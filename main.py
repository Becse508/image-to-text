from PIL import Image, UnidentifiedImageError
import numpy as np
from time import time
from os import listdir
try:
    from termcolor import cprint
    TERMCOLOR = True
except:
    TERMCOLOR = False


LOGO = """
████  ███        ████  ██████████████  ████████████ ██████████████ ██████  ██████ ██████████████
████  ██████  ███████  ████                    ████      ████        ██████████        ████     
████  ███████████████  ████      ████  ████████████      ████         ███████          ████     
████  ████  ███  ████  ████      ████  ████              ████         ████████         ████     
████  ████       ████  ████      ████  ████              ████       ████████████       ████     
████  ████       ████  ██████████████  ████████████      ████     ██████    █████      ████     
"""
print(LOGO)

INPUT_FOLDER = "images"
OUTPUT_FOLDER = "output"
STYLE = 'accurate'
FILTER_FUNC = lambda a,b: a % b == 0 # a=row index, b=FILTERED_ROWS
FILTERED_ROWS = 2 # row will not be kept if FILTER_FUNC is False (needed because in text editors, a line's height is more than a character's width, so in the output, a pixel's size ratio is FILTERED_ROWS:1)
#               ^  Set to 0 to disable

BLANK_CHARS = (' ', '⠀', ' ')
BLANK_CHAR = 0 # !!CAN CAUSE THE GENERATED TEXT TO FALL APART IF NOT SET TO 0!!
STYLES = {
    'math': {
        '0-51' : '%',
        '52-102' : '/',
        '103-153' : '+',
        '154-204' : '=',
        '205-255' : '-'
        },
    'reverse_math': {
        '0-51' : '-',
        '52-102' : '=',
        '103-153' : '+',
        '154-204' : '/',
        '205-255' : '%'
        },
    'accurate': {
        '0-51' : '█',
        '52-102' : '▓',
        '103-153' : '▒',
        '154-204' : '░',
        '205-255' : BLANK_CHARS[BLANK_CHAR]
        },
    'reverse_accurate': {
        '0-51' : BLANK_CHARS[BLANK_CHAR],
        '52-102' : '░',
        '103-153' : '▒',
        '154-204' : '▓',
        '205-255' : '█'
        },
}



class BadImageModeError(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)
        self.message = message


class Log:
    def __init__(self, save = False):
        self.start = int(time()*500)

        self.save = save


    def get_time(self):
        now = int(time()*500)
        return now - self.start


    def raw(self,title,msg,color):
        now = self.get_time()
        text = f"{now} [{title}] " + str(msg)

        if TERMCOLOR: cprint(text, color)
        else: print(text)
        if self.save == True: self.write(text)
    
    def info(self,msg):
        now = self.get_time()
        text = f"{now} [INFO] " + str(msg)

        print(text)
        if self.save == True: self.write(text)

    def warn(self,msg):
        now = self.get_time()
        text = f"{now} [WARNING] " + str(msg)

        if TERMCOLOR: cprint(text, 'yellow')
        else: print(text)
        if self.save == True: self.write(text)

    def error(self,msg):
        now = self.get_time()
        text = f"{now} [ERROR] " + str(msg)

        if TERMCOLOR: cprint(text, 'red')
        else: print(text)
        if self.save == True: self.write(text)

    def nl(self):
        print()
        if self.save == True: self.write('')


    def write(self,text):
        with open(f"logs/log_{self.start}.log","a",encoding='utf-8') as logFile:
            logFile.write(text + '\n')

    def writelines(self,text):
        with open(f"logs/log_{self.start}.log","a",encoding='utf-8') as logFile:
            logFile.writelines(text)



def get_image(image_path):
    image = Image.open(image_path, "r")
    width, height = image.size
    if image.mode != "RGB":
        try:
            image = image.convert('RGB')
        except:
            raise BadImageModeError(f"Failed to convert unknown image mode '{img}' to RGB.")
        

    channels = 3
    pixel_values = list(image.getdata())
    pixel_values = np.array(pixel_values).reshape((height, width, channels))
    return list(pixel_values)



def get_size(image_path):
    image = Image.open(image_path, "r")
    return image.size



def filter_rows(img_data):
    new_data = []
    for i,v in enumerate(img_data):
        if FILTER_FUNC(i, FILTERED_ROWS):
            new_data.append(v)
    
    return new_data
        


def generate(image_data):
    out = ''
    for x in image_data:
        for y in x:
            

            for key,value in STYLES[STYLE].items():
                range = [int(x) for x in key.split('-')]

                avg = sum(y)/3
                if range[0] <= avg <= range[1]:
                    out += value

        
        out += '\n'

    return out



if __name__ == '__main__':
    _log = Log()

    _log.info(f"Input folder: {INPUT_FOLDER}")
    _log.info(f"Output folder: {OUTPUT_FOLDER}")
    _log.warn("The program might not be able to convert all of your images into text files. Some of the generated text files might be obfuscated. If you encounter this, please let me know on Github.\n")
    


    for file in listdir(INPUT_FOLDER):
        _log.info(f"Reading {file}")
        try:
            img = get_image(INPUT_FOLDER + '/' + file)
        except BadImageModeError as e:
            _log.error(e.message)
            continue
        except FileNotFoundError:
            _log.error(f"{file} not found file.")
            continue
        except UnidentifiedImageError:
            _log.error(f"Failed to identify {file}. Maybe not an image?")
            continue



        if type(FILTERED_ROWS) != int or 0 != FILTERED_ROWS < 2:
            _log.error(f'Bad row filter value: {FILTERED_ROWS}. Please change the "FILTERED ROWS" constant back to 2 (or higher, 0 to disable).')
            input("Press Enter to exit... ")
            exit(-1)
        
        if FILTERED_ROWS != 0:
            _log.info('Filtering rows...')
            img = filter_rows(img)

        
        _log.info(f"Converting to text...")
        name = file.split('.')[0]
        with open(f'{OUTPUT_FOLDER}/{name}.txt','w',encoding='utf-8') as f:
            f.write(generate(img))
        
        _log.info(f"{file} done!\n")


    _log.info("Program Finished!")
    input("Press Enter to exit... ")   