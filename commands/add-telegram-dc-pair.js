const spawn = require('child_process').spawn;


module.exports = {
	name:'add-telegram-dc-pair',
	aliases:'add-pair',
	description:'Creates link between discord and telegram wit given identifications.',
	args:true,
	usage: '<telegram-id> <dc-id>',

	async execute(message,args) {
			const user_id = message.author.id;
			const function_name = 'add_discord_telegram_pair';

			const childProcess = spawn('python3',['./telegram-script/botboi_bot.py',function_name,args[0],args[1],user_id]);

			childProcess.stdout.on('data', (data) => {
					message.reply(data.toString());
			});

			childProcess.stderr.on('data', function(data) {
				console.log(data.toString());
		});
	}
}