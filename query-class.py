
class Query:
    def __init__(self,key,challenge,hostname):
        self.key = key
        self.challenge = challenge
        self.hostname = hostname



#test Query
myQuery = Query("darksouls","anorlondo","hostname")
print(myQuery.key,myQuery.challenge,myQuery.hostname)

#test list of Query
myQuery2 = Query("darksouls2","gutter","hostname")
queries = [myQuery,myQuery2]

for q in queries:
    print(q.key,q.challenge,q.hostname)

#
filename = "PROJ3-HNS.txt"

with open("PROJ3-HNS.txt",'r') as file:
    data = file.readlines()

print(data)
