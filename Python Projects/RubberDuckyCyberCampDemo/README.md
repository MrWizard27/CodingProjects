This project was part of a CTF for a few cyber summer camps to teach kids to be wary of unknown usb's and how quickly attackers can run attacks using those tools

This project hosts a web server that listens for a post request from a rubber ducky that was handed out. When the rubber ducky is plugged into an unsuspecting computer it invokes a web request to the web server containing user information on the pc and which team the rubber ducky belonged to.

This project works alongside a ctfd server, using the ip address of the "pwned" computer to query ctfd for their team name to display on the leaderboard. It also sends points to the team that owns the rubber ducky. it stores all the information gained from theses steps onto a leaderboard page.

This code was written very quickly and was edited on the fly to solve issues like having each group have new user account. There is a good chance the code will not work, it is currently being improved and a more stable version should be out soon.
