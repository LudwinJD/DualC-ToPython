from antlr4 import *
from ProgramaLexer import ProgramaLexer
from ProgramaParser import ProgramaParser
from ProgramaListener import ProgramaListener
from antlr4 import FileStream, CommonTokenStream, RecognitionException, ParseTreeWalker
from antlr4.error.ErrorListener import ConsoleErrorListener

class ProgramaToPythonConverter(ProgramaListener):
    def __init__(self):
        self.output_lines = []
        self.indentation_level = 0
        self.inside_main = False 
        self.analysis_successful = True 
        self.inside_for = False   

    def enterProgramaPrincipal(self, ctx):
        self.inside_main = True
        self.output_lines.append(self.indent() + "def main():")
        self.indentation_level += 1

    def enterSentenciaCout(self, ctx):
        cadena_context = ctx.CADENA()

        if cadena_context:
            cadena = cadena_context.getText()
        else:
            cadena = ''

        expresiones = ctx.expresion()

        if expresiones and isinstance(expresiones, list):
            # Hay expresiones aparte de la cadena
            expresion_texts = [expresion.getText() for expresion in expresiones]
            converted_code = f'print({cadena}, {", ".join(expresion_texts)})'
        elif expresiones:
            # Solo hay una expresión aparte de la cadena
            converted_code = f'print({cadena}, {expresiones.getText()})'
        elif cadena:
            # Solo hay una cadena
            converted_code = f'print({cadena})'
        else:
            # No hay ni cadena ni expresiones
            converted_code = 'print()'

        self.output_lines.append(self.indent() + converted_code)

    def enterSentenciaIf(self, ctx):
        condition = ctx.expresion().getText()
        self.output_lines.append(self.indent() + f'if {condition}:')
        #self.indentation_level += 1
        self.indentation_level += 1
        self.inside_if = True

    def enterSentenciaElse(self, ctx):
        self.indentation_level -= 1
        self.output_lines.append(self.indent() + 'else:')
        self.indentation_level += 1
        #print(ctx.bloque().getText())
   
    def exitSentenciaElse(self, ctx):
        self.indentation_level -= 1
        self.inside_else = False   

    def enterSentenciaFor(self, ctx):
        self.inside_for = True  # Establecer la bandera cuando entramos en un bucle for
        declaraciones_variables = ctx.declaracionVariable()
        variable_name = declaraciones_variables[0].ID().getText()

        condition = ctx.expresion(0).getText()
        condition_value = condition.split('<')[1].strip()  # Obtener el número después del signo menor
        self.output_lines.append(self.indent() + f'for {variable_name} in range({condition_value}):')
        self.indentation_level += 1

    def exitSentenciaFor(self, ctx):
        self.indentation_level -= 1
        self.inside_for = False  # Restablecer la bandera cuando salimos del bucle for


    def enterDeclaracionVariable(self, ctx):
        if not self.inside_for:  # Verificar si no estamos dentro de un bucle for
            variable_name = ctx.ID().getText()
            initialization = ''
            if ctx.expresion():
                initialization = f' = {ctx.expresion().getText()}'
            self.output_lines.append(self.indent() + f'{variable_name}{initialization}')

    def exitPrograma(self, ctx):
        self.indentation_level -= 1
        if self.inside_main:
            #self.indentation_level -= 2
            self.output_lines.append(self.indent() + "if __name__ == '__main__':")
            #self.indentation_level -= 2
            self.output_lines.append(self.indent() + "    main()")

    def enterOtherStatement(self, ctx):
        self.output_lines.append(self.indent() + f'{ctx.getText()}')

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            f.write('\n'.join(self.output_lines))

    def indent(self):
        return '    ' * self.indentation_level

class MyErrorListener(ConsoleErrorListener):
    def __init__(self):
        super().__init__()
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        super().syntaxError(recognizer, offendingSymbol, line, column, msg, e)
        if msg != "mismatched input '<EOF>' expecting {'int', 'std', 'if', 'return', '#', 'for', 'float', 'double', 'bool', 'string'}":
            # Solo agregar errores que no sean relacionados con '<EOF>'
            self.errors.append({
                'line': line,
                'column': column,
                'msg': msg
            })

# En tu script principal
input_file = "entrada.cpp"
output_file = "salida3.py"

def main():
    input_stream = FileStream(input_file, encoding='utf-8')
    lexer = ProgramaLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = ProgramaParser(token_stream) 
    
    # Agregar el listener de errores léxicos personalizado
    error_listener_lexico = MyErrorListener()
    lexer.removeErrorListeners()
    lexer.addErrorListener(error_listener_lexico)

    # Agregar el listener de errores sintácticos personalizado
    error_listener = MyErrorListener()
    lexer.removeErrorListeners()
    lexer.addErrorListener(error_listener)
    parser.removeErrorListeners()
    parser.addErrorListener(error_listener)

    tree = parser.programa()

    converter = ProgramaToPythonConverter()
    walker = ParseTreeWalker()
    walker.walk(converter, tree)
    converter.save_to_file(output_file)

   

    # Solo imprimir el árbol si no hubo errores
    if parser.getNumberOfSyntaxErrors() <= 1:
        print(tree.toStringTree(recog=parser))

        try:
            # Solo escribir en el archivo si no hubo errores
            if parser.getNumberOfSyntaxErrors() <= 1:
                with open(output_file, 'w') as f:
                    f.write('\n'.join(converter.output_lines))

        except RecognitionException as e:
            # Captura errores específicos de reconocimiento
            print(f"Error de reconocimiento: {e}")
        except Exception as e:
            # Captura cualquier otra excepción durante el análisis
            print(f"Excepcion durante el análisis: {e}")
    else:
        print("El analisis sintáctico contiene errores.")
        with open(output_file, 'w') as f:
            f.truncate(0)
            # Imprimir información del error en el archivo
            for error in error_listener.errors:
                error_message = f"Error de Sintaxis en la linea {error['line']}, columna {error['column']}"
                print(error_message)
                f.write(f"print('{error_message}')\n")
            
if __name__ == '__main__':
    main()
