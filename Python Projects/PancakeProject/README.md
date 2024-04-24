# Welcome to Pancake Project
### How to make this work
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

you want to copy whats next to authorization id and paste it into the authorization variable
