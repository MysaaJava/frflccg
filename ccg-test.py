from nltk.ccg import chart, lexicon
from nltk.ccg.chart import CCGChart,CCGLeafEdge
from nltk.tree import Tree
import pandas as pd
import numpy as np


valz = {
    '>' : 0.8,
    '<' : 0.7
}
def rweight(rule):
    s = rule.__str__()
    if s in valz:
        return valz[s]
    else:
        return 1.0 # Base rules weight

# Implements the CYK algorithm, code partly taken from nltk
def weightedParse(tokens, lex, rules):
    chart = CCGChart(list(tokens))
    
    # Initialize leaf edges.
    for index in range(chart.num_leaves()):
        for token in lex.categories(chart.leaf(index)):
            new_edge = CCGLeafEdge(index, token, chart.leaf(index))
            new_edge.weight = 1.0
            chart.insert(new_edge, ())

    # Select a span for the new edges
    for span in range(2, chart.num_leaves() + 1):
        for start in range(0, chart.num_leaves() - span + 1):
            
            bestedge = None
            
            # Try all possible pairs of edges that could generate
            # an edge for that span
            for part in range(1, span):
                lstart = start
                mid = start + part
                rend = start + span

                for left in chart.select(span=(lstart, mid)):
                    for right in chart.select(span=(mid, rend)):
                        # Generate all possible combinations of the two edges
                        for rule in rules:
                            edgez = list(rule.apply(chart, lex, left, right))
                            if(len(edgez)==1):
                                edge = edgez[0]
                                edge.weight = rweight(rule) * left.weight * right.weight
                                edge.triple = (rule,left,right)
                                if (bestedge == None) or (bestedge.weight < edge.weight):
                                    bestedge = edge
                            elif(len(edgez)!=0):
                                print("Too many new edges (unsupported rule used)")
                                
                        # end for rule loop
                    # end for right loop
                # end for left loop
            # end for part loop
    return chart

def wpToTree(edge):
    if isinstance(edge,CCGLeafEdge):
        return Tree((edge.token(),"Leaf"),[Tree(edge.token(),[edge.leaf()])])
    else:
        return Tree(
            (chart.Token(None,edge.categ()),edge.triple[0].__str__()),
            [wpToTree(t) for t in (edge.triple[1:])])

def bestTree(tokens, lex, rules):
    # We build the weighgted parse tree using cky
    w = weightedParse(tokens, lex, rules)
    # We get the biggest edge
    e = list(w.select(start=0,end=len(tokens)))[0]
    # We get the tree that brought us to this edge
    return (wpToTree(e),e.weight)



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
                lexstring+=mot+' => ' + table['Cat'+str(j)][i]  + '\n'

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

    lines.append("le chat et la souris dorment")
    
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
        
        
        # On affiche la dérivation la meilleure pour l'arbre
        if (i==0):
            print("Pas de dérivation tout court :/")
        else:
            t,d = bestTree(phrase.split(), lex, chart.ApplicationRuleSet)
            print("Found derivation tree with weight",d)
            chart.printCCGDerivation(t)
            
            

