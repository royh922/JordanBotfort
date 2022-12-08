package me.JordanBotfort.bot;

import net.dv8tion.jda.api.events.message.MessageReceivedEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Scanner;

import javax.annotation.Nonnull;

import java.util.Arrays;
import java.util.HashSet;
import java.util.Timer;
import java.util.TimerTask;

import java.lang.ProcessBuilder;

public class Commands extends ListenerAdapter {
    final String tickers[] = {"CCL","AMZN","AMD","NVDA","AAPL","TSLA","BBD","ITUB","GRAB","DLO","F","NIO","SOFI","XPEV","ABEV","TGT","DNA","INTC","PBR","META","T","NU","SNAP","LU","VALE","AMC","PLTR","AAL","BABA","UBER","WBD","PINS","SWN","CSCO","GOOGL","VTRS","GOOG","TLRY","MSFT","COIN","TSM","BAC","ZI","LCID","MU","M","NOK","U","LUMN","TME","CMCSA","PARA","C","AFRM","SHOP","RIG","GSAT","SIRI","LYFT","RLX","DKNG","APE","PBR-A","NCLH","VZ","PLUG","IQ","HPE","WFC","KGC","KMI","ASX","UMC","PTON","ET","BILI","XOM","VOD","TEVA","SLB","AGNC","HOOD","GGB","RBLX","OXY","AUY","FCX","CTRA","AQN","AMAT","MRVL","PFE","GM","BTG","IBN","TJX","SQ","MPW","PCG","GOLD","DIS","SE","WMT","HBI","HBAN","KO","YMM","ZIM","CPG","ELAN","PYPL","BMY","RIVN","CSX","CLF","USB","MO","CPNG","CS","KEY","QCOM","UAA","ERIC","HPQ","BEKE","NTRA","MAT","XP","DVN","ONON","GFI","BP","MRK","GPS","FTCH","MRO","NEE","JBLU","MQ","AMCR","MDT","PDD","NFLX","CIG","CVX","JPM","ON","CHPT","STNE","LI","AA","QS","LOW","X","TXN","COP","ABBV","DAL","BBWI","KDP","STLA","TFC","PAYO","JWN","TCOM","DBX","CVS","FTI","JD","BRFS","FIS","RUN","EPD","PATH","CRM","TOST","GILD","SCHW","OSH","NYCB","ING","V","PR","RF","RCM","ORCL","MCHP","NKE","PANW","HAL","AEO","WOLF","BAX","AVTR","BKR","KHC","AR","ROKU","IVZ","ALLY","AG","RKLB","LAZR","HL","JNJ","NLY","CTSH","TTD","VICI","NWL","CX","AAP","SBUX","SO","VRT","GSK","WDC","EBAY","BSX","HD","EW","NEM","APA","SYF","TCEHY","DASH","PG"};
    final private HashSet<String> tickers_set = new HashSet<>(Arrays.asList(tickers));
    @Override
    public void onMessageReceived(@Nonnull MessageReceivedEvent e) {
        if (!e.getAuthor().isBot()) {
            String m = e.getMessage().toString();
            m = m.split(":")[2];
            m = m.substring(0, m.indexOf("("));
            if(m.charAt(0) != '!') return;

            String opt = m.split(" ")[0];
            String User = e.getAuthor().toString().split("[(]")[0].substring(2);
            
            new File("./" + User).mkdirs();

            if(opt.equals("!run")){
                File currentTrack = new File("./" + User + "/track.txt");
                String python = "python";
                String jordan = "jordan.py";
                // String jordan = "test.py";
                String plot = "plot.py";
                Timer timer = new Timer();
                timer.scheduleAtFixedRate(new TimerTask(){
                    @Override
                    public void run() {
                        String tickers = null;
                        try {
                            if(currentTrack.exists()){
                                Scanner scan = new Scanner(currentTrack);
                                if(scan.hasNext()) tickers = scan.nextLine();
                                scan.close();
                            }
                            if(tickers == null){
                                e.getChannel().sendMessage("Please add a valid stock ticker to track! ex. amzn, tsla").queue();
                                return;
                            }
                            ProcessBuilder pb = new ProcessBuilder(python, jordan, User, tickers);
                            // pb.redirectErrorStream(true);
                            pb.inheritIO();
                            Process p = pb.start();
                            pb = new ProcessBuilder(python, plot, User);
                            // pb.redirectErrorStream(true);
                            p = pb.start();
                        } catch (IOException ex) {ex.printStackTrace();}
                    }   
                }, 0, 60*1000);
            }
            
            else if (opt.equals("!track")) {
                e.getMessage().addReaction("U+1F4B0").queue();
                if (m.split(" ").length > 0 && tickers_set.contains(m.split(" ")[1].toUpperCase())) {
                    String stock = m.split(" ")[1].toUpperCase();
                    e.getChannel().sendMessage("Tracking " + stock).queue();
                    File currentTrack = new File("./" + User + "/track.txt");
                    try {
                        String s1[] = {};
                        if(currentTrack.exists()){
                            Scanner scan = new Scanner(currentTrack);
                            if(scan.hasNext()) s1 = scan.nextLine().split("[,]");
                            scan.close();
                        }
                        HashSet<String> set = new HashSet<>(Arrays.asList(s1));
                        set.add(stock);
                        PrintWriter outFile = new PrintWriter("./" + User + "/" + "track.txt");
                        outFile.print(String.join(",", set));
                        outFile.close();
                    } catch (IOException ex) {ex.printStackTrace();}
                }
                else e.getChannel().sendMessage("Please add a valid stock ticker to track! ex. amzn, tsla").queue();
            } 

            else if(opt.equals("!untrack")){
                if (m.split(" ").length > 1) {
                    String stock = m.split(" ")[1].toUpperCase();
                    try {
                        File currentTrack = new File("./" + User + "/" + "track.txt");
                        Scanner scan = new Scanner(currentTrack);
                        String s1[] = scan.nextLine().split("[,]");
                        HashSet<String> set = new HashSet<>(Arrays.asList(s1));
                        if(set.remove(stock)) e.getChannel().sendMessage("Untracked " + stock).queue();
                        else e.getChannel().sendMessage("Not found in tracked list!").queue();
                        PrintWriter outFile = new PrintWriter("./" + User + "/" + "track.txt");
                        outFile.print(String.join(",", set));
                        outFile.close();
                        scan.close();
                    } catch (IOException ex) {ex.printStackTrace();}
                }
                else e.getChannel().sendMessage("Please add a ticker to be untracked! ex. amzn, tsla").queue();
            }

            else if (opt.equals("!stocks")) {
                File currentTrack = new File("./" + User + "/" + "track.txt");
                try {
                    Scanner scan = new Scanner(currentTrack);
                    if (scan.hasNext())
                        e.getChannel().sendMessage(User + ": " + scan.nextLine()).queue();
                    else e.getChannel().sendMessage("Not tracking any stocks. Use !track to add stocks").queue(); 
                    scan.close();
                } catch (FileNotFoundException e1) {
                    e.getChannel().sendMessage("Not tracking any stocks. Use !track to add stocks").queue();
                }
            } 

            else if (opt.equals("!graph")) {
                e.getChannel().sendMessage("Loading graph of profits... ").queue();
                File fig = new File("./" + User + "/fig.png");
                if(fig.exists()) e.getChannel().sendFile(fig).queue();
                else e.getChannel().sendMessage("Try again later or add more stocks to track").queue();
            } 

            else if (opt.equals("!log")) {
                int lines = 0;
                if (m.split(" ").length > 1) lines = Integer.parseInt(m.split(" ")[1]);
                else lines = 5;
                e.getChannel().sendMessage(String.format("Displaying the last %d transactions", lines)).queue();
                File log = new File("./" + User + "/" + "logs.txt");
                String logs = "";
                try {
                    Scanner scan = new Scanner(log);
                    while(scan.hasNext() && (lines-- > 0)) logs += scan.nextLine() + "\n";
                    e.getChannel().sendMessage(logs).queue(); 
                    scan.close();
                } catch (FileNotFoundException e1) {
                    e.getChannel().sendMessage("Not trading. Use !track to add stocks and !run to start trading!").queue();
                }
            }

            else if(opt.equals("!help")){
                String message = "!track <ticker> to add stocks to trade\n!stocks to view all tracking stocks\n";
                message += "!untrack <ticker> to remove a stock from trading\n";
                message += "!graph to see total assets and performance over time\n";
                message += "!log to see past transaction details";
                e.getChannel().sendMessage(message).queue();
            }

            else{
                e.getChannel().sendMessage("Invalid input. Use !help to get a list of comments to call").queue();
                File egg = new File("./egg.jpg");
                e.getChannel().sendFile(egg).queue();
            }
        }
    }
}