package me.JordanBotfort.bot;

import net.dv8tion.jda.api.JDABuilder;
import net.dv8tion.jda.api.entities.Message;
import net.dv8tion.jda.api.events.message.MessageReceivedEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;
import net.dv8tion.jda.api.requests.GatewayIntent;

import javax.security.auth.login.LoginException;

public class Jordan extends ListenerAdapter
{
    public static void main(String[] args) throws LoginException
    {
        JDABuilder bot = JDABuilder.createDefault(TOKEN);
        bot.addEventListeners(new commands());
        bot.enableIntents(GatewayIntent.GUILD_MESSAGES);
        bot.enableIntents(GatewayIntent.DIRECT_MESSAGES);
        bot.build();
    }
}

