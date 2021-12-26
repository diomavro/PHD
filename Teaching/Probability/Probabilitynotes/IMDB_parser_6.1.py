#!/usr/bin/python
# -*- coding: utf-8 -*-             #unbedingt benötigt!!
from urllib.request import urlopen
import re, time
from tkinter import *
from threading import *


class Parser(Thread):
    def __init__(self):
        Thread.__init__(self)
    def start(self, rater, movieType, num_votes):
        start = time.time()
        nummernListe = self.filmNummern(movieType, num_votes)                                #here film numbers is called
        f = open(str(rater)+".txt", "w")        #damit die Dateien immer anfangs leer sind
        f.write("")                             #
        f.close()                               #
        f = open(str(rater)+"_sorted.txt", "w") #
        f.write("")                             #
        f.close()                               #    
        top250 = urlopen("http://www.imdb.com/chart/top?")      #so that the files are always initially empty
        top250_source = top250.read()                                   #
        for nummer in nummernListe:                                                         
            movie = self.rating("http://www.imdb.com/title/"+nummer+"/ratings-"+rater, rater)      #here is called rating
            treffer = top250_source.find('''.
      <a href="/title/'''+nummer)                                       #
            if treffer == -1:                                           #
                movie += "  | NO"+"\n"                                  #
            else:                                                       #
                platz_start = treffer - 3                               #
                platz_end = platz_start + 3                             #
                platzierung = top250_source[platz_start:platz_end]      #
                movie += "  | "+platzierung+"\n"                        #
            f = open(str(rater)+".txt", "a")
            f.write(movie)
            f.close()
        end = time.time()
        print (end-start)
        self.ordnen(rater)                                                                  #here will arrange called

    def filmNummern(self, movieType, num_votes):                                             #i: Going through the list of all the films ; j : through the individual films on one side of the list

        anzahlText = urlopen("http://www.imdb.com/search/title?at=0&count=1&num_votes="+num_votes+",&sort=user_rating,desc&start=1&title_type="+movieType+",&view=simple")
        anzahlText_source = anzahlText.read()                                           #finds the number of movies to be viewed
        anzahl_start = anzahlText_source.find("titles.")-7
        anzahl_end = anzahl_start+6 
        anzahl = anzahlText_source[anzahl_start:anzahl_end]
        while anzahl.find(" ") != -1:
            anzahl = anzahl[1:]
        if anzahl.find(",") != -1:
            an = anzahl[0:anzahl.find(",")]
            zahl = anzahl[anzahl.find(",")+1:len(anzahl)]
            anzahl = an+zahl
        else:
            pass
        m = int(anzahl)
        n = m/100
        rest = anzahl[len(anzahl)-2:len(anzahl)]
        k = int(rest)
        print ("Quantity of entries = "+anzahl)

        nummernListe = []
        for i in range(0, n):
            filmListe = urlopen("http://www.imdb.com/search/title?at=0&count=100&num_votes="+num_votes+",&sort=user_rating,desc&start="+str(i*100+1)+"&title_type="+movieType+",&view=simple")
            html_Liste = filmListe.read()
            print (i+1)
            for j in range(1, 101): #<102
                start = html_Liste.find('''><a href="/title/''')+17                         # has ever changed
                end = start+9
                filmNummer = html_Liste[start:end]
                nummernListe.append(filmNummer)
                html_Liste = html_Liste[end:len(html_Liste)]
        for i in range(0, 1):
            filmListe = urlopen("http://www.imdb.com/search/title?at=0&count=100&num_votes="+num_votes+",&sort=user_rating,desc&start="+str(n*100+1)+"&title_type="+movieType+",&view=simple")
            html_Liste = filmListe.read()
            for j in range(1, k+1): 
                start = html_Liste.find('''><a href="/title/''')+17                      
                end = start+9
                filmNummer = html_Liste[start:end]
                nummernListe.append(filmNummer)
                html_Liste = html_Liste[end:len(html_Liste)]
        return nummernListe
            
    def rating(self, url, rater):
        page = urlopen(url)                 #Open URL Attention : Invoice is true only for Top1000 voters !!! All the others have other criteria !!!
        page_source = page.read()                                           
        start = page_source.find("<title>")+7       #Titel
        end = page_source.find("</title>")-15
        titel = page_source[start:end]

        abgelesen_start = page_source.find('''</p><p><a href="#reports">Demographic breakdowns''')-12       #zur Überprüfung, ob
        abgelesen_end =  abgelesen_start+3                                                                  #die Formel wirklich
        abgelesen = page_source[abgelesen_start:abgelesen_end]                                              #stimmt.
        
        ratings =[]                                 #Anzahl der 10, 9, 8 ... votes
        for i in range(1, 11):
            start = page_source.find('''</tr><tr><td align="right">''')+27
            end = page_source.find('''</td><td nowrap="1"''')
            temp = page_source[start:end]
            temp = float(temp)
            ratings.append(temp)            
            page_source = page_source[(end+19):len(page_source)]

        gsumme = 0                              #Rechnung für mehr nachkommastellen
        anzahl = 0
        for k in range(1, 11):
            gsumme += ratings[-k]*(k)
            anzahl += ratings[-k]
        average = gsumme / anzahl

