import sys
import copy

from tag import Tag
from token_1 import Token
from lexer import Lexer
from no import No

class Parser():

   def __init__(self, lexer):
      self.lexer = lexer
      self.token = lexer.proxToken() # Leitura inicial obrigatoria do primeiro simbolo
      if self.token is None: # erro no Lexer
        sys.exit(0)

   def sinalizaErroSintatico(self, message):
      print("[Erro Sintatico] na linha " + str(self.token.getLinha()) + " e coluna " + str(self.token.getColuna()) + ": ")
      print(message, "\n")
      sys.exit(0)

   def sinalizaErroSemantico(self, message):
      print("[Erro Semantico] na linha " + str(self.token.getLinha()) + " e coluna " + str(self.token.getColuna()) + ": ")
      print(message, "\n")
      sys.exit(0)

   def advance(self):
      print("[DEBUG] token: ", self.token.toString(full_print=False))
      self.token = self.lexer.proxToken()
      if self.token is None: # erro no Lexer
        sys.exit(0)

   # verifica token esperado t 
   def eat(self, t):
      if(self.token.getNome() == t):
         self.advance()
         return True
      else:
         return False

   """
   ATENCAO:
   A verificacao semantica acontece junto as producoes
   gramaticais em:
   (1) CMD   --> print T;
   (2) ATRIB --> id = T;
   (3) T     --> id
   (4) T     --> num
   As regras e acoes semanticas estao na descricao do exercicio.
   Procure pelas marcacoes 'TODO' para saber o que e onde 
   complementar com codigo. 
   """

   # Programa -> CMD EOF
   def Programa(self):
      self.Cmd()
      if(self.token.getNome() != Tag.EOF):
         self.sinalizaErroSintatico("Esperado \"EOF\"; encontrado " + "\"" + self.token.getLexema() + "\"")

         
   def Cmd(self):
      # Cmd -> if E then { CMD } CMD’
      if(self.eat(Tag.KW_IF)): 
         self.E()
         if(not self.eat(Tag.KW_THEN)):
            self.sinalizaErroSintatico("Esperado \"then\", encontrado " + "\"" + self.token.getLexema() + "\"")
         if(not self.eat(Tag.SMB_AC)):
            self.sinalizaErroSintatico("Esperado \"{\", encontrado " + "\"" + self.token.getLexema() + "\"")
         self.Cmd()
         if(not self.eat(Tag.SMB_FC)):
            self.sinalizaErroSintatico("Esperado \"}\", encontrado " + "\"" + self.token.getLexema() + "\"")
         self.CmdLinha()
      # Cmd -> print T;
      elif(self.eat(Tag.KW_PRINT)):
        # verificacao semantica
        '''
        TODO: Apos expandir T, valide o tipo de T, conforme a regra semantica.
        '''
        noT = self.T()
        # COMPLETE AQUI A VALIDACAO SEMANTICA
        
        if (noT.tipo == Tag.TIPO_VAZIO):
            print("variável não declarada")

        if(not self.eat(Tag.SMB_PV)):
            self.sinalizaErroSintatico("Esperado \";\", encontrado " + "\"" + self.token.getLexema() + "\"")

      # Cmd -> ATRIB CMD
      else:
         self.Atrib()
         self.Cmd()

         
   def CmdLinha(self):
      # CmdLinha -> else { CMD }
      if(self.eat(Tag.KW_ELSE)):
         if(not self.eat(Tag.SMB_AC)):
            self.sinalizaErroSintatico("Esperado \"{\", encontrado " + "\"" + self.token.getLexema() + "\"")
         self.Cmd()
         if(not self.eat(Tag.SMB_FC)):
            self.sinalizaErroSintatico("Esperado \"}\", encontrado " + "\"" + self.token.getLexema() + "\"")
      # CmdLinha -> epsilon
      else:
         return

      
   # Atrib -> id = T;
   def Atrib(self):
      # Armazena copia do token corrente, uma vez que o ID pode ser consumido.
      # Util para usar na verificacao semantica.
      tempToken = copy.copy(self.token)

      '''
        TODO: Apos expandir T, o ID deve ter o seu tipo
         configurado para o mesmo tipo do no T, conforme a regra semantica.
      '''
      # print('========= Linha 119 ========')
      # print(self.token.getLexema())
      if (self.token.getLexema()):
         self.token.setTipo(Tag.TIPO_NUMERO)
      if(self.eat(Tag.ID)):
         if(not self.eat(Tag.OP_ATRIB)):
            self.sinalizaErroSintatico("Esperado \"=\", encontrado " + "\"" + self.token.getLexema() + "\"")
         
         # verificacao semantica
         noT = self.T()

         # COMPLETE AQUI A VALIDACAO SEMANTICA
         # if (noT.tipo == Tag.TIPO_VAZIO):
         #    self.token.setTipo(noT.tipo)
         #    tempToken.setTipo(noT.tipo)
         # else:
         #    print("erro: variavel nao declarada antes de atribuição")
               
         if(not self.eat(Tag.SMB_PV)):
            self.sinalizaErroSintatico("Esperado \";\", encontrado " + "\"" + self.token.getLexema() + "\"")
      else:
         self.sinalizaErroSintatico("Esperado \"id\", encontrado " + "\"" + self.token.getLexema() + "\"")

         
   # E -> T E'
   def E(self):
      self.T()
      self.ELinha()

      
   def ELinha(self):
      # E' -> OP T
      if(self.token.getNome() == Tag.OP_MAIOR or self.token.getNome() == Tag.OP_MENOR or
         self.token.getNome() == Tag.OP_MAIOR_IGUAL or self.token.getNome() == Tag.OP_MENOR_IGUAL or
         self.token.getNome() == Tag.OP_IGUAL or self.token.getNome() == Tag.OP_DIFERENTE):
            self.Op()
            self.T()
      # E' ->  epsilon
      else:
         return

      
   # Op -> ">" | "<" | ">=" | "<=" | "==" | "!="
   def Op(self):
      if(not(
         self.eat(Tag.OP_MAIOR) or self.eat(Tag.OP_MENOR) or self.eat(Tag.OP_MAIOR_IGUAL) or 
         self.eat(Tag.OP_MENOR_IGUAL) or self.eat(Tag.OP_IGUAL) or self.eat(Tag.OP_DIFERENTE))):
            self.sinalizaErroSintatico("Esperado \">, <, >=, <=, ==, !=\", encontrado " + "\"" + self.token.getLexema() + "\"")

            
   # T -> id | num
   def T(self):
      noT = No()

      # armazena token corrente, uma vez que o ID pode ser consumido
      tempToken = copy.copy(self.token)

      if(self.eat(Tag.ID)):
          noT.tipo = tempToken.getTipo()
      elif(self.eat(Tag.NUM)):
        noT.tipo = Tag.TIPO_NUMERO
      else:
         self.sinalizaErroSintatico("Esperado \"numero, id\", encontrado "  + "\"" + self.token.getLexema() + "\"")

      return noT