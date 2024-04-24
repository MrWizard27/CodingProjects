import re

width = 134
filename = 'vga.txt'

def trpix(pixel_value):
     value = float(pixel_value)
     value = value*255
     value = int(value)
     return int(value)


f = open(filename, "r")
fo = open("output.txt", "w")
text=f.read()
f.close()
text2=''
if ' ' in text:
    text2 = re.sub('^\\(|,|\\)\n$|\\)$','',text)
    text2 = text2.replace(') (' , '\n')
    text2 = text2.replace('\\)','\n')
    text2 = re.sub('\\)|\\(','',text2)
    # print(text2)
    
count = 0
fo.write("[\n")
for line in text2.split('\n'):
    if count == 0:
        fo.write("[")
    fo.write("(")
    fo.write(str((trpix(line.split(" ")[0]))) + ", ")
    fo.write(str((trpix(line.split(" ")[0]))) + ", ")
    fo.write(str((trpix(line.split(" ")[0]))))
    count += 1
    if count == width:
        count = 0
        fo.write(")")
        fo.write("], \n")
    else:
        fo.write("),")
fo.write("]")
fo.close()
f.close()

        