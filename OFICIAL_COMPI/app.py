from flask import Flask, render_template, jsonify, request, send_file
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index.html')
def index_cpp():
    return render_template('index.html')

@app.route('/indexP.html')
def index_python():
    return render_template('indexP.html')

@app.route('/guardar_codigo_cpp', methods=['POST'])
def guardar_codigo_cpp():
    data = request.get_json()
    codigo = data.get('codigo', '')
    with open('entrada.cpp', 'w', encoding='utf-8') as f:
        f.write(codigo)
    return jsonify({'mensaje': 'Código guardado correctamente'})

@app.route('/guardar_codigo_py', methods=['POST'])
def guardar_codigo_py():
    data = request.get_json()
    codigo = data.get('codigo', '')
    with open('salida.py', 'w', encoding='utf-8') as f:
        f.write(codigo)
    return jsonify({'mensaje': 'Código guardado correctamente'})

@app.route('/ejecutar_cpp_a_python')
def ejecutar_cpp_a_python():
    resultado = subprocess.check_output(['python', 'OFICIAL.C++_A_PYTHON.PY'], universal_newlines=True)
    return jsonify({'resultado': resultado})

@app.route('/ejecutar_python_a_cpp')
def ejecutar_python_a_cpp():
    resultado = subprocess.check_output(['python', 'ANALISADOR_PYTHON_A_C++.py'], universal_newlines=True)
    return jsonify({'resultado': resultado})

@app.route('/obtener_salida_cpp_a_python')
def obtener_salida_cpp_a_python():
    try:
        with open('salida3.py', 'r', encoding='utf-8') as f:
            contenido = f.read()
        return jsonify({'codigoSalida': contenido})
    except FileNotFoundError:
        return jsonify({'codigoSalida': 'Archivo salida3.py no encontrado'})
    
@app.route('/obtener_salida_python_a_cpp')
def obtener_salida_python_a_cpp():
    try:
        with open('salida.py', 'r', encoding='utf-8') as f:
            contenido = f.read()
        return jsonify({'codigoSalida': contenido})
    except FileNotFoundError:
        return jsonify({'codigoSalida': 'Archivo salida3.py no encontrado'})

@app.route('/leer_archivo_cpp', methods=['POST'])
def leer_archivo_cpp():
    try:
        archivo_cargado = request.files['fileInput']
        
        # Verificar si se proporcionó el archivo y tiene una extensión permitida
        if archivo_cargado and allowed_file(archivo_cargado.filename):
            contenido = archivo_cargado.read().decode('utf-8')
            return jsonify({'mensaje': 'Archivo leído correctamente', 'contenido': contenido})
        else:
            return jsonify({'mensaje': 'Archivo no válido o no proporcionado'})
    except Exception as e:
        return jsonify({'mensaje': f'Error al leer el archivo: {str(e)}'})

# Función auxiliar para verificar si el archivo tiene una extensión permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'txt', 'py', 'cpp'}

@app.route('/leer_archivo_python', methods=['POST'])
def leer_archivo_python():
    try:
        archivo_cargado = request.files['fileInput']
        
        # Verificar si se proporcionó el archivo y tiene una extensión permitida
        if archivo_cargado and allowed_file(archivo_cargado.filename):
            contenido = archivo_cargado.read().decode('utf-8')
            return jsonify({'mensaje': 'Archivo leído correctamente', 'contenido': contenido})
        else:
            return jsonify({'mensaje': 'Archivo no válido o no proporcionado'})
    except Exception as e:
        return jsonify({'mensaje': f'Error al leer el archivo: {str(e)}'})

# Función auxiliar para verificar si el archivo tiene una extensión permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'txt', 'py', 'cpp'}

if __name__ == '__main__':
    app.run(debug=True)
