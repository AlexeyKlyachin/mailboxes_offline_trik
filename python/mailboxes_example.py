""" 
	OFFLINE version of MAILBOX object for TRIK
	author: Alexey Klyachin, 2020, robonest.ru
"""

import mailboxes_offline

def move2cells():
    brick.encoder(E3).reset()
    goal = 35 / (3.14159 * 5.6) * 360
    brick.motor(M4).setPower(80)
    brick.motor(M3).setPower(80)
    while brick.encoder(E3).read() < goal:
        wait(30)
    brick.motor(M4).setPower(0)
    brick.motor(M3).setPower(0)		  


robotHulls = [1, 10, 20]	      # номера 'бортов' роботов, участвующих в 'общении'
robotNumber = 1				          # номер ТЕКУЩЕГО робота, если работает в оффлайн

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

