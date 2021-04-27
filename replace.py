import os

#file = open("templates/home.html","r")
#lignes = file.readlines()
#file.close()
#L = [1,2,3,4,5,6,7]
#z = lignes[40]
#print(z)
#z = int(z[92])

#print(z)
#z = z +1
#if z ==8 :
    #z=0
#z = str(z)
#print(z)
#lignes[40] = '		<button class="carte" onclick="updateBtn()"><img id="imgbtn" src="/static/pokemon/{{carte['+z+']}}"></button>\n'
#file = open("templates/home.html","w")
#file.writelines(lignes)
#file.close()
file = open("transfere.txt", "r")
lignes = file.readlines()
file.close()
n=[0,0,0,0,0,0,0,0]
n=str(n)
lignes[0] = n+'\n'

file = open("transfere.txt","w")
file.writelines(lignes)
file.close()
