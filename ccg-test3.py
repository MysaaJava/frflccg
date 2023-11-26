from nltk.ccg import chart, lexicon

lex = lexicon.fromstring('''
     :- S, NP, N, VP

     Det :: NP/N
     Pro :: NP
     Modal :: S\\NP/VP

     TV :: VP/NP
     DTV :: TV/NP

     the => Det

     that => Det
     that => NP

     I => Pro
     you => Pro
     we => Pro

     chef => N
     cake => N
     children => N
     dough => N

     will => Modal
     should => Modal
     might => Modal
     must => Modal

     and => var\\.,var/.,var

     to => VP[to]/VP

     without => (VP\\VP)/VP[ing]

     be => TV
     cook => TV
     eat => TV

     cooking => VP[ing]/NP

     give => DTV

     is => (S\\NP)/NP
     prefer => (S\\NP)/NP

     which => (N\\N)/(S/NP)

     persuade => (VP/VP[to])/NP
     ''')

parser = chart.CCGChartParser(lex, chart.DefaultRuleSet)
for parse in parser.parse("you prefer that cake".split()):
    chart.printCCGDerivation(parse)
    break

for parse in parser.parse("that is the cake which you prefer".split()):
    chart.printCCGDerivation(parse)
    break
