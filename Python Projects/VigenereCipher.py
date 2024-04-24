def encode(String, Password):
    String.lower()
    Password.lower()
    count = 0
    cyphertext = ""
    shift = 0
    for i in String:
        if count >= len(Password):
            count = 0
        if i.isspace():
            cyphertext += " "
            continue
        #Checks if the password will shift passed the end of the alphabet
        if ((ord(Password[count])-96) + (ord(i)-96)) > 26:
            cyphertext += chr(ord(i) + (ord(Password[count])-96) - 26)
        else:
            cyphertext += chr(ord(i) + (ord(Password[count])-96))
       
        count += 1
        
    print(cyphertext)
        

String = input("What do you want to encode?\n")
Password = input("What is the key?\n")
encode(String, Password)
