import requests
from bs4 import BeautifulSoup

#This code is for the Rubber Ducky activity in the CTF activity used at the Radford Summer Camps
#Sorry this code is a mess, it was made very quickly and had to be fixed during the activity
#Before starting this code, find each mention of <Edit this> to find each variable that must be changed before running

# <Edit this> Ctfd server has the option to create a API access token, create one and put it here as well as the ip of the Ctfd server
token = 'Ctfd token here'
ctfdServerIp = 'ctfd_ip_here'

class Computer(object):
    def __init__(self, ip, CompName, ID):
        self.ip = ip
        self.CompName = CompName
        self.users = []
        self.PwnTeams = {}
        self.pairs = []
        self.TeamNames = {}
        self.TeamID = 0
        self.HasTeam = False
        if ID == 0:
            self.TeamID = self.GetTeamID()
            if self.TeamID == 1:
                self.HasTeam = True
        else:
            self.TeamID = ID
            self.HasTeam = True
            # The rubber duckies just say team 1,2,3, or 4 as the pwn team so you'll need to map the teamID's being used to team 1,2,3,4
            # <Edit this> edit self.pairs to hold the teamID's you'll be using for team 1,2,3, and 4
        self.pairs = [8,9,10,11]
            # <Edit this> This holds the team name mappings to teamID's, you can probably get WebMain to replace the team names as that's what displays it but I had to rush it so I just copied it over.
        self.TeamNames = {1:"admin",2:"test",3:"user 1",8:"Teamone",9:"Teamtwo",10:"Teamthree",11:"Teamfour"}

    # adds a computer user to machine information
    def add_user(self, user):
        self.users.append(user)

    # adds a pwn to the list of pwns for the machine, also gives points to the team that pwned the machine
    def add_pwn(self, pwnTeam):
        # Rubber ducky only contains team 1-4, This translates that to the actual team id being used
        print(f"Converted {pwnTeam} to {self.pairs[pwnTeam-1]}")
        pwnTeam = int(self.pairs[pwnTeam-1])
        
        print(f"adding pwn: {self.TeamNames[pwnTeam]}")
        # PwnTeams holds a list of team that have pwned the machine, this stops teams from getting multiple points from one machine
        if (pwnTeam not in self.PwnTeams):
            print(f"Team: {self.TeamNames[pwnTeam]} not pwned yet")
            # HasTeam is true if a teamid can be found
            print(f"HasTeam: {self.HasTeam}, TeamID: {self.TeamID}, pwnTeam: {pwnTeam}")
            # I made it only give points if a computer owned by a team is pwned so that people couldn't use external sources to gain points. If you'd like to change that, change this if statement to if True: or remove it
            if self.HasTeam:
                # Checks if the team id of the computer and the pwnteamID are the same, This stops someone from pwning their own machine
                print(f"checking {self.TeamID} vs {pwnTeam}")
                if (int(self.TeamID) == int(pwnTeam)):
                    print(f"Team {self.TeamID} owns this machine| You cannot pwn your own machine")
                    return
                print(f"giving the teamid: {pwnTeam} a point")
                # gives 10 points to the team that pwned the machine
                try:
                    print(
                        requests.post(
                            f"http://{ctfdServerIp}/api/v1/awards",
                            json={"name":"RubberDucky Score","value":"10","category":"Social Engineering","description":f"Pwned {self.TeamNames[self.TeamID]}","icon":"code","user_id":pwnTeam},
                            headers={"Content-Type": "application/json", "Authorization": f"Token {token}"},
                        )
                    )
                except:
                    # If there is no connection, it marks the pwnteam as false to show that they have not been given points
                    print("No connection")
                    print(f"{self.TeamNames[pwnTeam]} with id {pwnTeam} has pwned this machine But has not been scored due to a missing connection to the server")
                    return
                print(f"{self.TeamNames[pwnTeam]} with id {pwnTeam} has pwned this machine")
                # A pwntTeam is set to true when it is scored, this lets me know if someone is not being scored and prevents double scoring
                self.PwnTeams[pwnTeam] = True 

                return
            # if a machine does not have a team it does not score the pwns and gives this error message, then trys to find it again, if it does, it scored the pwns
            print(f"Team:{self.TeamID} does not have team\nVariables: {self.HasTeam}, {self.TeamID}, {pwnTeam}")
            checkifFound = self.GetTeamID()
            if checkifFound == 0:
                self.PwnTeams[pwnTeam] = False
            else:
                print("Found a teamid")
                self.count_Score()
        else:
            print(f"Team {pwnTeam} has already pwned this machine.")
            return

    # returns a list of teams that have pwned the machine in html code format
    def get_pwns(self):
        print("getting pwns")
        pwns = "<ul class=\"pwns\">\n"
        for i in self.PwnTeams:
            print(i)
            # if self.PwnTeams[i]:
            #     pwns += f"<li><a href=\"/team/{i}\">{self.TeamNames[i]}</a></li>\n"
            if self.PwnTeams[i]:
                pwns += f"<li><a href=\"/team/{i}\">{self.TeamNames[i]} | Scored</a></li>\n"
            else:
                pwns += f"<li><a href=\"/team/{i}\">{self.TeamNames[i]} | Not Scored</a></li>\n"
        pwns += "</ul>\n"
        return pwns

    #Tries to find a team ID
    def GetTeamID(self):
        print("Getting ID")
        if self.HasTeam:
            print("already has id")
            return self.TeamID
        id = 0
        # Queries the website for users with the ip of the machine
        try:
            output = requests.get(
            f"http://{ctfdServerIp}/admin/users?field=ip&q={self.ip}",
            headers={"Content-Type": "application/json", "Authorization": f"Token {token}"},
            )
        except:
            print("No connection")
            return id
        soup = BeautifulSoup(output.content, "html.parser")

        # Sorts through the HTML data for the team id
        for tbody in soup.find_all("tbody"):
            for td in tbody.find_all("td"):
                # Iterates through possible team id's
                if td.get("class", [])[0] == 'team-id':
                    id = int(td.text.strip())
                    print(self.users)
                    print(int(id) in self.pairs)
                    # if one of the team id's associated with the IP is in the pairs variable, return that id
                    if int(id) in self.pairs:
                        print(f"{self.ip} has team id {id}")
                        self.TeamID = id
                        self.count_Score()
                        return id
                elif td.get("class", [])[0] == 'team-name':
                    print(f"{self.ip} is part of {td.text.strip()}")

        print(id)
        if id == 0:
            print(f"{self.ip} is not part of a team")
        elif id > 0:
            print(f"{self.ip} has team id {id}")
            self.TeamID = id
            self.count_Score()

        return id
    # manual definition of teamID
    def make_team(self, teamnum):
        self.TeamID = teamnum
        self.count_Score()

    # Function to score any unscored pwns
    def count_Score(self):
        pwnedself = False
        
        #Checks if it has a teamID
        if self.TeamID == 0:
            self.TeamID = self.GetTeamID()
            if self.TeamID == 0:
                print("Still no team")
                return
            
        self.HasTeam = True
        print("hasTeam is True")
        print(f"{self.ip} is now part of a team")
        print("Fixing Score")

        # Iterates through pwnTeams and if one is false, it tries to give them points
        for i in self.PwnTeams:
            if self.PwnTeams[i]:
                print(f"Already scored team {i}")
                break

            print(f"giving points for teamid {i}")
            if int(i) == int(self.TeamID):
                print(f"Team {i} owns this machine| You cannot pwn your own machine")
                pwnedself = True
            elif not self.PwnTeams[i]:
                print(f"Team {i} has pwned {self.ip}")
                try:
                    print(
                        requests.post(
                            f"http://{ctfdServerIp}/api/v1/awards",
                            json={"name":"RubberDucky Score","value":"10","category":"Social Engineering","description":"Pwned","icon":"code","user_id":7+i},
                            headers={"Content-Type": "application/json", "Authorization": f"Token {token}"},
                        ).text
                    )
                except:
                    print(f"{self.TeamNames[i]} with id {i} has pwned this machine But has not been scored due to a missing connection to the server")
                    return
                self.PwnTeams[i] = True
        if pwnedself:
            print(f"removing {self.TeamID} from pwned list")
            self.PwnTeams.pop(self.TeamID, None)


    def load_pwn(self, pwnTeamID, pwned):
        self.PwnTeams[pwnTeamID] = pwned
