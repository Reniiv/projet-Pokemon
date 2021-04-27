import random
class Pokemon:


    def __init__ (self):
        self.list_Pokemon=[]
        hires = "_hires.png"
        for i in range(1,103):
            a= str(i) + hires
            self.list_Pokemon.append(a)

    
    def getlist_Pokemon(self):
        #Sort ma list de carte pokemon
        return self.list_Pokemon

   #Trie de ma liste par récursivté
    def tri(self):
            list = getlist_Pokemon()
            inferieur = [];
            pivot = [];
            superieur = []
            if len(list) < 2:
                return list
            pivotNombre = random.choice(list)
            for i in list:
                if i < pivotNombre:
                    inferieur.append(i)
                elif i > pivotNombre:
                    superieur.append(i)
                else:
                    pivot.append(i)
            return tri(inferieur) + pivot + tri(superieur)

    def proba(self):
        #Initialise ma liste de proba
        weigths = [1] * len(self.list_Pokemon)
        #Definit une valeur à une carte particuliere
        weigths[3] =0.01
        list_Pok = self.list_Pokemon
        L = []
        for i in range(6):
            #Sort 1 carte de ma liste avec les probabilité de la liste weight
            a=random.choices(list_Pok, weights=weigths, k=1)
            L.append(a[0])
            c= list_Pok.index(a[0])
            list_Pok.pop(list_Pok.index(a[0]))
            weigths.pop(c)
        return L
