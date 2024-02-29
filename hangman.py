
import pygame
import sys
import random
from time import sleep
from pygame.locals import *
from timeit import default_timer as timer

fps = 30
pygame.init()
width = 800
height = 600

bg=pygame.image.load("bg1.png")

black = (0,0,0)
white = (255,255,255)
lightred = (255, 165, 145)
darklightred = (255, 97, 81)
lightblue = (126,178,255)
darklightblue = (42, 129, 255)
lightgrey = (192, 192, 192)
cyan = (0, 255, 255)
lightgreen = (0, 255, 0)
green = (26,200,43)

textBoxSpace = 5
textBoxNumber = 0

bgm=pygame.mixer.music.load("bgm.mp3")
pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.play(-1)

pencil1=pygame.mixer.Sound("pencil1.mp3")
pencil2=pygame.mixer.Sound("pencil2.mp3")
pencil3=pygame.mixer.Sound("pencil3.mp3")
pencil4=pygame.mixer.Sound("pencil4.mp3")
pencil5=pygame.mixer.Sound("pencil5.mp3")
pencil6=pygame.mixer.Sound("pencil6.mp3")
pencil1.set_volume(0.7)
pencil2.set_volume(0.7)
pencil3.set_volume(0.7)
pencil_sound=[pencil1,pencil2,pencil3,pencil6]

win_sound=pygame.mixer.Sound("win.mp3")
lose_sound=pygame.mixer.Sound("lose.wav")
select_sound=pygame.mixer.Sound("select2.mp3")
back_sound=pygame.mixer.Sound("select.mp3")

letter_keys=[pygame.K_a,pygame.K_b,pygame.K_c,pygame.K_d,pygame.K_e,pygame.K_f,pygame.K_g,pygame.K_h,pygame.K_i,pygame.K_j,pygame.K_k,pygame.K_l,pygame.K_m,pygame.K_n,pygame.K_o,pygame.K_p,pygame.K_q,pygame.K_r,pygame.K_s,pygame.K_t,pygame.K_u,pygame.K_v,pygame.K_w,pygame.K_x,pygame.K_y,pygame.K_z]
letters='abcdefghijklmnopqrstuvwxyz'

def button(word,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen,ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen,ic,(x,y,w,h))

    buttonText = pygame.font.Font(None,20)
    buttonTextSurf = buttonText.render(word, True, white)
    buttonTextRect = buttonTextSurf.get_rect()
    buttonTextRect.center = ((x+(w/2)), (y+(h/2)))
    screen.blit(buttonTextSurf, buttonTextRect)

def endGame(result=0):
    global textBoxSpace, textBoxNumber, end, start
    end = timer()
    timeTaken = (end - start)
    textBoxSpace = 5
    textBoxNumber = 0
    resultMessage="You lost..!"
    messageColor=darklightred

    pygame.mixer.music.pause()
    if result==1:
        resultMessage="You won!"
        messageColor=green
    message = "Time taken: " + str(round(timeTaken)) + "s"
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        button("Yes",(width/2)-50,420,100,50,darklightred,lightred,quitGame)
        button("No",(width/2)-50,500,100,50,darklightblue,lightblue,hangman)

        largeText = pygame.font.SysFont("comicsansms",90)
        textSurf1 = largeText.render("End Game?",True,messageColor)
        textRect1 = textSurf1.get_rect()
        textRect1.center = (width / 2, height / 2)
        screen.blit(textSurf1, textRect1)

        textSurf2 = largeText.render(resultMessage,True,messageColor)
        textRect2 = textSurf2.get_rect()
        textRect2.center = (width/2,200)
        screen.blit(textSurf2, textRect2)

        textSurf3 = largeText.render(message,True,messageColor)
        textRect3 = textSurf3.get_rect()
        textRect3.center = (width/2,100)
        screen.blit(textSurf3, textRect3)

        pygame.display.update()
        clock.tick(fps)

def quitGame():
    pygame.quit()
    sys.exit()

def unpause():
    global pause
    pause = False

def pause():
    largeText = pygame.font.SysFont("chauser",115)
    TextSurf = largeText.render("Paused",True,black)
    TextRect = TextSurf.get_rect()
    TextRect.center = (width / 2, height / 2)
    screen.blit(TextSurf, TextRect)

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(white)


        button("Continue",150,450,100,50,darklightred,lightred,unpause)
        button("Quit",550,450,100,50,darklightblue,lightblue,quitGame)

        pygame.display.update()
        clock.tick(fps)

