// OFFLINE version of MAILBOX object for TRIK
// author: Alexey Klyachin, 2020, robonest.ru

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
	hasMessages: function(){ return script.readAll(this.myFile).length > 0 },

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
				script.wait(20);
			})
	}
}
