from enum import Enum

class Tag(Enum):
   '''
   Uma representacao em constante de todos os nomes 
   de tokens para a linguagem.
   '''

   # Fim de arquivo
   EOF = -1

   # Palavras-chave
   KW_IF = 1
   KW_ELSE = 2
   KW_THEN = 3
   KW_PRINT = 4

   # Operadores 
   OP_MENOR = 10
   OP_MENOR_IGUAL = 11
   OP_MAIOR_IGUAL = 12
   OP_MAIOR = 13
   OP_IGUAL = 14
   OP_DIFERENTE = 15

   OP_ATRIB = 16

   # Simbolos
   SMB_PV = 17
   SMB_AC = 18
   SMB_FC = 19
    
   # Identificador
   ID = 20

   # Numeros
   NUM = 30

   # Constantes para tipos
   TIPO_VAZIO   = 1000
   TIPO_NUMERO  = 1001