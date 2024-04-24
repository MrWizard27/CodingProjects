import pyautogui
import time
import keyboard
import requests
import json
import sqlite3

# Function to get the id of a question
def get_id(question):
    conn = sqlite3.connect('trivia.db')
    c = conn.cursor()
    tdb_query = "https://opentdb.com/browse.php?query="
    query = requests.get(tdb_query + question + "&type=Question#")
    try:
        id = query.text.split('ID')[1].split('<td>')[1][:-5]
        return int(id)
    except Exception as e:
        if (query.text.split('class="alert alert-danger">')[1][:19] == "No questions found."):
            return c.execute("SELECT MAX(id) FROM trivia").fetchone()[0] + 1
        print("Error in ")
    conn.close()

# Function to type a string
def type_string(string):
    pyautogui.typewrite(string)
    pyautogui.press('enter')

# Function to click the mouse
def click_mouse():
    pyautogui.click()

# Function to get the most recent message from the chat
def get_message(emb):
    # put channel id here
    channelid = 00000000000000
    headers = {
        'authorization': 'put your authorization token here'
    }
    r = requests.get(f'https://discord.com/api/v9/channels/{channelid}/messages?limit=8', headers=headers)
    jsonn = json.loads(r.text)

    if emb == False:
        return jsonn[0]

    for value in jsonn:
        try:
            if 'embeds' in value and len(value['embeds']) > 0:
                return (value)
        except Exception as e:
            print("No message found")

def get_option(answer):
    options = get_message(True)['embeds'][0]['description'].split("\n")
    n = 0
    while(True):
        if options[n][4:] == answer:
            return n-1
        else:
            n += 1


# Function to check whether the highlow game number is greater than or equal to 50
def highlowcheck():
    try:
        highlownumber = get_message(True)['embeds'][0]['title']
    except Exception as e:
        print("Error in highlowcheck")
        return False
    print("got message")
    print(highlownumber)
    try:
        highlownumber = highlownumber[23:]
        print(highlownumber)
        if highlownumber.isdigit() and int(highlownumber) >= 50:
            return True
        else:
            return False
    except Exception as e:
        print("Error in highlowcheck")
        return False
    
# Function to run the trivia game
def trivia():
    conn = sqlite3.connect('trivia.db')
    c = conn.cursor()
    print("trivia")
    type_string("p!trivia hard")
    time.sleep(1)
    try:
        question = get_message(True)['embeds'][0]['description'].split("\n")[0]
    except Exception as e:
        print("Error in trivia")
        return
    print(question)

    if (c.execute("SELECT * FROM trivia WHERE id = " + str(get_id(question))).fetchone() == None):
        print("Question not found")
        print("adding to database")
        type_string("1")
        try:
            if (get_message(False)['content'].split("> ")[1][:9] == "Incorrect"):
                #gets the correct answer if you answered incorrectly
                answer = get_message(False)['content'].split("**")[1]
                print("answer = " + answer)
                return
            else:
                #gets the first answer if the first answer is correct
                answer = get_message(True)['embeds'][0]['description'].split("\n")[2][4:]
                print("answer = " + answer)
                return
        except Exception as e:
            answer = get_message(True)['embeds'][0]['description'].split("\n")[2][4:]
            print("answer1 = " + answer)

        c.execute("INSERT INTO trivia (id, question, answer) VALUES (?, ?, ?)", (str(get_id(question)), question, answer))
        conn.commit()
        print("added | " + str(get_id(question)) + " | " + question + " | " + answer + " |" + "to database")
    else:
        answer = c.execute("SELECT answer FROM trivia WHERE id = " + str(get_id(question))).fetchone()[0]
    print(answer)

    option = get_option(answer)
    print(option)
    print(option)
    type_string(str(option))
    conn.close()

# Function to fish   
def buy_fishing_rod():
    # put channel id here
    channelid = 00000000000000
    print("Buying Fishing Rod")
    type_string("p!dep all")
    time.sleep(1)
    type_string("p!with 50")
    time.sleep(1)
    type_string("p!buy fishing rod")
    time.sleep(2)
    messageid = (get_message(False)['id'])
    headers = {
        'authorization': 'put your authorization token here'
    }
    requests.put(f'https://discord.com/api/v9/channels/{channelid}/messages/{messageid}/reactions/@@FILL THIS PART IN@@', headers=headers)
    time.sleep(1)
# Function to run the Highlow game 
def highlow():
    print("highlow")
    type_string("p!highlow")
    time.sleep(1)
    if highlowcheck():
        type_string("low")
    else:
        type_string("high")
    time.sleep(30)



# Example usage
if __name__ == "__main__":
    # highlow delay is 30 seconds
    # fish is 1 minute (though the fishing rod has a chance to break and you have to select the check to buy it and you can't do that with code, unless you can find the position of the button, lot of code for that so come back to it)
    # work is 5 minutes
    # trivia is 10 minutes

    print("Starting in")
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    time.sleep(1)
    while True:
        # trivia
        print("trivia")
        trivia()
        time.sleep(0.5)
        type_string("p!dep all")
        time.sleep(1)
        for i in range(0, 2):
            #work
            print("work")
            type_string("p!work")
            time.sleep(1)
            type_string("p!dep all")
            time.sleep(1)
            for i in range(0, 5):
                #fish
                print("Fishing")
                type_string("p!fish")
                time.sleep(1)
                try:
                    if (get_message(False)['content'].split("> ")[1]=="Your fishing rod broke! Go buy a new one to start fishing again"):
                        buy_fishing_rod()
                except Exception as e:
                    print("Fishing rod not broken")
                for i in range(0,2):
                    #highlow
                    highlow()