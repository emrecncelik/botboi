module.exports = {
    name: 'purge',
    aliases: ['delete'],
    description: 'Delete up to 99 messages.',
    args: true,
    usage: '<number>',
    execute(message, args) {
            const amount = parseInt(args[0]) + 1;

            if (isNaN(amount)) {
                return message.reply('That\'s not a valid argument (ex. !purge 10)');
            }
            else if (amount <= 1 || amount > 100) {
                return message.reply('You can delete minimum 1, maximum 99 messages.');
            }
            message.channel.bulkDelete(amount);
            message.reply(`deleted ${amount - 1} messages.`);
    }
};
