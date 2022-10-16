#Bibliothes/Modules
from fileinput import filename
import PyPDF2
import requests
from PyPDF2 import PdfFileReader
from googlesearch import search 
from bs4 import BeautifulSoup
import glob, os


path = "/home/basto/Documents/travail/DEFT2021-cas-cliniques/test2/"
#os.chdir("/home/basto/Documents/travail/DEFT2021-cas-cliniques/test2")
for file in glob.glob("*.txt"):
    
    #recueration du nom du fichier
    file_Name = file.split('.txt',1) 

    #recuperation des phrases dans les "txt"
    textAnalyse = open(file,'r')
    data = textAnalyse.read()
    data = data.split('\n',1)
    query = data[0]

    #recherche google des phrases
    print('Recherche Google...')
    for url in search(query, tld="co.in", lang = 'fr', num=1, stop=1, pause=2, verify_ssl=True): 
        
        #recuperation des informations du pdf
        r = requests.get(url, stream=True)
        with open(path+'/pdf.pdf', 'wb') as f:
            print('ecriture PDF...')
            f.write(r.content)
            print('PDF ecrit.\n')
            
        try:
            document = PdfFileReader(open(path+'/pdf.pdf','rb'))
            pdftext = ""
            for page in [0]:
                pageObj = document.getPage(page)
                pdftext += pageObj.extractText().replace('\n','')

            resultatFichier = open(path + '/resultat.txt','a')

            #exeption d'ecriture 1
            if "Résumé" in pdftext:
                textTraitement = pdftext.split('Résumé',1)
                textTraitement2 = textTraitement[1].split('Mots clés :',1)
                #print('Résumé trouvé: \n',textTraitement2[0])

                #resultatFichier = open(path + '/resultat.txt','a')
                #print(filename[0])
                resultatFichier.write(file_Name[0] + " ; Résumé: " + textTraitement2[0]+';' + '\n')
                resultatFichier.close()

            #exeption d'ecriture 2
            if "Objectifs" in pdftext:
                textTraitement = pdftext.split('Objectifs',1)
                #print('Résumé trouvé: \n','Objectifs ',textTraitement[1])    

                #resultatFichier = open(path + '/resultat.txt','a')
                #print(filename[0])
                resultatFichier.write(file_Name[0] + " ; Résumé: Objectifs:" + textTraitement[1] + ';' +'\n')
                resultatFichier.close()

            #pas de resumé dans le PDF ?
            else:
                '''
                resultatFichier = open(path + '/resultat.txt','a')
                resultatFichier.write("DOCUMENT NON VALIDE\n")
                resultatFichier.clode()
                print('le document n est pas valide\n')
                '''
                #resultatFichier = open(path + '/resultat.txt','a')
                #print(filename[0])
                resultatFichier.write(file_Name[0] + ";DOCUMENT NON VALIDE;\n")
                resultatFichier.close()
        
        except PyPDF2.utils.PdfReadError:
            print('[!]PAS UN PDF')
            print('Recherche HTML...\n')

            requete = requests.get(url)
            
            resultatFichier = open(path + '/resultat.txt','a')

            try:
                page = requete.text.split('Résumé',1)
                page = page[1].split('Mots clés',1)
                cleantext = BeautifulSoup(page[0])
                resultatFichier.write(file_Name[0] + ';' + cleantext + ';' + '\n')

                resultatFichier.close()

            except:
                resultatFichier.write(file_Name[0] + ';' + 'DOCUMENT NON VALIDE' + ';' + '\n')