##### Here begins the part, that is only correct for the "top 1000 voters" #####

        if rater == "top_1000":
            a = 0.06
        else:
            a = 0.06            ##### This number is the amount of votes cut away from both sides (10 and 1 votes). Maybe you'll have to change it too.

        newrate = ratings                       #weighted average , instead of mean formula has yet to be found for all other votergruppen
        print (newrate)
        nrand = anzahl*a                      #varies for different votergruppen !!!! For top1000: 0.06
        for m in range(1, 11):                  #lower Rand
            if nrand > 0:
                if nrand > ratings[-m]:
                    nrand -= ratings[-m]
                    newrate[-m] = 0
                else:
                    newrate[-m] = ratings[-m] - nrand
                    nrand = 0
            else:
                pass
        nrand = anzahl*a                     # for top1000: 0.06
        for n in range(0,10):                   #top Rand
            if nrand > 0:
                if nrand > ratings[n]:
                    nrand -= ratings[n]
                    newrate[n] = 0
                else:
                    newrate[n] = ratings[n] - nrand
                    nrand = 0
            else:
                pass
        gsummenew = 0                           #improved results
        anzahlnew = 0
        for p in range(1, 11):
            gsummenew += newrate[-p]*(p)
            anzahlnew += newrate[-p]
        averagenew = gsummenew / anzahlnew                   

##### Here it ends #####

##### If you want to try some things on your own here is the place! #####
## Make sure to always write your program like this:
##        if rater == "top_1000":
##            pass
##        else:
##            #your code
##            averagenew = #your code


##### Here a first (and unsuccessful) try of mine starts #####       

        if rater == "top_1000":                         #Experiment: adjusting for other Votergruppen
            pass                                        #Programmiere "Richtigen-Algorithmus-Suchmaschine (mit Variablen und Vergleich ausgelesen <-> berechnet)
        else:
            gsummenew_new = 0
            anzahlnew_new = 0
            for k in range(1, 11):                                      #Hier Zahl
                gsummenew_new += newrate[-k]*(k)*(1-int(abs(k-averagenew))*0.0)
                anzahlnew_new += newrate[-k]*(1-int(abs(k-averagenew))*0.0)
                print (abs(k-averagenew))
            averagenew = gsummenew_new / anzahlnew_new

##### Here it ends #####

        bla = str(averagenew)
        while len(bla) <= 12:                   #Ästhetische verbesserung. Sorgt dafür, dass alle Wertungen die gleiche Anzahl Ziffern haben
            bla += "0"
        print ("Cal. weighted average: "+bla+' | '+titel)             ##### cal. = calculated
        print ("Real weighted average: "+abgelesen)
        return bla+' | '+titel

    def ordnen(self, rater):                    #Sortieren der Ergebnisse 
        x = 1
        liste = []
        f = open(str(rater)+".txt", "r")
        for line in f.readlines():
            liste.append(line)
        f.close()
        liste = sorted(liste, reverse=True)
        fSorted = open(str(rater)+"_sorted.txt", "a")
        fSorted.write(" +/- |    Wertung    | Titel\n")     #Legende
        for film in liste:
            platzierung = film[len(film)-4:len(film)-1]
            film = film[0:len(film)-7]+"\n"
            if platzierung == " NO":
                film = "  NO | "+film
            else:
                veranderung = int(platzierung) - x
                if veranderung >= 0:                        #Nur für Ästhetik. Führende Nullen bei Veränderung (z.B. +003)
                    veranderung = "%03i" % veranderung
                    bla = "+"+str(veranderung)
                else:
                    veranderung = "%04i" % veranderung
                    bla = str(veranderung)
                film = bla+" | "+film
            fSorted.write(film)
            x += 1
        fSorted.close()
        self.zeichen(rater)

    def zeichen(self, rater):                               #Sonderzeichen
        f = open(str(rater)+"_sorted.txt", "r")
        text = f.read()
        f.close()
        f = open("Sonderzeichen.txt", "r")
        sonderzeichen = f.read()
        f.close()
        treffer = text.find("&#")
        while treffer != -1:
            treffer2 = text.find(";")
            szeichen = text[treffer:treffer2+1]
            er = sonderzeichen.find(szeichen)
            ersatz = sonderzeichen[er-2:er-1]
            text = text[:treffer]+ersatz+text[treffer2+1:]
            treffer = text.find("&#")
        fzeichen = open(str(rater)+"_sorted.txt", "w")
        fzeichen.write(text)
        fzeichen.close()

