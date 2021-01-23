const fetch = require('node-fetch');

module.exports = {
    name: 'gif',
    description: 'Get a gif from tenor with given search query.',
    args: true,
    usage: '<search query>',
    async execute(message, args) {
        let keywords = args.join(' ');
        keywords = keywords.turkishtoEnglish();
        try {
            const url = `https://api.tenor.com/v1/search?q=${keywords}&key=${process.env.TENORKEY}&limit=10`;
            const response = await fetch(url);
            const json = await response.json();
            const results = json.results;
            const index = Math.floor(Math.random() * results.length);
            message.channel.send(results[index].url);
        }
        catch (error) {
            message.channel.send('There are no results for this search query.');
        }
    },
};

// convert search query from Turkish chars to English chars
String.prototype.turkishtoEnglish = function() {
    return this.replace('Ğ', 'g')
        .replace('Ü', 'u')
        .replace('Ş', 's')
        .replace('I', 'i')
        .replace('İ', 'i')
        .replace('Ö', 'o')
        .replace('Ç', 'c')
        .replace('ğ', 'g')
        .replace('ü', 'u')
        .replace('ş', 's')
        .replace('ı', 'i')
        .replace('ö', 'o')
        .replace('ç', 'c');
};
