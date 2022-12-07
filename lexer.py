import sys

from ts import TS
from tag import Tag
from token_1 import Token

class Lexer():

   def __init__(self, input_file):
      try:
         self.input_file = open(input_file, 'rb')
         self.lookahead = 0
         self.n_line = 1
         self.n_column = 1
         self.ts = TS()
      except IOError:
         print('Erro de abertura do arquivo. Encerrando.')
         sys.exit(0)

   def closeFile(self):
      try:
         self.input_file.close()
      except IOError:
         print('Erro ao fechar arquivo. Encerrando.')
         sys.exit(0)

   def sinalizaErroLexico(self, message):
      print("[Erro Lexico]: ", message, "\n");

   def retornaPonteiro(self):
      '''Metodo importante para retornar a leitura no arquivo,
      uma posicao, ja que um caractere foi lido indicando fim
      de um lexema, porem indicando tambem o inicio de outro
      lexema. Isso esta evidente no AFD na leitura de 'outro'.
      '''
      if(self.lookahead.decode('ascii') != ''):
         self.input_file.seek(self.input_file.tell()-1)
         self.n_column -= 1

   def printTS(self):
      self.ts.printTS()

   def proxToken(self):
      # Implementa um AFD.
      
      estado = 1
      lexema = ""
      # c = '\u0000'

      while(True):
         self.lookahead = self.input_file.read(1)
         c = self.lookahead.decode('ascii')
         self.n_column += 1

         if(estado == 1):
            if(c == ''):
               return Token(Tag.EOF, "EOF", self.n_line, self.n_column)
            elif(c == ' ' or c == '\t' or c == '\n'):
               estado = 1
               if(c == '\n'): 
                  self.n_line += 1
                  self.n_column = 1
               #nao fiz tratamento de \tab
            elif(c == '='):
               estado = 2
            elif(c == '!'):
               estado = 4
            elif(c == '<'):
               estado = 6
            elif(c == '>'):
               estado = 9
            elif(c.isdigit()):
               lexema += c
               estado = 12
            elif(c.isalpha()):
               lexema += c
               estado = 14
            elif(c == '/'):
               estado = 16
            elif(c == ';'):
               return Token(Tag.SMB_PV, ";", self.n_line, self.n_column)
            elif(c == '{'):
               return Token(Tag.SMB_AC, "{", self.n_line, self.n_column)
            elif(c == '}'):
               return Token(Tag.SMB_FC, "}", self.n_line, self.n_column)
            else:
               self.sinalizaErroLexico("Caractere invalido [" + c + "] na linha " +
               str(self.n_line) + " e coluna " + str(self.n_column))
               return None
         elif(estado == 2):
            if(c == '='):
               return Token(Tag.OP_IGUAL, "==", self.n_line, self.n_column)
               
            self.retornaPonteiro()
            return Token(Tag.OP_ATRIB, "=", self.n_line, self.n_column)
         elif(estado == 4):
            if(c == '='):
               return Token(Tag.OP_DIFERENTE, "!=", self.n_line, self.n_column)

            self.sinalizaErroLexico("Caractere invalido [" + c + "] na linha " +
            str(self.n_line) + " e coluna " + str(self.n_column))
            return None
         elif(estado == 6):
            if(c == '='):
               return Token(Tag.OP_MENOR_IGUAL, "<=", self.n_line, self.n_column)

            self.retornaPonteiro()
            return Token(Tag.OP_MENOR, "<", self.n_line, self.n_column)
         elif(estado == 9):
            if(c == '='):
               return Token(Tag.OP_MAIOR_IGUAL, ">=", self.n_line, self.n_column)

            self.retornaPonteiro()
            return Token(Tag.OP_MAIOR, ">", self.n_line, self.n_column)
         elif(estado == 12):
            if(c.isdigit()):
               lexema += c           
            else:
               self.retornaPonteiro()
               return Token(Tag.NUM, lexema, self.n_line, self.n_column)
         elif(estado == 14):
            if(c.isalnum()):
               lexema += c
            else:
               self.retornaPonteiro()
               token = self.ts.getToken(lexema)

               if(token is None):
                  token = Token(Tag.ID, lexema, self.n_line, self.n_column)
                  self.ts.addToken(lexema, token)
               else:
                  # atualiza linha e coluna do token que ja esta na TS
                  token.setLinha(self.n_line)
                  token.setColuna(self.n_column)
                  self.ts.addToken(lexema, token)

               return token
         # fim if's de estados
      # fim while
