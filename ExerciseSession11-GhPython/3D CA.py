"""Provides a scripting component.
    Inputs:
        x: The x script variable
        y: The y script variable
    Output:
        a: The a output variable"""

__author__ = "laoma"
__version__ = "2022.03.12"

import rhinoscriptsyntax as rs
import random
from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import Rhino.Geometry as rg


class Cell:
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z
    self.type = None

class Cell_void(Cell):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.type = 'void'
        self.neighbours = []
        self.food=0
        self.ffood=0
        self.office_supplies=0
        self.furniture=0
        self.daily=0

    def behaviour(self):
        office = 0
        for n in self.neighbours:
            if n.type == 'office':
                office += 1
        if office<=15:
            return 'office'
        else:
            return 'void'


    def getNeighbourCoordinates(self):
        neighbours = []
        list1=[-10,0,10]
        list2=[-4,0,4]
        for i in list1:
            for j in list1:
                for k in list2:
                    neighbours.append([self.x+i, self.y+j, self.z+k])
        neighbours.remove([self.x,self.y,self.z])
        return neighbours

class Cell_office(Cell):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.type = 'office'
        self.neighbours = []
        self.food=0.0013*20
        self.ffood=0.001*20
        self.office_supplies=0.0063*20
        self.furniture=0.746*20
        self.daily=0.017*20

    def behaviour(self):
        nrlive = 0
        resi=0
        for n in self.neighbours:
            if n.type == 'office':
                nrlive += 1
            if n.type =='residence':
                resi+=1
        if nrlive<=7:
            return 'office'
        elif 10<=nrlive<=12:
            return 'residence'
        elif nrlive>=20:
            return 'void'
        else:
            return 'office'


    def getNeighbourCoordinates(self):
        neighbours = []
        list1=[-10,0,10]
        list2=[-4,0,4]
        for i in list1:
            for j in list1:
                for k in list2:
                    neighbours.append([self.x+i, self.y+j, self.z+k])
        neighbours.remove([self.x,self.y,self.z])
        return neighbours

class Cell_restaurant(Cell):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.type = 'restaurant'
        self.neighbours = []
        self.food=0.15*15
        self.ffood=0.09*15
        self.office_supplies=0.0008*15
        self.furniture=0.375*15
        self.daily=0.005*15

    def behaviour(self):
        nrlive = 0
        for n in self.neighbours:
            if n.type == 'restaurant':
                nrlive += 1
        if nrlive <=3:
            return 'market'
        elif 11<=nrlive<=17:
            return 'market'

        elif nrlive>=22:
            return 'void'
        else:
            return 'restaurant'

    def getNeighbourCoordinates(self):
        neighbours = []
        list1=[-10,0,10]
        list2=[-4,0,4]
        for i in list1:
            for j in list1:
                for k in list2:
                    neighbours.append([self.x+i, self.y+j, self.z+k])
        neighbours.remove([self.x,self.y,self.z])
        return neighbours

class Cell_market(Cell):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.type = 'market'
        self.neighbours = []
        self.food=0.0008*20
        self.ffood=0.0006*20
        self.office_supplies=0.0017*20
        self.furniture=0.221*20
        self.daily=0.55*20

    def behaviour(self):
        nrlive = 0
        for n in self.neighbours:
            if n.type == 'market':
                nrlive += 1
        if nrlive <=3:
            return 'residence'
        elif 8<=nrlive<=17:
            return 'restaurant'
        elif nrlive>=18:
            return 'void'

        else:
            return 'market'

    def getNeighbourCoordinates(self):
        neighbours = []
        list1=[-10,0,10]
        list2=[-4,0,4]
        for i in list1:
            for j in list1:
                for k in list2:
                    neighbours.append([self.x+i, self.y+j, self.z+k])
        neighbours.remove([self.x,self.y,self.z])
        return neighbours

