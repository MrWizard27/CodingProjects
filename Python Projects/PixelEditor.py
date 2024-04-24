byte = 0
color = " "
resolution = 16
pixel = 0
pixels = [116,85,70,56,57]
def move():
    pixel = input("what is your starting pixel?\n")
    while(True):
        direction = input("Which Direction do you want to go (use wasd)\n")
        match direction:
            case "w":
                print("Moving Up")
                pixel = int(pixel) + 16
                print("pixel:" + str(pixel))
                Findpixel1(pixel)
            case 'a':
                print("Moving Left")
                pixel = int(pixel) - 1
                print("pixel:" + str(pixel))
                Findpixel1(pixel)
            case 's':
                print("Moving Down")
                pixel = int(pixel) - 16
                print("pixel:" + str(pixel))
                Findpixel1(pixel)
            case 'd':
                print("Moving right")
                pixel = int(pixel) + 1
                print("pixel:" + str(pixel))
                Findpixel1(pixel)

def pixelInfo(byte):

    pixel = (byte - (byte%3)) / 3
    
    match byte%3:
        case 0:
            color = "blue"
        case 1:
            color = "green"
        case 2:
            color = "red"
    
    print("Color: " +  color + "\nLocation: " + str(int(pixel)))

def Findpixel(pixel, color):

    byte = int(pixel*3)

    match color:
        case "blue":
            byte += 0
        case "green":
            byte += 1
        case "red":
            byte += 2
    print ("Byte: " + str(byte))

def makecommands():
    pixelColor = [158, 158, 158]
    flipper = True
    for i in pixels:
        x = 3
        while x > 0:
            if (flipper):
                print("bsub " + str(((i*3)+x-1)) + " " + str(pixelColor[3-x]) + " < rgbPokeBall2.bmp > rgbPokeBall.bmp")
                flipper = False
            else:
                print("bsub " + str(((i*3)+x-1)) + " " + str(pixelColor[3-x]) + " < rgbPokeBall.bmp > rgbPokeBall2.bmp")
                flipper = True
            x = x - 1
        print()

makecommands()

#while(True):
#    choice = input("1.Get Pixel Info \n2.Find Pixel\n3.Move\n")
#    match choice:
#            case '1':
#                pixelInfo()
#            case '2':
#                Findpixel()
#            case '3':
#                move()