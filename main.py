import requests
from bs4 import BeautifulSoup
import pprint
import re
import json

#builds our database by getting the html of the users.php page on myanimelist, soup makes it formatted nicely
#and allows us to find all href links which will allow us to gather a list of usernames
#this list of usernames will be used later to build out database with likes as well as dislikes

#returns a list of users from the link myanimelist.nte/users.php(this link only shows the 20 most recent users to log on)
def usersbuilder():
    users = requests.get("http://myanimelist.net/users.php")
    soup = BeautifulSoup(users.text, 'html.parser')
    test = soup.find_all("a", href=re.compile("profile"))
    userlist = []
    for x in range(len(test)):
        if x %2 == 0:
            userlist.append(test[x].getText())
            # print(test[x].getText())
    print(userlist)

#returns a list of tuples containing every manga a person has on their myanimelist along with the score they have given it
def usersscores(username):
    #grabs the mangalist of the username passed
    user = requests.get(f"https://myanimelist.net/mangalist/{username}")
    mangalist = BeautifulSoup(user.text, 'html.parser')
    mangalist_data = mangalist.table["data-items"]
    newstring = re.sub(r',"priority_string":"[A-Za-z]*"},', "}Splithere", mangalist_data)
    new_manga_list = re.split("Splithere", newstring)
    mangadictlist = []
    for x in range(len(new_manga_list)):
        if x == 0:
            temp = new_manga_list[x][1:]
            new_manga_list[x] = temp
        if x == len(new_manga_list)-1:
            temp = new_manga_list[x][:-1]
            new_manga_list[x] = temp
        if len(new_manga_list[x]) > 0:
            res = json.loads(new_manga_list[x])
            mangadictlist.append(res)
    return mangadictlist

new_list = (usersscores("LEVI_ARPIT"))
for x in new_list:
  print(f"name is {x['manga_title']} and the score is {x['score']}")
# usersscores("marecho")