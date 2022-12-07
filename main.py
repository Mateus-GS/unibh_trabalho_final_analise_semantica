from tag import Tag
from token_1 import Token
from lexer import Lexer
from parser_1 import Parser

'''
Esse eh o programa principal. Basta executa-lo.
'''

if __name__ == "__main__":
   lexer = Lexer('prog1.txt')

   parser = Parser(lexer)

   parser.Programa()

   print("\n=>Tabela de simbolos:")
   lexer.printTS()
   lexer.closeFile()
    
   print('\n=> Fim da compilacao')
