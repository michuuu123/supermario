
import sys
import xml.etree.ElementTree as ET
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from gui import Ui_MainWindow
import random


class Game(QMainWindow):
    WIDTH = 420
    HEIGHT = 220
    SPEED = 10
    def __init__(self):
        super(Game, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.start()
        self.ui.startBtn.clicked.connect(self.start)
        self.ui.endBtn.clicked.connect(self.pause)
        self.ui.saveBtn.clicked.connect(self.save)
        self.ui.loadBtn.clicked.connect(self.load)
        self.ui.watchBtn.clicked.connect(self.filmON)
        self.ui.recordBtn.clicked.connect(self.record)

    def start(self):  # generate map
        self.ui.endBtn.blockSignals(False)
        self.ui.recordBtn.blockSignals(False)
        self.ui.watchBtn.blockSignals(False)
        self.ui.saveBtn.blockSignals(False)
        self.ui.loadBtn.blockSignals(False)
        self.paused = False
        self.state = 0
        self.watchingFilm = False
        self.filmSaving = False
        self.dataFilm = ET.Element('data')
        self.scene = QGraphicsScene(20, 20, Game.WIDTH, Game.HEIGHT)
        self.film = False
        self.ui.graphicsView.setFixedSize(Game.WIDTH + 10, Game.HEIGHT + 10)
        self.ui.graphicsView.setScene(self.scene)
        self.mario = QGraphicsPixmapItem(QPixmap("mario.png"))
        self.mario.setScale(0.15)
        self.mario.setPos(20, Game.HEIGHT - 20)
        self.marioPos = (20, Game.HEIGHT - 20)
        self.scene.addItem(self.mario)
        self.score = 0
        self.enemySteps = 100

        self.grounds = []
        self.coins = []
        for i in range(20):
            r = Game.HEIGHT - random.randint(90, 110)
            self.coin = QGraphicsPixmapItem(QPixmap("coin.png"))
            self.coin.setPos(120 + 120 * i, r)
            self.coin.setScale(0.1)
            self.coins.append(self.coin)
            self.scene.addItem(self.coin)

            self.ground = QGraphicsPixmapItem(QPixmap("ground.jpg"))
            self.ground.setPos(120 + 120 * i - 5, r + 25)
            self.ground.setScale(0.15)
            self.grounds.append(self.ground)
            self.scene.addItem(self.ground)

        self.clouds = []
        for i in range(50):
            cloud = QGraphicsPixmapItem(QPixmap("cloud.png"))
            cloud.setPos(120 + 120 * i, 30)
            cloud.setScale(0.15)
            self.clouds.append(cloud)
            self.scene.addItem(cloud)

        self.turtles = []
        for i in range(10):
            turtle = QGraphicsPixmapItem(QPixmap("turtle.png"))
            turtle.setPos(120 + 350 * i, Game.HEIGHT - 30)
            turtle.setScale(0.5)
            self.turtles.append(turtle)
            self.scene.addItem(turtle)

        self.timer = QBasicTimer()
        self.timer.start(Game.SPEED, self)
        self.up = False
        self.jump = False
        self.down = False
        self.direction = -1
        self.jumpSteps = 0
        self.bg = QBrush(QPixmap("tlo1.jpg"))
        trans = QTransform()
        trans.scale(0.4, 0.47)
        self.bg.setTransform(trans)
        self.scene.setBackgroundBrush(self.bg)
        self.setFocusPolicy(Qt.StrongFocus)

    def pause(self):
        if self.paused is False:
            self.paused = True
            self.ui.endBtn.setText("Start")
            self.timer.stop()
        else:
            self.paused = False
            self.ui.endBtn.setText("Pause")
            self.timer.start(Game.SPEED, self)

    def stop(self):
        self.timer.stop()
        self.ui.endBtn.blockSignals(True)

    def record(self):
        if self.ui.recordBtn.text() == 'Record':
            self.ui.recordBtn.setText('Stop Recording')
            self.film = True
            self.filmSaving = False
            self.dataFilm = ET.Element('data')

        else:
            self.ui.recordBtn.setText('Record')
            self.endRecording()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Left:
            self.direction = 2

        elif key == Qt.Key_Right:
            self.direction = 1

        elif key == Qt.Key_Up:
            self.up = True

    def showState(self,root): #loading one state from film.xml

        self.score = int(root.find('score').text)
        mario = root.find("mario")
        x = mario.find('x').text
        y = mario.find('y').text
        self.marioPos = (int(x), int(y))
        self.mario.setPos(self.marioPos[0], self.marioPos[1])

        self.loadingElements(root, 'ground', self.grounds)
        self.loadingElements(root, 'cloud', self.clouds)

        self.coins = self.loadingDynamicElements(root, 'coin', self.coins, 0.1)
        self.turtles = self.loadingDynamicElements(root, 'turtle', self.turtles, 0.5)

    def filmON(self):    # begin saving states in film.xml
        tree = ET.parse('film.xml')
        root = tree.getroot()
        self.states = root.findall('state')
        self.watchingFilm = True

    def endRecording(self):
        if self.film is True:
            mydata = ET.tostring(self.dataFilm)
            mydata = str(mydata)
            mydata = mydata[2:-1]
            myfile = open("film.xml", "w")
            myfile.write(mydata)
            self.film = False
            self.filmSaving = True

    def fly(self): # actions when mario dosent touch the ground
        if self.up is True and self.down is False and self.jump is False:
            self.jump = True
            self.jumpSteps = 100

        if self.down is True:
            self.fall()

        if self.jump is True:
            self.goingUp()

    def goingUp(self): # mario goes up
        self.jumpSteps -= 1
        self.marioPos = (self.marioPos[0], self.marioPos[1] - 1)
        self.mario.setPos(self.marioPos[0], self.marioPos[1])

        if self.checkGround() is True:
            self.jump = False
            self.down = True
            self.jumpSteps = 0
            self.marioPos = (self.marioPos[0], self.marioPos[1] + 1)
            self.mario.setPos(self.marioPos[0], self.marioPos[1])

        if self.jumpSteps == 0:
            self.jump = False
            self.down = True

    def fall(self): # mario fall down
        self.marioPos = (self.marioPos[0], self.marioPos[1] + 1)
        self.mario.setPos(self.marioPos[0], self.marioPos[1])

        if self.checkGround() is True:
            self.marioPos = (self.marioPos[0], self.marioPos[1] - 1)
            self.mario.setPos(self.marioPos[0], self.marioPos[1])
            if self.up is True:
                self.down = False

        self.killEnemy()

        if self.marioPos[1] == Game.HEIGHT - 20:
            self.down = False

    def savingElements(self,name,elements, data): #save list of elements in xml file
        items = ET.SubElement(data, name+'s')

        for i in elements:
            pos = i.pos()
            it = ET.SubElement(items, name)

            it.text = str(pos)

    def loadingElements(self,root,name,elements): #load list of elements from xml file
        tmp = root.find(name + 's')
        i = 0
        for element in tmp.findall(name):
            cos = element.text
            cos = cos.split('PyQt5.QtCore.QPointF(')
            cos = cos[1].split(',')
            x = cos[0]
            y = cos[1]
            y = y[:-1]

            elements[i].setPos(float(x), float(y))
            i += 1

    def save(self):  # make save in save.xml
        data = ET.Element('data')
        items = ET.SubElement(data, 'mario')
        item1 = ET.SubElement(items, 'x')
        item2 = ET.SubElement(items, 'y')

        item1.text = str(self.marioPos[0])
        item2.text = str(self.marioPos[1])

        score = ET.SubElement(data, 'score')
        score.text = str(self.score)


        self.savingElements('ground',self.grounds,data)
        self.savingElements('coin', self.coins, data)
        self.savingElements('turtle', self.turtles, data)
        self.savingElements('cloud',self.clouds,data)

        # create a new XML file with the results
        mydata = ET.tostring(data)
        mydata = str(mydata)
        mydata = mydata[2:-1]
        myfile = open("save.xml", "w")
        myfile.write(mydata)

    def load(self): # load save from save.xml
        tree = ET.parse('save.xml')
        root = tree.getroot()
        self.score = int(root.find('score').text)
        mario = root.find("mario")
        self.down = True

        x = mario.find('x').text
        y = mario.find('y').text


        if int(y) == Game.HEIGHT - 20:
            self.down = False
        self.marioPos = (int(x), int(y))
        if self.mario.isVisible() == False:
            self.mario.show()
            self.ui.endBtn.blockSignals(False)
            self.timer.start(Game.SPEED, self)

        self.mario.setPos(self.marioPos[0], self.marioPos[1])


        self.loadingElements(root,'ground',self.grounds)
        self.loadingElements(root, 'cloud', self.clouds)

        self.coins = self.loadingDynamicElements(root,'coin',self.coins,0.1)
        self.turtles = self.loadingDynamicElements(root,'turtle',self.turtles,0.5)

    def loadingDynamicElements(self,root,name,elements,scale): # loading from xml list of elements, which changes their number during the game
        for i in elements:
            i.hide()
        elements = []
        tmp = root.find(name+'s')
        i = 0
        for element in tmp.findall(name):
            cos = element.text
            cos = cos.split('PyQt5.QtCore.QPointF(')
            cos = cos[1].split(',')
            x = cos[0]
            y = cos[1]
            y = y[:-1]

            item = QGraphicsPixmapItem(QPixmap(name + ".png"))
            item.setScale(scale)
            elements.append(item)
            self.scene.addItem(item)
            elements[i].setPos(float(x), float(y))
            i += 1
        return elements

    def checkGround(self): # check if mario touch the ground
        test = False
        for i in self.grounds:
            if self.mario.collidesWithItem(i) is True:
                test = True
        return test

    def keyReleaseEvent(self, event):
        key = event.key()
        if key == Qt.Key_Left:
            self.direction = -1
        elif key == Qt.Key_Right:
            self.direction = -1
        elif key == Qt.Key_Up:
            self.up = False

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.fly()
            self.moveMario()
            self.takeCoin()
            self.drawScore()
            self.moveEnemy()
            self.killMario()
            if self.film is True and self.filmSaving is False:
                self.saveState()
            if self.watchingFilm is True:
                if self.state < len(self.states):
                    self.showState(self.states[self.state])
                    self.state +=1
                else:
                    self.watchingFilm = False
                    self.state = 0
                    self.down = True
                    if self.marioPos[1] == Game.HEIGHT - 20:
                        self.down = False
            self.scene.update()

    def saveState(self): # save state in film.xml
        data = ET.SubElement(self.dataFilm, 'state')
        items = ET.SubElement(data, 'mario')
        item1 = ET.SubElement(items, 'x')
        item2 = ET.SubElement(items, 'y')
        score = ET.SubElement(data, 'score')
        score.text = str(self.score)

        item1.text = str(self.marioPos[0])
        item2.text = str(self.marioPos[1])

        self.savingElements('ground', self.grounds, data)
        self.savingElements('coin', self.coins, data)
        self.savingElements('turtle', self.turtles, data)
        self.savingElements('cloud', self.clouds, data)

    def goRight(self):
        if self.marioPos[0]<Game.WIDTH/2:
            self.marioPos = (self.marioPos[0] + 1, self.marioPos[1])
            self.mario.setPos(self.marioPos[0], self.marioPos[1])
            if self.checkGround() is True:
                self.marioPos = (self.marioPos[0] - 1, self.marioPos[1])
                self.mario.setPos(self.marioPos[0], self.marioPos[1])

        else:
            self.marioPos = (self.marioPos[0] + 1, self.marioPos[1])
            self.mario.setPos(self.marioPos[0], self.marioPos[1])
            if self.checkGround() is True:
                self.marioPos = (self.marioPos[0] - 1, self.marioPos[1])
                self.mario.setPos(self.marioPos[0], self.marioPos[1])
            else:
                self.marioPos = (self.marioPos[0] - 1, self.marioPos[1])
                self.mario.setPos(self.marioPos[0], self.marioPos[1])
                self.moveEnviroment()

    def goLeft(self):
        if self.marioPos[0]>20:
            self.marioPos = (self.marioPos[0] - 1, self.marioPos[1])
            self.mario.setPos(self.marioPos[0], self.marioPos[1])
            for i in self.grounds:
                if self.mario.collidesWithItem(i) is True:
                    self.marioPos = (self.marioPos[0] + 1, self.marioPos[1])
                    self.mario.setPos(self.marioPos[0], self.marioPos[1])

    def killEnemy(self):
        for i in self.turtles:
            if self.mario.collidesWithItem(i) is True:
                enemy = i
                enemy.hide()
                self.turtles.remove(enemy)

    def killMario(self):
        if self.checkEnemy() is True:
            self.mario.hide()
            self.stop()

    def moveMario(self):
        if self.direction == 1:
            self.goRight()
        if self.direction == 2:
            self.goLeft()

    def takeCoin(self):
        for i in self.coins:
            if self.mario.collidesWithItem(i) is True:
                self.coins.remove(i)
                i.hide()
                self.score+=1

    def moveEnemy(self):
        if self.enemySteps<-100:
            self.enemySteps = 100
        self.enemySteps -=1
        for i in self.turtles:
            posC = i.pos()
            if self.enemySteps >0:
                offset = QPointF(1, 0)
            else:
                offset = QPointF(-1, 0)
            i.setPos(posC + offset)

    def moveEnviroment(self):
        self.moveByOneStep(self.coins)
        self.moveByOneStep(self.clouds)
        self.moveByOneStep(self.grounds)
        self.moveByOneStep(self.turtles)

    def moveByOneStep(self, elements):
        for i in elements:
            posC = i.pos()
            offset = QPointF(1,0)
            i.setPos(posC-offset)

    def drawScore(self):
        self.ui.scoreBox.setText(str(self.score))

    def checkEnemy(self): #check if enemy kills mario
        end = False
        for i in self.turtles:
            if self.mario.collidesWithItem(i) is True:
                end = True
        return end

app = QtWidgets.QApplication([])

application = Game()

application.show()
sys.exit(app.exec())