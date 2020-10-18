""" 
	OFFLINE version of MAILBOX object for TRIK
	author: Alexey Klyachin, 2020, robonest.ru
"""
import os
import json

class Mailboxes:
  def __init__(self, robotNumber = 1, robotHulls = [1, 2]):
    self.storagePath = 'c:/temp/mailboxes/'
    self.fileExt = '.txt'
    self.robotNumber = robotNumber
    self.robotHulls = robotHulls
    self.myFile = self.makeFileName(self.robotNumber)
    
    if not os.path.exists(self.storagePath):
      os.mkdir(self.storagePath)

    [self.clearFile(self.makeFileName(robot)) for robot in self.robotHulls]

  def makeFileName(self, robot_number):
    return self.storagePath + str(robot_number) + self.fileExt
    
  def writeFile(self, file, msg = ''):
    with open(file, mode='a') as f:
      f.write(msg + '\n')

  def clearFile(self, file):
    with open(file, mode='w', encoding='utf-8') as f:
      f.write('')
  
  def readFile(self, file):
    with open(file) as f:
      data = [json.loads(line.strip()) for line in f.readlines()]
    self.clearFile(file)
    return data                           # [список] из N элементов, каждый элемент - строка файла
  
  def myHullNumber(self):
    return self.robotNumber

  def receive(self):
    while not mailboxes.hasMessages():
      script.wait(50)
    return self.readFile(self.myFile)

  def hasMessages(self):
    return os.path.getsize(self.myFile) > 0
  
  def send(self, robots = [], msg = None):
    if robots is None:
      raise ('[Объект mailboxes: Не указаны параметры для отправки сообщения]')

    if msg is None:                         # если указан только первый параметр, то принимаем его за сообщение и отправляем всем роботам
      msg = robots
      robots = self.robotHulls				      # сообщение для всех роботов

    if type(robots) is list and len(robots) == 0:    # указан пустой массив -> сообщение уходит всем роботам
      robots = self.robotHulls

    if type(robots) is int:
      robots = [robots]	                    # если указан номер только одного робота -> переводим его в [список]

    for robot in robots:
      self.writeFile(self.makeFileName(robot), json.dumps(msg))


def move2cells():
    brick.encoder('E3').reset()
    goal = (35 / (3.14159 * 5.6)) * 360
    brick.motor('M4').setPower(80)
    brick.motor('M3').setPower(80)
    while brick.encoder('E3').read() < goal:
        wait(30)
    brick.motor('M4').setPower(0)
    brick.motor('M3').setPower(0)		  
      
      
robotHulls = [1, 10, 20]	        # номера 'бортов' роботов, участвующих в 'общении'
robotNumber = 1				            # номер ТЕКУЩЕГО робота, если работает в оффлайн

mailboxes = Mailboxes(robotNumber, robotHulls)
    
wait = script.wait

brick.display().addLabel('my number: '+ str(mailboxes.myHullNumber()), 10, 10)
brick.display().redraw()

if robotNumber == 1:
  while not brick.keys().wasPressed(KeysEnum.Up):
    script.wait(100)
  mailboxes.send(10, 'message to second robot')

mailboxes.receive()							                # ждем первое сообщение
move2cells()								                    # едем 2 клетки
wait(1000)

if mailboxes.myHullNumber() == 10:
    mailboxes.send(20, 'message to third robot')

if mailboxes.myHullNumber() == 20:
    mailboxes.send(1, 'message to first robot')

wait(2000)

if mailboxes.myHullNumber() == 1:
    mailboxes.send('message to all robots')				    # отправляем сообщение всем роботам

msg = mailboxes.receive()						            # ждем второе сообщение					
move2cells()

