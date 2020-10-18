""" 
	OFFLINE version of MAILBOX object for TRIK
	author: Alexey Klyachin, 2020, robonest.ru
"""

import os
import json

class Mailboxes:
  def __init__(self, robotNumber = 1, robotHulls = [1, 2, 3]):
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