def textObjects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def main():
    global clock, screen, play
    play = True
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Hangman!")

    while True:
        hangman()

def placeLetter(letter):
    global pick, pickSplit
    space = 10
    wordSpace = 0
    while wordSpace < len(pick):
        text = pygame.font.Font('freesansbold.ttf',40)
        if letter in pickSplit[wordSpace]:
            textSurf = text.render(letter,True,black)
            textRect = textSurf.get_rect()
            textRect.center = (((150)+space),(200))
            screen.blit(textSurf, textRect)
        wordSpace += 1
        space += 60

    pygame.display.update()
    clock.tick(fps)

def textBoxLetter(letter):
    global textBoxSpace, textBoxNumber
    if textBoxNumber <= 5:
        text = pygame.font.Font(None,40)
        textSurf = text.render(letter,True,black)
        textRect = textSurf.get_rect()
        textRect.center = (((105)+textBoxSpace),(350))
        screen.blit(textSurf, textRect)

    elif textBoxNumber <= 10:
        text = pygame.font.Font(None,40)
        textSurf = text.render(letter,True,black)
        textRect = textSurf.get_rect()
        textRect.center = (((105)+textBoxSpace),(400))
        screen.blit(textSurf, textRect)

    elif textBoxNumber <= 15:
        text = pygame.font.Font(None,40)
        textSurf = text.render(letter,True,black)
        textRect = textSurf.get_rect()
        textRect.center = (((105)+textBoxSpace),(450))
        screen.blit(textSurf, textRect)

    elif textBoxNumber <= 20:
        text = pygame.font.Font(None,40)
        textSurf = text.render(letter,True,black)
        textRect = textSurf.get_rect()
        textRect.center = (((105)+textBoxSpace),(500))
        screen.blit(textSurf, textRect)

    pygame.display.update()
    clock.tick(fps)

def back():
    back_sound.play()
    hangman()

def hangman():
    global textBoxSpace, textBoxNumber
    textBoxSpace = 5
    textBoxNumber = 0
    pygame.mixer.music.pause()
    while play == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(bg,(0,0))
        space = 10
        textBoxSpace = 5

        text = pygame.font.Font(None,50)
        textSurf = text.render("Choose a category",True,black)
        textRect = textSurf.get_rect()
        textRect.center = ((width/2),(height/2))
        screen.blit(textSurf, textRect)

        button("Animals",150,350,150,120,black,lightgrey,Animals)
        button("Vehicles",500,350,150,120,black,lightgrey,Vehicles)
        button("Food",150,100,150,120,black,lightgrey,Foods)
        button("Sports",500,100,150,120,black,lightgrey,Sports)

        pygame.display.update()
        clock.tick(fps)