class Cell_residence(Cell):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.type = 'residence'
        self.neighbours = []
        self.food=0.005*8
        self.ffood=0.003*8
        self.office_supplies=0.0003*8
        self.furniture=1.113*8
        self.daily=0.021*8

    def behaviour(self):
        nrlive = 0
        for n in self.neighbours:
            if n.type == 'residence':
                nrlive += 1
        if nrlive <=3:
            return 'office'

        elif 11<=nrlive<=13:
            return 'market'
        elif 17<=nrlive<=19:
            return 'education'
        elif nrlive>=20:
            return 'void'
        else:
            return 'residence'

    def getNeighbourCoordinates(self):
        neighbours = []
        list1=[-10,0,10]
        list2=[-4,0,4]
        for i in list1:
            for j in list1:
                for k in list2:
                    neighbours.append([self.x+i, self.y+j, self.z+k])
        neighbours.remove([self.x,self.y,self.z])
        return neighbours

class Cell_education(Cell):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.type = 'education'
        self.neighbours = []
        self.food=0.0018*50
        self.ffood=0.001*50
        self.office_supplies=0.009*50
        self.furniture=0.294*50
        self.daily=0.007*50

    def behaviour(self):
        nrlive = 0
        for n in self.neighbours:
            if n.type == 'education':
                nrlive += 1
        if nrlive <=3:
            return 'education'
        elif 11<=nrlive<=13:
            return 'residence'
        elif nrlive>=20:
            return 'void'
        else:
            return 'education'

    def getNeighbourCoordinates(self):
        neighbours = []
        list1=[-10,0,10]
        list2=[-4,0,4]
        for i in list1:
            for j in list1:
                for k in list2:
                    neighbours.append([self.x+i, self.y+j, self.z+k])
        neighbours.remove([self.x,self.y,self.z])
        return neighbours

class Cell_space(Cell):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.type = 'space'
        self.neighbours = []
        self.food=0
        self.ffood=0
        self.office_supplies=0
        self.furniture=0
        self.daily=0

    def behaviour(self):
        office = 0
        residence=0
        restaurant=0
        market=0
        education=0
        space=0
        for n in self.neighbours:
            if n.type == 'office':
                office += 1
            elif n.type == 'residence':
                residence += 1
            elif n.type == 'restaurant':
                restaurant += 1
            elif n.type == 'market':
                market += 1
            elif n.type == 'education':
                education += 1
            elif n.type == 'space':
                space += 1
        if office>=9:
            return 'office'
        if residence>=9:
            return 'residence'



    def getNeighbourCoordinates(self):
        neighbours = []
        list1=[-10,0,10]
        list2=[-4,0,4]
        for i in list1:
            for j in list1:
                for k in list2:
                    neighbours.append([self.x+i, self.y+j, self.z+k])
        neighbours.remove([self.x,self.y,self.z])
        return neighbours

envcell=[]
for k in range(51):
    for i,j in zip(X,Y):
        if int(i)%5!=0:
            i=i+1
        if int(j)%5!=0:
            j=j+1
        envcell.append((int(i),int(j),int(k)*4+2))
spacecell=envcell[:]

celldict={}
if officeX != None:
    for i,j,k in zip(officeX,officeY,officeZ):
        if int(i)%5!=0:
            i=i+1
        if int(j)%5!=0:
            j=j+1
        c=Cell_office(int(i),int(j),int(k))
        celldict[int(i),int(j),int(k)]=c
        if spacecell.__contains__((int(i),int(j),int(k)))==True:
            spacecell.remove((int(i),int(j),int(k)))
if restaurantX != None:
    for i,j,k in zip(restaurantX,restaurantY,restaurantZ):
        if int(i)%5!=0:
            i=i+1
        if int(j)%5!=0:
            j=j+1
        c=Cell_restaurant(int(i),int(j),int(k))
        celldict[int(i),int(j),int(k)]=c
        if spacecell.__contains__((int(i),int(j),int(k)))==True:
            spacecell.remove((int(i),int(j),int(k)))
