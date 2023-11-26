from nltk.ccg import chart, lexicon
import pandas as pd
import numpy as np


lexstring='''
:- S,N
chat => N
dort => N\S
'''

lex = lexicon.fromstring(lexstring)
print(lex)
parser = chart.CCGChartParser(lex, chart.ApplicationRuleSet)

phrase="chat dort"
for parse in parser.parse(phrase.split()):
    chart.printCCGDerivation(parse)
