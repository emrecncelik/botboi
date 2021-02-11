const Discord = require('discord.js');
const snoowrap = require('snoowrap');

module.exports = {
    name: 'reddit',
    description: 'Gets reddit top posts from a given subreddit.',
    args: true,
    usage: '<subreddit name> <time> <limit>',
    async execute(message, args) {
        const r = new snoowrap({
            userAgent: 'A random string? I actually do not know what this is.',
            clientId: process.env.REDDIT_CLIENT_ID,
            clientSecret: process.env.REDDIT_CLIENT_SECRET,
            refreshToken: process.env.REDDIT_REFRESH,
        });

        const subreddit_query = args[0];
        const time_query = args[1];
        const limit_query = parseInt(args[2]);

        const subreddit = await r.getSubreddit(subreddit_query);
        const topPosts = await subreddit.getTop({ time: time_query, limit: limit_query });

        for (let i = 0; i < topPosts.length; i++) {
            const post = topPosts[i];
            message.channel.send(makeEmbed(post));
            // Send url if the post contains media or url
            // Embed gifs or videos don't work, so sending media separately
            if (!post.is_self) {
                message.channel.send(post.url);
            }
            console.log(post.title);
        }
    },
};

function makeEmbed(post) {
    const sub_name = post.subreddit_name_prefixed;
    const title = post.title;
    const text = post.selftext;
    const url = 'https://www.reddit.com' + post.permalink;

    const redditEmbed = new Discord.MessageEmbed()
        .setAuthor(sub_name)
        .setTitle(title)
        .setDescription(text)
        .setURL(url);
    return redditEmbed;
}