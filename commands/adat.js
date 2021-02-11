const spawn = require('child_process').spawn;

module.exports = {
	name:'adat',
	aliases:['5adat'],
	description:'Send message on telegram to mentioned person',
	args:true,
	usage:'<tag person>',


	async execute(message,args){
		const mentioned_id = message.mentions.users.first().id;
		const user_id = message.author.id;
		const mentioned_name = message.mentions.users.first().username;
		const function_name = 'call_for_5_adat'

		const childProcess = spawn('python3',['./telegram-script/botboi_bot.py',function_name,mentioned_id,mentioned_name,user_id]);
		childProcess.stdout.on('data', data => {
			message.reply(data.toString());
		})
	

		childProcess.stderr.on('data', function(data) {
			console.log(data.toString());
		});

	}
}

