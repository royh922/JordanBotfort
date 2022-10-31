package me.JordanBotfort.bot;

import net.dv8tion.jda.api.events.message.MessageReceivedEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Scanner;
import java.util.Arrays;
import java.util.HashSet;

public class commands extends ListenerAdapter {
    @Override
    public void onMessageReceived(MessageReceivedEvent e) {
        if (!e.getAuthor().isBot()) {
            String m = e.getMessage().toString();
            m = m.split(":")[2];
            m = m.substring(0, m.indexOf("("));
            if(m.charAt(0) != '!') return;

            String opt = m.split(" ")[0];
            String User = e.getAuthor().toString().split("[(]")[0].substring(2);

            if (opt.equals("!track")) {
                e.getMessage().addReaction("U+1F4B0").queue();
                if (m.split(" ").length > 1) {
                    String stock = m.split(" ")[1].toUpperCase();
                    e.getChannel().sendMessage("Tracking " + stock).queue();
                    File currentTrack = new File(User + "_" + "track.txt");
                    try {
                        if (!currentTrack.exists()) {
                            PrintWriter outFile = new PrintWriter(User + "_" + "track.txt");
                            if (stock.length() > 0)
                                outFile.print(stock);
                            outFile.close();
                        } 
                        else {
                            Scanner scan = new Scanner(currentTrack);
                            if (scan.hasNext()) {
                                String s1[] = scan.nextLine().split("[,]");
                                HashSet<String> set = new HashSet<>(Arrays.asList(s1));
                                set.add(stock);
                                PrintWriter outFile = new PrintWriter(User + "_" + "track.txt");
                                outFile.print(String.join(",", set));
                                outFile.close();
                            }
                            scan.close();
                        }
                    } catch (IOException ex) {ex.printStackTrace();}
                }
                else e.getChannel().sendMessage("Please add a stock ticker to track! ex. amzn, tsla").queue();
            } 
            else if (opt.equals("!stocks")) {
                File currentTrack = new File(User + "_" + "track.txt");
                try {
                    Scanner scan = new Scanner(currentTrack);
                    if (scan.hasNext())
                        e.getChannel().sendMessage(User + ": " + scan.nextLine()).queue();
                    scan.close();
                } catch (FileNotFoundException e1) {
                    e.getChannel().sendMessage("Not tracking any stocks. Use !track to add stocks").queue();
                }
            } 
            else if (opt.equals("!hello")) { //TODO Fun easter egg?
                e.getChannel().sendMessage("Hello world!").queue();
            } 
            else if (opt.equals("!graph")) { //TODO Implement real time graph retrieval
                e.getChannel().sendMessage("Loading graph of profits... ").queue();
                File fig = new File("demo.png");
                e.getChannel().sendFile(fig).queue();
                /*
                 * File currentTrack = new File("track.txt");
                 * try
                 * {
                 * Scanner scan = new Scanner(currentTrack);
                 * if (currentTrack.exists())
                 * {
                 * String s1 = scan.nextLine();
                 * String s2 = "graph";
                 * scan.close();
                 * PrintWriter outFile = new PrintWriter("track.txt");
                 * outFile.println(s1);
                 * outFile.print(s2);
                 * outFile.close();
                 * }
                 * }
                 * catch (FileNotFoundException ex)
                 * {
                 * ex.printStackTrace();
                 * }
                 */
            } 
            else if (opt.equals("!log")) {
                String num = m.substring(m.indexOf('!') + 4);
                num = num.substring(0, num.indexOf("("));
                System.out.println(num);
                e.getChannel().sendMessage("Displaying the last" + num + " transactions").queue();
            }
            else{
                e.getChannel().sendMessage("Invalid input. Use !help to get a list of comments to call").queue();
            }
        }
    }
}
