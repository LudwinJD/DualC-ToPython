grammar Programa;

programa : programaPrincipal sentencia+ EOF;

programaPrincipal : sentenciaInclude 'int' 'main' '(' ')' bloque;

sentencia : sentenciaCout
          | sentenciaIf
          | declaracionVariable
          | sentenciaInput
          | sentenciaReturn
          | sentenciaInclude
          | sentenciaFor;

sentenciaCout : 'std' '::' 'cout' '<<' CADENA ('<<' 'std' '::' 'endl' ';' | ';')
              | 'std' '::' 'cout' '<<' CADENA ';'
              | 'std' '::' 'cout' '<<' expresion ';'
              | 'std' '::' 'cout' '<<' CADENA '<<' expresion ('<<' 'std' '::' 'endl' ';' | ';')
              | 'std' '::' 'cout' '<<' expresion ('<<' 'std' '::' 'endl' ';' | ';');

sentenciaIf : 'if' '(' expresion ')' bloque (sentenciaElse)?;
sentenciaElse : 'else' bloque;

declaracionVariable : tipo ID ('=' expresion)? ';'
                   | tipo ID '=' expresion ';'
                   | tipo ID '(' ')' bloque
                   | tipo ID '(' ')' bloqueElse
                   | tipo ID '(' ')' bloqueIf
                   | tipo ID ';';

sentenciaInput : 'std' '::' 'cin' '>>' ID ';';

sentenciaReturn : 'return' expresion ';';

sentenciaInclude : '#' 'include' '<' ID '>';

sentenciaFor : 'for' '(' declaracionVariable expresion ';' expresion ')' bloque
             | 'for' '(' declaracionVariable expresion ';' declaracionVariable ')' bloque
             | 'for' '(' expresion ';' expresion ';' expresion ')' bloque
             | 'for' '(' ';' expresion ';' expresion ')' bloque;

bloque : '{' sentencia* '}';
bloqueElse : '{' sentencia* '}';
bloqueIf : '{' sentencia* '}';

expresion : ID
           | INT
           | FLOAT
           | DOUBLE
           | CADENA
           | 'true'
           | 'false'
           | expresion ('+'|'-'|'*'|'/') expresion
           | '(' expresion ')'
           | expresion ('>'|'<'|'>='|'<='|'=='|'!=') expresion
           | expresion '?' expresion ':' expresion
           | '+''+'ID
           | ID'+''+'
           | '-' expresion;

tipo : 'int' | 'float' | 'double' | 'bool' | 'string';

ID : [a-zA-Z_][a-zA-Z0-9_]*;
INT : [0-9]+;
FLOAT : [0-9]+ ('.' [0-9]*)? ('e' [+\-]? [0-9]+)?;
DOUBLE : [0-9]+ ('.' [0-9]*)? 'e' [+\-]? [0-9]+;
CADENA : '"' (('\\' '"') | ~('\n'|'"'))* '"';
WS : [ \t\r\n]+ -> skip;
COMMENT : '//' ~[\r\n]* -> skip;
