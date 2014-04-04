'''
Created on Apr 3, 2014

@author: I028663
'''

from mako.template import Template

def generateHTMLOutput(predictions, date):
    tpl_params = []
    for symbol in predictions:
        if predictions[symbol] == 1:
            tpl_params.append({'str':symbol, 'up': True})
        else:
            tpl_params.append({'str':symbol, 'up': False})
    print Template(filename = "trend_tpl.txt" ).render(predictions=tpl_params, date = date)

if __name__ == '__main__':
    predictions = {
                   'SOFIX': 1,
                   '3JR': -1
                   }
    generateHTMLOutput(predictions, date = '31 05 2014')
    
