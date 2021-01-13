import base64
from bs4 import BeautifulSoup as bs
import os
import argparse
import io

parser = argparse.ArgumentParser(description="FB2 Image Extractor")
parser.add_argument("input", type=str, help="Input file (.fb2)")
parser.add_argument("output", type=str, help="Output folder (should not exist)")
args = parser.parse_args()

args_ok = True
if(os.path.exists(args.output) and os.path.isdir(args.output)):
    print("Output folder should not exist!")
    args_ok = False
if(args_ok and not os.path.exists(args.input)):
    print("Input file does not exist!")
    args_ok = False
if(args_ok and not os.path.isfile(args.input)):
    print("Input must be a file!")
    args_ok = False
if(args_ok and not os.path.splitext(args.input)[1]):
    print("Input file should be an .fb2!")
    args_ok = False

if(args_ok):
    os.mkdir(args.output)
    with io.open(args.input, 'r', encoding="utf-8") as file:
        data = file.read()
    content = bs(data, "lxml")
    for i, binary in enumerate(content.find_all("binary")):
        if(binary['content-type'] == "image/jpeg"):
            print("Got a jpeg image file, writing...", end=" ")
            with open(args.output+'/'+str(i+1)+'.jpg', 'wb') as file:
                image = base64.decodebytes(binary.text.encode("utf-8"))
                file.write(image)
            print("done!")
        elif(binary['content-type'] == "image/png"):
            print("Got a png image file, writing...", end=" ")
            with open(args.output+'/'+str(i+1)+'.png', 'wb') as file:
                image = base64.decodebytes(binary.text.encode("utf-8"))
                file.write(image)
            print("done!")
        else:
            print("Got unknown binary, skipping...")