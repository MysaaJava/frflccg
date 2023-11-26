from nltk.ccg import chart, lexicon
import pandas as pd
import numpy as np


# On importe notre lexique sous forme de tableur
table = pd.read_excel("CategoriesGramaticalesCombinatoire.ods", engine="odf")

# On récupère le nombre de mots qui ont été définis
n = len(table['MOT'])

# On donne la liste des catégories primitives
lexstring=':- S,N,Pp\n'
# On ajoute la notation V pour N\S
lexstring+='V :: S\\N\n'

# On lis les données depuis le tableur en une chaine de caractère parsable
for i in range(n):
    for j in range(3):
        if isinstance(table['Cat'+str(j)][i],str):
            for mot in table['MOT'][i].split('/'):
                lexstring+=mot+' => ' + table['Cat'+str(j)][i] + '\n'

# Pour inverser les slash dans le lexicon
#lexstring = lexstring.replace('\\','#').replace('/','\\').replace('#','/')

# On crée notre lexique
lex = lexicon.fromstring(lexstring)

# On crée le parser, on donne l'ensemble des règles qu'il est cencé connaître
parser = chart.CCGChartParser(lex, chart.DefaultRuleSet)
#parser = chart.CCGChartParser(lex, chart.ApplicationRuleSet)

printTotal=True
printDerivations=not printTotal

# On lit les phrases dans le fichier
with open('phrases.txt') as f:
    lines = f.readlines()

    lines.append("mon voisin lui donne le chat")

    for phrase in lines:
        # On met tout en minuscule
        phrase = phrase.lower().strip()
        if printDerivations:
            print("============================================================================")
            print('#',phrase)
        lex = lexicon.fromstring(lexstring)
        parser = chart.CCGChartParser(lex, chart.ApplicationRuleSet)

        # Et on affiche tous les arbres de dérivation trouvés
        i=0
        for parse in parser.parse(phrase.split()):
            i+=1
            if printDerivations:
                chart.printCCGDerivation(parse)
            
        if printTotal:
            print(i,phrase)
