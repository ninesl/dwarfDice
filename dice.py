# import enum
import random
import pygame as pg
from enum import Enum

class Die:
    def __init__(self, sides, color, setNum = None):
        self.isSelected = False
        self.num = -1
        self.isHovered = False
        self.baseColor = color

        self.sides = []
        for i in range(sides):
            if setNum:
                self.sides.append( Side(setNum, color, self) )
            else: 
                self.sides.append( Side(i + 1, color, self) ) 
                # create a side with i+1 pips
        self.curSide = self.sides[0]

    # def copySelf(self, deleteSides = []):
    #     if deleteSides:
    #         for index in deleteSides:


    # +1 for each 'thing'
    def getSellValue(self):
        val = 0
        val += self.getNumSides()
        for side in self.sides:
            if not side.mods:
                val += 1
            for pip in side.getPips():
                if pip.mod != Mod.BASE:
                    val += 1
        return val // 3
    
    def getNumSides(self):
        return len(self.sides)
    
    def select(self):
        self.isSelected = not self.isSelected #invert selection flag

    #returns value of a calculated side
    def rollDie(self):
        iSide = self.rollSide()
        self.curSide = iSide

        self.num = iSide.getCalculate()
        return self.num

    # returns random side
    def rollSide(self):
        return self.sides[random.randint(0, self.getNumSides() - 1)]
    
    def getColor(self):
        if self.isHovered:
            self.curSide.color.a = 50 #slightly transparent
        else:
            self.curSide.color.a = 255 #set to opaque
        return self.curSide.color
    
    def calculate(self):
        return self.curSide.getCalculate()
    
    def getMaxNum(self):
        max = Side(0, self.baseColor, self).getNum()
        for side in self.sides:
            if max < side.getNum():
                max = side.getNum()
        return max

    def addSide(self):
        newSideNum = self.getMaxNum() + 1
        self.sides.append( Side(newSideNum, self.baseColor, self) )

    def cascadeColors(self, incr):
        minusIncr = 0
        for side in self.sides:
            r = side.color.r + minusIncr
            g = side.color.g + minusIncr
            b = side.color.b + minusIncr

            if r > 255:
                r = 255
            if g > 255:
                g = 255
            if b > 255:
                b = 255

            if r < 0:
                r = 0
            if g < 0:
                g = 0
            if b < 0:
                b = 0

            side.color = pg.Color(r,g,b)
            minusIncr += incr

class Side:
    MAX_PIPS = 13
    def __init__(self, value, color, parentDie):
        self.parentDie = parentDie
        self.pips = []
        self.mods = []
        self.originalColor = color
        self.color = color
        self.baseScore = 1
        for _ in range(value):
            # self.pips.append(Pip())
            self.addNewPip()
    
    def getCalculate(self):
        score = 0
        for pip in self.pips:
            score += self.baseScore
            match pip.mod:
                case Mod.ATK:
                    score += 1
                    if self.hasATKMod():
                        score += 1
                # case Mod.DEF:
                #     break
                case Mod.GOLD:
                    score += 0
                case Mod.BASE:
                    score += 0
        return score
    
    def addNewPip(self):
        if self.getNum() < self.MAX_PIPS:
            self.pips.append(Pip())
            return True
        return False
    
    def getPips(self):
        #todo return pips for mod in DrawService graphics.py
        return self.pips
    
    def getNum(self):
        return len(self.pips)
    
    def addATKMod(self):
        self.mods.append(Mod.ATK)
        self.updateColor()

    def addGOLDMod(self):
        self.mods.append(Mod.GOLD)
        self.updateColor()

    def hasGOLDMod(self):
        return Mod.GOLD in self.mods
    def hasATKMod(self):
        return Mod.ATK in self.mods
    
    def updateColor(self):
        if self.hasGOLDMod() and self.hasATKMod():
            self.color = pg.Color(255,112,34)#gold/red
        elif self.hasGOLDMod():
            self.color = Mod.GOLD.value
        elif self.hasATKMod():
            self.color = Mod.ATK.value
        elif len(self.mods) == 0:
            self.color = self.originalColor

    # USE Mod ATK,DEF,GOLD etc
    # def setModSide(self, modEnum):
    #     self.modEnum = modEnum
        
class Pip:
    def __init__(self):
        self.isHovered = False
        self.mod = Mod.BASE

    def getPipColor(self):
        return self.mod.value
    
    def addATKMod(self):
        self.mod = Mod.ATK

    def addGOLDMod(self):
        self.mod = Mod.GOLD

    def isGOLDMod(self):
        return self.mod == Mod.GOLD

class Mod(Enum):
    ATK = pg.Color(101,0,0)
    # DEF = pg.Color(0,100,255,230)
    GOLD = pg.Color(255,171,34)
    BASE = pg.Color(0,0,0)
    # ATK  = pg.Color(0,0,0,230)

    # DEF  = pg.Color(0,0,0,230)
    # GOLD = pg.Color(0,0,0,230)

blankDie = Die(6, pg.Color(0,0,0,255), setNum=0)
# for side in blankDie.sides:
#     side.pips = []