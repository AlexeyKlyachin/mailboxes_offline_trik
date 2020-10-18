// OFFLINE version of MAILBOX object for TRIK
// author: Alexey Klyachin, 2020, robonest.ru

robotHulls = [1, 20, 44]		// номера 'бортов' роботов, участвующих в 'общении'
robotNumber = 1				// номер ТЕКУЩЕГО робота, если работает в оффлайн
include('c:/mailboxes.js')

mailboxes.init()				// создаем имя файла для текущего робота и создаем/очищаем файлы для остальных роботов

wait = script.wait

brick.display().addLabel('my  number: '+ mailboxes.myHullNumber(), 10, 10)
brick.display().redraw()

if (robotNumber == 1){
	while (!brick.keys().wasPressed(KeysEnum.Up)) { script.wait(100)}
	mailboxes.send(20, 'message to second robot')
}

mailboxes.receive()							// ждем первое сообщение
move2cells()								// едем 2 клетки
wait(1000)

if (mailboxes.myHullNumber() == 20){
	mailboxes.send(44,'message to third robot')
}

if (mailboxes.myHullNumber() == 44){
	mailboxes.send(1,'message to first robot')
}

wait(2000)

if (mailboxes.myHullNumber() == 1)
	mailboxes.send('message to all robots')		// отправляем сообщение всем роботам

msg = mailboxes.receive()						// ждем второе сообщение					
move2cells()

	
function move2cells(){
	brick.encoder(E3).reset()
	var goal = (35 / (Math.PI * 5.6)) * 360
	brick.motor(M4).setPower(80)
	brick.motor(M3).setPower(80)
	while (brick.encoder(E3).read() < goal) wait(30)
	brick.motor(M4).setPower(0)
	brick.motor(M3).setPower(0)		
}