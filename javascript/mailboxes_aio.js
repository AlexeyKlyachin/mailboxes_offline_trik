// OFFLINE version of MAILBOX object for TRIK
// Author: Alexey Klyachin, 2020, robonest.ru

mailboxes = {
	storagePath: 'c:/temp/mailboxes/',	// путь для хранения файлов ("почтовых ящиков") для каждого робота из списка robotHulls
	fileExt: '.txt',
	myFile: '',
	
	init: function(){
		this.myFile = this.storagePath + robotNumber + this.fileExt
		
		for (var r in robotHulls)
			this.clearFile(this.storagePath + robotHulls[r] + this.fileExt)
	},
	
	writeFile:	function(file, msg){ script.writeToFile(file, msg) },
	clearFile:	function(file){ script.removeFile(file);  this.writeFile(file,'') },
	readFile:	function(file){ var data = script.readAll(file); this.clearFile(file); if (data.length > 0) return JSON.parse(data); return data; },
	myHullNumber:	function(){ return robotNumber },
	hasMessages:    function(){ script.readAll(this.myFile).length > 0 },

	receive: function(){ 
		while (!mailboxes.hasMessages())
			script.wait(100);
		var data = mailboxes.readFile(this.myFile); 
		return data 
	},
	
	send: function(robots, msg){  					// только 2 параметра - для совместимости формата с основным объектом mailbox
                if (robots == undefined) throw ('[Объект mailboxes: Не указаны параметры для отправки сообщения]')

		if (msg == undefined){					// указан только первый параметр => сообщение уходит всем роботам
			msg = robots
			robots = robotHulls
		}

        	if (robots.length == 0)					// указан пустой массив => сообщение уходит всем роботам
			robots = robotHulls

		if (typeof robots == 'number') robots = [robots]        // указан номер только одного робота
	
		robots.forEach(function (n) {
				mailboxes.writeFile(mailboxes.storagePath + n + mailboxes.fileExt, JSON.stringify(msg)+'\n')
				wait(20);
			})
	}
}

robotHulls = [1, 20, 44]		// номера 'бортов' роботов, участвующих в 'общении'
robotNumber = 1				// номер ТЕКУЩЕГО робота, если работает в оффлайн

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