import pygame as pg
import random as rand
import dice
import graphics
import events
import logic
import sounds
import animate

pg.init()
pg.display.set_caption("Dwarf Dice")
window_icon = pg.image.load("assets/pickaxe.png")
pg.display.set_icon(window_icon)


clock = pg.time.Clock()

WIDTH =  1920
HEIGHT = 1080

playerDice = []
rangeMin, rangeMax = 0,255
playerDice.append(dice.Die(6, pg.Color(rand.randint(rangeMin, rangeMax), 
                                       rand.randint(rangeMin, rangeMax),
                                       rand.randint(rangeMin, rangeMax))))
playerDice.append(dice.Die(6, pg.Color(rand.randint(rangeMin, rangeMax), 
                                       rand.randint(rangeMin, rangeMax),
                                       rand.randint(rangeMin, rangeMax))))
playerDice.append(dice.Die(6, pg.Color(rand.randint(rangeMin, rangeMax), 
                                       rand.randint(rangeMin, rangeMax),
                                       rand.randint(rangeMin, rangeMax))))
playerDice.append(dice.Die(6, pg.Color(rand.randint(rangeMin, rangeMax), 
                                       rand.randint(rangeMin, rangeMax),
                                       rand.randint(rangeMin, rangeMax))))
playerDice.append(dice.Die(6, pg.Color(rand.randint(rangeMin, rangeMax), 
                                       rand.randint(rangeMin, rangeMax),
                                       rand.randint(rangeMin, rangeMax))))


BACKGROUND_COLOR_RANGE = 100

SoundService = sounds.SoundService()

DrawService = graphics.DrawService(WIDTH, HEIGHT, NUM_SHAPES = 250, rangeNum=BACKGROUND_COLOR_RANGE)
AnimateService = animate.AnimateService(DrawService)

EventService = events.EventService()
LogicService = logic.LogicService(playerDice, DrawService)

SoundService.playMusic()

total = 0
for die in playerDice:
    die.rollDie()

going = True
#TODO FPS math?

recentHandScore = None

while going:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            going = False
        # elif event.type == pg.VIDEORESIZE:
        #     WIDTH = event.w
        #     HEIGHT = event.h
        #     DrawService.setScreen(WIDTH, HEIGHT, BACKGROUND_COLOR_RANGE)
        #     LogicService.unselectAll()

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1: #left mouse button
                d = EventService.selectRectDie(diceAndRect)
                if d:
                    SoundService.selectDiceSound(d.isSelected)
                else:
                    SoundService.diceDict["tap"].play()
                LogicService.addDice()
                DrawService.BackgroundService.changeShapeColors(LogicService.getSelectedDice(), d)

        if event.type == pg.KEYDOWN:
            match event.key:
                case pg.K_SPACE:
                    # DrawService.BackgroundService.changeDirection()
                    AnimateService.shakeDice(playerDice)
                    SoundService.diceRollSound(LogicService.rollsLeft)
                    LogicService.rollDice()
                #Scoring a hand
                case pg.K_q:
                    AnimateService.shakeDice(playerDice, selected=True)
                    recentHandScore = LogicService.score()
                    SoundService.hitSound(recentHandScore)
                case pg.K_ESCAPE:
                    going = False

    DrawService.resetFrame()
    #returns list of (die, rect) for EventService
    diceAndRect = DrawService.drawDice(playerDice)

    EventService.dieHovered(diceAndRect)

    LogicService.findHand()

    DrawService.drawTextContent(LogicService)

    
    fps = int(clock.get_fps())
    DrawService.drawText(1, f"fps {fps}", WIDTH / 8 * 7, 5)
    pg.display.update()
    clock.tick(60)

##Old code to change background color
                #left and right arrow keys change background color
                # case pg.K_LEFT:
                #     BACKGROUND_COLOR_RANGE -= 15
                #     if BACKGROUND_COLOR_RANGE < 5:
                #         BACKGROUND_COLOR_RANGE = 5
                #     else:
                #         DrawService.setBackgroundColors(BACKGROUND_COLOR_RANGE, LogicService.   getSelectedDice())
                #         LogicService.unselectAll()
                # case pg.K_RIGHT:
                #     BACKGROUND_COLOR_RANGE += 15
                #     if BACKGROUND_COLOR_RANGE > 250:
                #         BACKGROUND_COLOR_RANGE = 250
                #     else:
                #         DrawService.setBackgroundColors(BACKGROUND_COLOR_RANGE,LogicService.getSelectedDice())
                #         LogicService.unselectAll()