import pyautogui
import time
import keyboard
import requests
import json
import sqlite3
from bs4 import BeautifulSoup
import urllib.parse

conn = sqlite3.connect('trivia.db')

c = conn.cursor()

# c.execute("""DROP TABLE trivia""")
# c.execute("""CREATE TABLE trivia  (
#             id Integer PRIMARY KEY,
#             question TEXT,
#             answer TEXT
#             )""")

def get_id(question):
    html_question = urllib.parse.quote_plus(question)
    tdb_query = "https://opentdb.com/browse.php?query="
    query = requests.get(tdb_query + html_question + "&type=Question#")
    # print(query.text.split('ID')[1])
    try:
        id = query.text.split('ID')[1].split('<td>')[1][:-5]
        return int(id)
    except Exception as e:
        print("Error in get_id")
        print("Question: " + question)
        print("URL: " + tdb_query + html_question + "&type=Question")

def type_string(string):
    pyautogui.typewrite(string)
    pyautogui.press('enter')

def get_message():
    # put channel id here
    channelid = 000000000000
    headers = {
        'authorization': 'put your authorization token here'
    }
    r = requests.get(f'https://discord.com/api/v9/channels/{channelid}/messages?limit=8', headers=headers)
    jsonn = json.loads(r.text)

    return jsonn

def get_trivia_message():
    jsonn = get_message()
    trivia_message = "To win 🥞500, answer this question in `10 seconds`"
    bot_name = "Pancake"
    for i in range(0, len(jsonn)):
        try:
            if (jsonn[i]['content'] == trivia_message and jsonn[i]['author']['username'] == bot_name):
                return jsonn[i]
        except Exception as e:
            1+1
    

def get_trivia_answers():
    answer = " "
    old_answer = "placeholder"

    while(True):
        try:
            if (get_trivia_message()['embeds'][0]['description'].split("\n")[0] != None):
                question = get_trivia_message()['embeds'][0]['description'].split("\n")[0]
                id = get_id(question)
                if (c.execute("SELECT * FROM trivia WHERE id = " + str(get_id(question))).fetchone() == None):
                    print("question not in database")
                answer = c.execute("SELECT answer FROM trivia WHERE id = " + str(get_id(question))).fetchone()[0]
                if answer == old_answer:
                    continue
                print("Trivia question found!!, answer: " + answer)
                old_answer = answer
        except Exception as e:
            1+1

def get_smessage_id():
    jsonn = get_message()
    bot_name = "Pancake"
    fmessage = "Are you sure you want to sell "
    for i in range(0, len(jsonn)):
        try:
            if (jsonn[i]['content'][:len(fmessage)] == fmessage and jsonn[i]['author']['username'] == bot_name):
                return jsonn[i]['id']
        except Exception as e:
            1+1
    print("Error in get_fmessage_id")

def sell_fish():
    # put channel id here
    channelid = 0000000000000000
    print("selling common fish")
    type_string("p!sell common")
    time.sleep(2)
    messageid = (get_smessage_id())
    # put authorization id here
    headers = {
        'authorization': 'put your authorization token here'
    }
    requests.put(f'https://discord.com/api/v9/channels/{channelid}/messages/{messageid}/reactions/@@FILL THIS PART IN@@', headers=headers)

                

def add_questions():
    # Count cannot be greater than 50
    count = 50
    difficulty = "hard"
    API = "https://opentdb.com/api.php?amount={cnt}&difficulty={dflty}".format(cnt=count, dflty=difficulty)

    while(True):
        data = requests.get(API)
        for i in range(count):
            question = json.loads(data.text)['results'][i]['question']
            formatted_question = BeautifulSoup(question).getText()
            answer =  BeautifulSoup(json.loads(data.text)['results'][i]['correct_answer']).getText()
            id = get_id(formatted_question)
            # print(str(id) + " | " + formatted_question + " | " + answer)
            try:
                if (c.execute("SELECT * FROM trivia WHERE id = " + str(id)).fetchone() == None):
                    c.execute("INSERT INTO trivia (id, question, answer) VALUES (?, ?, ?)", (id, formatted_question, answer))
                    print("Added question")
                    print(str(id) + " | " + formatted_question + " | " + answer)
                    conn.commit()
                else:
                    1 + 1
                    # print("Question already exists")
            except Exception as e:
                print("Error in add_questions")

add_questions()
# get_trivia_answers()
# time.sleep(1)
# while(True):
#     sell_fish()
#     type_string("p!dep all")

# question = "In the 1976 film 'Taxi Driver', how many guns did Travis buy from the salesman?"
# id = get_id(question)
# answer = "4"
# print(id)
# oldid = 18958

# print(str(c.execute("SELECT * FROM trivia WHERE id = " + str(oldid)).fetchone()))

# query = "SELECT * FROM trivia WHERE question = ?"
# print(str(c.execute(query, (question,)).fetchone()))

# print(str(c.execute("UPDATE trivia SET answer = ? WHERE question = ?", (answer, question)).fetchone()))
# print(str(c.execute("DELETE FROM trivia WHERE id = ?", (oldid,)).fetchone()))

# print(str(c.execute("SELECT * FROM trivia WHERE id = " + str(id)).fetchone()))

# print(str(c.execute("SELECT * FROM trivia WHERE id = " + str(oldid)).fetchone()))


# count = 10
# r = requests.get(f'https://opentdb.com/api.php?amount={count}&difficulty=hard')
# jsonn = json.loads(r.text)





conn.commit()

conn.close()