if commerceX != None:
    for i,j,k in zip(commerceX,commerceY,commerceZ):
        if int(i)%5!=0:
            i=i+1
        if int(j)%5!=0:
            j=j+1
        c=Cell_market(int(i),int(j),int(k))
        celldict[int(i),int(j),int(k)]=c
        if spacecell.__contains__((int(i),int(j),int(k)))==True:
            spacecell.remove((int(i),int(j),int(k)))
if residenceX != None:
    for i,j,k in zip(residenceX,residenceY,residenceZ):
        if int(i)%5!=0:
            i=i+1
        if int(j)%5!=0:
            j=j+1
        c=Cell_residence(int(i),int(j),int(k))
        celldict[int(i),int(j),int(k)]=c
        if spacecell.__contains__((int(i),int(j),int(k)))==True:
            spacecell.remove((int(i),int(j),int(k)))
if educationX != None:
    for i,j,k in zip(educationX,educationY,educationZ):
        if int(i)%5!=0:
            i=i+1
        if int(j)%5!=0:
            j=j+1
        c=Cell_education(int(i),int(j),int(k))
        celldict[int(i),int(j),int(k)]=c
        if spacecell.__contains__((int(i),int(j),int(k)))==True:
            spacecell.remove((int(i),int(j),int(k)))
for v in spacecell:
    c=Cell_space(v[0],v[1],v[2])
    celldict[v[0],v[1],v[2]]=c

for i in celldict:
    c=celldict[i]
    neigourCoords = c.getNeighbourCoordinates()
    for n in neigourCoords:
       if celldict.__contains__((n[0],n[1],n[2]))==True:
           c.neighbours.append(celldict[n[0],n[1],n[2]])


def evaluate(dict):
    food=Food
    frozen_food=Frozen_food
    office_supplies=Office_supplies
    furniture=Furniture
    daily_necessities=Daily_necessities
    nextCellDict={}
    for i in dict:
        c = dict[i]
        next = c.behaviour()
        if next == 'office':
            nCell = Cell_office(c.x,c.y,c.z)
            food=food+c.food-nCell.food
            frozen_food=frozen_food+c.ffood-nCell.ffood
            office_supplies=office_supplies+c.office_supplies-nCell.office_supplies
            furniture=furniture+c.furniture-nCell.furniture
            daily_necessities=daily_necessities+c.daily-nCell.daily
            if food>=0 and frozen_food>=0 and office_supplies>=0 and furniture>=0 and daily_necessities>=0:
                nextCellDict[c.x,c.y,c.z] = nCell
        elif next == 'restaurant':
            nCell = Cell_restaurant(c.x,c.y,c.z)
            food=food+c.food-nCell.food
            frozen_food=frozen_food+c.ffood-nCell.ffood
            office_supplies=office_supplies+c.office_supplies-nCell.office_supplies
            furniture=furniture+c.furniture-nCell.furniture
            daily_necessities=daily_necessities+c.daily-nCell.daily
            if food>=0 and frozen_food>=0 and office_supplies>=0 and furniture>=0 and daily_necessities>=0:
                nextCellDict[c.x,c.y,c.z] = nCell
        elif next == 'market':
            nCell = Cell_market(c.x,c.y,c.z)
            food=food+c.food-nCell.food
            frozen_food=frozen_food+c.ffood-nCell.ffood
            office_supplies=office_supplies+c.office_supplies-nCell.office_supplies
            furniture=furniture+c.furniture-nCell.furniture
            daily_necessities=daily_necessities+c.daily-nCell.daily
            if food>=0 and frozen_food>=0 and office_supplies>=0 and furniture>=0 and daily_necessities>=0:
                nextCellDict[c.x,c.y,c.z] = nCell
        elif next == 'residence':
            nCell = Cell_residence(c.x,c.y,c.z)
            food=food+c.food-nCell.food
            frozen_food=frozen_food+c.ffood-nCell.ffood
            office_supplies=office_supplies+c.office_supplies-nCell.office_supplies
            furniture=furniture+c.furniture-nCell.furniture
            daily_necessities=daily_necessities+c.daily-nCell.daily
            if food>=0 and frozen_food>=0 and office_supplies>=0 and furniture>=0 and daily_necessities>=0:
                nextCellDict[c.x,c.y,c.z] = nCell
        elif next == 'education':
            nCell = Cell_education(c.x,c.y,c.z)
            food=food+c.food-nCell.food
            frozen_food=frozen_food+c.ffood-nCell.ffood
            office_supplies=office_supplies+c.office_supplies-nCell.office_supplies
            furniture=furniture+c.furniture-nCell.furniture
            daily_necessities=daily_necessities+c.daily-nCell.daily
            if food>=0 and frozen_food>=0 and office_supplies>=0 and furniture>=0 and daily_necessities>=0:
                nextCellDict[c.x,c.y,c.z] = nCell
        elif next == 'void':
            nCell = Cell_void(c.x,c.y,c.z)
            nextCellDict[c.x,c.y,c.z] = nCell
            food=food+c.food
            frozen_food=frozen_food+c.ffood
            office_supplies=office_supplies+c.office_supplies
            furniture=furniture+c.furniture
            daily_necessities=daily_necessities+c.daily
        else:
            c.neighbours = []
            nextCellDict[c.x,c.y,c.z] = c

    for i in nextCellDict:
        c = nextCellDict[i]
        neigourCoords = c.getNeighbourCoordinates()
        for n in neigourCoords:
            if nextCellDict.__contains__((n[0],n[1],n[2]))==True:
                c.neighbours.append(nextCellDict[n[0],n[1],n[2]])

    dict = nextCellDict
    return dict,food,frozen_food,office_supplies,furniture,daily_necessities

