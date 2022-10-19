package me.JordanBotfort.bot;

import net.dv8tion.jda.api.events.message.MessageReceivedEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.Locale;
import java.util.Scanner;

public class commands extends ListenerAdapter
{
    @Override
    public void onMessageReceived(MessageReceivedEvent e)
    {
        if(!e.getAuthor().isBot())
        {
            String m = e.getMessage().toString();
            if (m.contains("!track"))
            {
                String stock = m.substring(m.indexOf('!') + 6);
                stock = stock.substring(1, stock.indexOf("(")).toUpperCase(Locale.ROOT);
                e.getChannel().sendMessage("Tracking " + stock).queue();
                File currentTrack = new File("track.txt");
                try {
                    Scanner scan = new Scanner(currentTrack);
                    if (currentTrack.exists()&&scan.hasNextLine())
                    {
                        String s1 = scan.nextLine();
                        String s2 = "";
                        if(scan.hasNextLine())
                        {
                            s2 = scan.nextLine();
                        }
                        scan.close();
                        PrintWriter outFile = new PrintWriter("track.txt");
                        outFile.print(s1+",");
                        outFile.println(stock);
                        outFile.print(s2);
                        outFile.close();
                    }
                    else if (!currentTrack.exists())
                    {
                        PrintWriter outFile = new PrintWriter("track.txt");
                        outFile.print(stock);
                        outFile.close();
                    }
                    else
                    {
                        PrintWriter outFile = new PrintWriter("track.txt");
                        outFile.println(stock);
                        outFile.close();
                    }
                }
                catch (FileNotFoundException ex)
                {
                    ex.printStackTrace();
                }
            }
            else if (m.contains("!graph"))
            {
                e.getChannel().sendMessage("Loading graph of profits... ").queue();
                File currentTrack = new File("track.txt");
                try
                {
                    Scanner scan = new Scanner(currentTrack);
                    if (currentTrack.exists())
                    {
                        String s1 = scan.nextLine();
                        String s2 = "graph";
                        scan.close();
                        PrintWriter outFile = new PrintWriter("track.txt");
                        outFile.println(s1);
                        outFile.print(s2);
                        outFile.close();
                    }
                }
                catch (FileNotFoundException ex)
                {
                    ex.printStackTrace();
                }
            }
            else if (m.contains("!log"))
            {
                String num = m.substring(m.indexOf('!')+4);
                num = num.substring(0, num.indexOf("("));
                System.out.println(num);
                e.getChannel().sendMessage("Displaying the last"+num+" transactions").queue();
            }
        }
    }
}
