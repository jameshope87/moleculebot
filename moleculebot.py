import random
import requests
from bs4 import BeautifulSoup
import html5lib
import os
from sendemail import *
from credentials import *

#Below will start scraping the site
url = 'http://www.chm.bris.ac.uk/motm/motm.htm'
response = requests.get(url)
soup = BeautifulSoup(response.content, "html5lib")
name = soup.find_all('option')

#This creates a list of all the molecules
molecule_list = []
for a in name:
    molecule_list.append(a.text)

#writes the molecule list to a file
#with open("moleculelist.py", "w") as f:
#    f.write(molecule_list)

#This generates a random number according to length of the list
rand_num = random.randint(2,len(molecule_list))
#print rand_num

#This prints the random index.  You can change print to a variable and use it with email
#print molecule_list[rand_num]
#print (molecule_list[rand_num])

#check for cache file and make blank list if notm
if not os.path.isfile("usedmolecules.txt"):
    usedmolecules =[]
#if cachfile exists use it as a list
else:
    with open("usedmolecules.txt","r") as f:
        usedmolecules=f.read()
        usedmolecules=usedmolecules.split("\n")
        usedmolecules=filter(None, usedmolecules)
        usedmolecules=map(int, usedmolecules)

#print used molecules list to check
if len(usedmolecules)>(len(molecule_list)/2):
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddr, "Warning, we are running out of molecules to choose from!")
    server.quit()


    
print "Currently used molecules are: ", usedmolecules

moleculelist=[]
#Get three random molecules and put them in moleculelist
def getmolecules(number):
    templist=[]
    i=0
    while i<number:
        rand_num = random.randint(2,len(molecule_list))
        #check random number has not already been chosen
        if rand_num not in usedmolecules:
            #get the molecule name and add it to the temp list
            b = str(molecule_list[rand_num])[:-1]
            templist.append(b)
            usedmolecules.append(rand_num)
            i+=1
    #add chosen molecules to the cache    
    with open("usedmolecules.txt","w") as f:
        for num in usedmolecules:
            f.write(str(num) + "\n")
    #clear the input list and join lists
    del moleculelist[:]
    for mol in templist:
        moleculelist.append(mol)
    #this allows the current list to be output into a variable. Multiple lists of molecules can be made!
    return templist

def clearcache():
    del usedmolecules[:]
    with open("usedmolecules.txt","w") as f:
        f.write("")
#compose message
def message(listomolecules):
    return "Hello \n" + "The molecules picked for you this week are: \n" + "\n".join(listomolecules)

    

#email function
def mailmolecules(username, password, fromaddr, toaddr, msg):
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddr, msg)
    server.quit()

mailmolecules(username, password, fromaddr, toaddr, message(getmolecules(3)))

exit()