def hangmanGame(category,title):
    global pause, pick, pickSplit, textBoxSpace, textBoxNumber, start
    start = timer()
    chances = 20
    pick = random.choice(category)
    pickSplit = [pick[i:i+1] for i in range(0, len(pick), 1)]

    select_sound.play()
    pygame.mixer.music.unpause()
    screen.blit(bg,(0,0))

    wordSpace = 0
    space = 10
    while wordSpace < len(pick):
        text = pygame.font.Font(None,50)
        textSurf1 = text.render("_",True,black)
        textRect1 = textSurf1.get_rect()
        textRect1.center = (((150)+space),(200))
        screen.blit(textSurf1, textRect1)
        space = space + 60
        wordSpace += 1

    guesses = ''
    while True:
        guess = ''

        if textBoxNumber == 5:
            textBoxSpace = 5
        if textBoxNumber == 10:
            textBoxSpace = 5
        if textBoxNumber == 15:
            textBoxSpace = 5

        pygame.draw.rect(screen, lightgreen, [610,40,150,20])
        text = pygame.font.Font(None,30)
        textSurf = text.render(("Chances: %s" % chances),False,black)
        textRect = textSurf.get_rect()
        textRect.topright = (750,40)
        screen.blit(textSurf, textRect)

        textTitle = pygame.font.Font(None,40)
        textTitleSurf = textTitle.render(title,True,black)
        textTitleRect = textTitleSurf.get_rect()
        textTitleRect.center = ((width/2),50)
        screen.blit(textTitleSurf, textTitleRect)

        pygame.draw.rect(screen, black, [100,300,250,250],2)

        if chances == 19:
            pygame.draw.rect(screen,black,[450,550,100,10])
        elif chances == 18:
            pygame.draw.rect(screen,black,[550,550,100,10])
        elif chances == 17:
            pygame.draw.rect(screen,black,[650,550,100,10])
        elif chances == 16:
            pygame.draw.rect(screen,black,[500,450,10,100])
        elif chances == 15:
            pygame.draw.rect(screen,black,[500,350,10,100])
        elif chances == 14:
            pygame.draw.rect(screen,black,[500,250,10,100])
        elif chances == 13:
            pygame.draw.rect(screen,black,[500,250,150,10])
        elif chances == 12:
            pygame.draw.rect(screen,black,[600,250,100,10])
        elif chances == 11:
            pygame.draw.rect(screen,black,[600,250,10,50])
        elif chances == 10:
            pygame.draw.line(screen,black,[505,505],[550,550],10)
        elif chances == 9:
            pygame.draw.line(screen,black,[550,250],[505,295],10)
        elif chances == 8:
            pygame.draw.line(screen,black,[505,505],[460,550],10)
        elif chances == 7:
            pygame.draw.circle(screen,black,[605,325],30)
        elif chances == 6:
            pygame.draw.rect(screen,black,[600,350,10,60])
        elif chances == 5:
            pygame.draw.rect(screen,black,[600,410,10,60])
        elif chances == 4:
            pygame.draw.line(screen,black,[605,375],[550,395],10)
        elif chances == 3:
            pygame.draw.line(screen,black,[605,375],[650,395],10)
        elif chances == 2:
            pygame.draw.line(screen,black,[605,465],[550,485],10)
        elif chances == 1:
            pygame.draw.line(screen,black,[605,465],[650,485],10)

        button("Back",50,50,100,50,black,lightgrey,back)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                failed = 0

                if event.key == pygame.K_SPACE:
                    pause()

                if event.key == pygame.K_ESCAPE:
                    play = False

                for i in range(26):
                    if event.key==letter_keys[i]:
                        random.choice(pencil_sound).play()
                        guess = guess + letters[i]
                        guesses += guess
                        for char in pick:
                            if char in guesses:
                                pass
                            else:
                                failed += 1

                        if guess in pick:
                            placeLetter(letters[i])

                        if failed == 0:
                            win_sound.play()
                            endGame(1)

                        if guess not in pick:
                            textBoxSpace += 40
                            textBoxNumber += 1
                            chances = chances - 1
                            textBoxLetter(letters[i])

                        if chances == 0:
                            lose_sound.play()
                            endGame()

        pygame.display.update()
        clock.tick(fps)

def Animals():
    animal = ['cow','dog','cat','pig','zebra','bird','giraffe','lion','tiger','penguin','hamster','fox','panda','bear','cheetah','ostrich','meerkat','whale','shark','horse','monkey','octopus','kitten','kangaroo','chicken','fish','rabbit','sheep']
    title = "Animals"
    hangmanGame(animal,title)

def Vehicles():
    vehicle = ['car','bus','train','airplane','plane','ship','jet','boat','lorry','tractor','bike','motorbike','tram','van','ambulance','fire engine','rocket','taxi','caravan','coach','lorry','scooter','sleigh','tank','wagon','spaceship']
    title = "Vehicles"
    hangmanGame(vehicle,title)

def Foods():
    food = ['apple','banana','orange','peach','pizza','donut','chips','sandwich','cookie','cucumber','carrot','sweetcorn','ice cream','pancake','bread','potato','tomato','nuts','yogurt','pasta','rice','cheese','soup','fish','egg','meat','ham','sausage']
    title = "Foods"
    hangmanGame(food,title)

def Sports():
    sport = ['rugby','football','netball','basketball','swimming','hockey','curling','running','golf','tennis','badmington','archery','volleyball','bowling','dancing','gym','skating','baseball','rounders','boxing','climbing','canoe','cycling','fencing','karate','shooting','cricket']
    title = "Sports"
    hangmanGame(sport,title)

if __name__ == '__main__':
    main()
