# Welcome to Pancake Project
## Dependencies
pyautogui
``pip install pyautogui``

keyboard
``pip install keyboard``

requests
``pip install requests``

BeautifulSoup
``pip install beautifulsoup4``

## How to make this work
I had to make the URL's not work so i didn't accidentally give out a way to control my discord account, here is the process to get ones that will work with yours
What you will need:
- Channel ID
- authorization id
- reaction request URL

#### ChannelID
Right-click on the channel you plan on using this script in then select copy channel id and paste that into every channel id variable in both scripts

#### Authorization id
for this youll need to login to discord in your browser, not the app. go to the channel you want to use, then click the 3 dots at the top right if you're using chrome

![image](https://github.com/MrWizard27/CodingProjects/assets/130387713/a09e3126-fe26-4afd-b434-133fc6dfd6c0)

then click more tools, then developer tools
then click network, it should look like this

![image](https://github.com/MrWizard27/CodingProjects/assets/130387713/6ee7f1a1-4e8e-49ee-bcd3-dc530e4e5603)

Now start typing in the chat but don't send it, you should get a packet called typing in the network tab, this is where your authorization id is

![image](https://github.com/MrWizard27/CodingProjects/assets/130387713/5276cbec-5ce6-4994-b826-18c41218e5d8)

you want to copy whats next to authorization id and paste it where it says to put your authorization variable

#### Reaction Request URL
To get this you need to sell your fishing rod, then buy another one, when you react to the message to buy it, record the url for that 
it should be the one called %40me?location

![image](https://github.com/MrWizard27/CodingProjects/assets/130387713/d5f8206a-f885-4b32-81c8-d8a287e3366a)

copy that request url and paste the part that isn't in the code, make sure the code still has the {channelid} and {messageid} parts or it won't react to the most recent message, so basically everything after /reactions/
it should look something like this with the only part different after reactions
https://discord.com/api/v9/channels/{channelid}/messages/{messageid}/reactions/check%4B320790211071085690/%40me?location=Message&type=0

Now it should be all setup, you can run it with ``python PancakeScriptMK1.py`` It'll count down from 3 and then start automatically playing all the games

if you want to use the trivia part you'll need to get the trivia db filled in, check out the process from there

## Shoutout to Amrios and Codium, Amrios has a really good trivia bot which is where I learned how the trivia for pancake bot worked and was able to make my own version. Codium has a really good tutorial on how to use python requests to get discord messages and is what i used to start this project

https://www.youtube.com/watch?v=xh28F6f-Cds

https://github.com/amrios/tdb-pancakes

# Making the trivia Database

This is a hard part if you don't know SQL, plus my db filler has a lot of example code i used for debugging so it will be hard to navigate.
make sure to do all the steps you did to set up the pancake script to the trivia database, it has a lot of the same methods

#### First step, creating the database

comment out the add_questions() at the bottom (put # in front of it)
then uncomment out the
# c.execute("""DROP TABLE trivia""")
# c.execute("""CREATE TABLE trivia  (
#             id Integer PRIMARY KEY,
#             question TEXT,
#             answer TEXT
#             )""")
at the top
run the script, it will create you trivia table
make sure to comment that part out again or your database will be cleared after everyrun

now uncomment the add_questions() and run the script, it will fill your db with a bunch of answers to trivia questions. the pancake script will also add the answers to unknown questions as well

if you have any questions feel free to message me