officelist=[]
restaurantlist=[]
marketlist=[]
residencelist=[]
educationlist=[]
voidlist=[]

for g in range(int(generation)):
    officelist=[]
    restaurantlist=[]
    marketlist=[]
    residencelist=[]
    educationlist=[]
    voidlist=[]
    for i in celldict:
        c=celldict[i]
        if c.type=='office':
            officelist.append([c.x,c.y,c.z])
        elif c.type=='restaurant':
            restaurantlist.append([c.x,c.y,c.z])
        elif c.type=='market':
            marketlist.append([c.x,c.y,c.z])
        elif c.type=='residence':
            residencelist.append([c.x,c.y,c.z])
        elif c.type=='education':
            educationlist.append([c.x,c.y,c.z])
        elif c.type=='void':
            voidlist.append([c.x,c.y,c.z])
    celldict,cfood,cffood,coffice,cfurniture,cdaily=evaluate(celldict)

officepoints=[]
restaurantpoints=[]
marketpoints=[]
residencepoints=[]
educationpoints=[]
voidpoints=[]
for p in officelist:
    point3d=rg.Point3d(int(p[0]),int(p[1]),int(p[2]))
    officepoints.append(point3d)
for p in restaurantlist:
    point3d=rg.Point3d(int(p[0]),int(p[1]),int(p[2]))
    restaurantpoints.append(point3d)
for p in marketlist:
    point3d=rg.Point3d(int(p[0]),int(p[1]),int(p[2]))
    marketpoints.append(point3d)
for p in residencelist:
    point3d=rg.Point3d(int(p[0]),int(p[1]),int(p[2]))
    residencepoints.append(point3d)
for p in educationlist:
    point3d=rg.Point3d(int(p[0]),int(p[1]),int(p[2]))
    educationpoints.append(point3d)
for p in voidlist:
    point3d=rg.Point3d(int(p[0]),int(p[1]),int(p[2]))
    voidpoints.append(point3d)