class IMDB:
    def __init__(self):
        self.gui()
    def gui(self):                                      #Komanndobox, hier fehlen noch einige Votergruppen
        root = Tk()
        root.title("IMDB")

        Label(root, text="Number of votes").grid(row=0)                               #Anzahl Bewertungen
        num_votes = Entry(root)
        num_votes.grid(row=0, column=1)

        Label(root, text="Type Of Movie").grid(row=2)                                   #Film-Typ
        wahl1 = IntVar()                                                        
        feature = Checkbutton(root, text="Feature Film", variable=wahl1)
        feature.grid(row=3, column=0)
        wahl2 = IntVar()
        documentary = Checkbutton(root, text="Documentary", variable=wahl2)
        documentary.grid(row=4, column=2)
        wahl3 = IntVar()
        tv_movie = Checkbutton(root, text="TV Movie", variable=wahl3)
        tv_movie.grid(row=3, column=1)
        wahl4 = IntVar()
        tv_movie = Checkbutton(root, text="TV Series", variable=wahl4)
        tv_movie.grid(row=3, column=2)
        wahl5 = IntVar()
        tv_movie = Checkbutton(root, text="TV Episode", variable=wahl5)
        tv_movie.grid(row=3, column=3)
        wahl6 = IntVar()
        tv_movie = Checkbutton(root, text="TV Special", variable=wahl6)
        tv_movie.grid(row=4, column=0)
        wahl7 = IntVar()
        tv_movie = Checkbutton(root, text="Mini-Series", variable=wahl7)
        tv_movie.grid(row=4, column=1)
        wahl8 = IntVar()
        tv_movie = Checkbutton(root, text="Video Game", variable=wahl8)
        tv_movie.grid(row=4, column=3)
        wahl9 = IntVar()
        tv_movie = Checkbutton(root, text="Short Film", variable=wahl9)
        tv_movie.grid(row=5, column=0)
        wahl10 = IntVar()
        tv_movie = Checkbutton(root, text="Video", variable=wahl10)
        tv_movie.grid(row=5, column=1)        
        
        Label(root, text="Group Of Raters").grid(row=6)
        titleTypes = ["Top 1000 voters", "Males under 18", "Aged under 18", "Aged 45+"]     #Ratergruppe
        rater = StringVar(root)
        om2 = OptionMenu(root, rater, *titleTypes)
        om2.grid(row=7, column=1)

        ok = Button(root, text="OK", command=lambda: self.imdb(rater.get(), wahl1.get(), wahl2.get(), wahl3.get(), wahl4.get(), wahl5.get(), wahl6.get(), wahl7.get(), wahl8.get(), wahl9.get(), wahl10.get(), num_votes.get()))
        ok.grid(row=8)
            
        root.mainloop()
        
    def imdb(self, rater, wahl1, wahl2, wahl3, wahl4, wahl5, wahl6, wahl7, wahl8, wahl9, wahl10, num_votes):
        parser = Parser()
        if wahl1==1:
            wahl1 = "feature,"
        else:
            wahl1=""
        if wahl2==1:
            wahl2 = "documentary,"
        else:
            wahl2=""
        if wahl3==1:
            wahl3 = "tv_movie,"
        else:
            wahl3=""
        if wahl4==1:
            wahl4 = "tv_series,"
        else:
            wahl4=""
        if wahl5==1:
            wahl5 = "tv_episode,"
        else:
            wahl5=""
        if wahl6==1:
            wahl6 = "tv_special,"
        else:
            wahl6=""
        if wahl7==1:
            wahl7 = "mini_series,"
        else:
            wahl7=""
        if wahl8==1:
            wahl8 = "game,"
        else:
            wahl8=""
        if wahl9==1:
            wahl9 = "short,"
        else:
            wahl9=""
        if wahl10==1:
            wahl10 = "video,"
        else:
            wahl10=""
        movieType = wahl1+wahl2+wahl3+wahl4+wahl5+wahl6+wahl7+wahl8+wahl9+wahl10
        if rater=="Top 1000 voters":
            rater = "top_1000"
        elif rater =="Males under 18":
            rater = "male_age_1"
        elif rater == "Aged under 18":
            rater = "age_1"
        elif rater == "Aged 45+":
            rater = "age_4"
        parser.start(rater, movieType, num_votes)

imdb = IMDB()
