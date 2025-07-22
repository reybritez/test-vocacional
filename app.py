from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'tu_super_clave_secreta_aqui_cambiala!' # ¡IMPORTANTE: Cambia esto por una clave secreta fuerte y única!

# Definición de las preguntas del test
# Cada pregunta tiene un texto, opciones y cómo esas opciones afectan los puntajes de las carreras.
questions = [
    {
        'id': 1,
        'pregunta': '¿Qué tipo de problemas te entusiasma más resolver?',
        'opciones': {
            'A': 'Diseñar y construir sistemas complejos o programas de computadora.',
            'B': 'Analizar argumentos, debatir ideas y buscar la justicia.',
            'C': 'Investigar enfermedades, cuidar pacientes o entender el cuerpo humano.'
        },
        'impacto_carrera': {
            'A': {'Ingenieria Informatica': 2, 'Derecho': 0, 'Medicina': 0},
            'B': {'Ingenieria Informatica': 0, 'Derecho': 2, 'Medicina': 0},
            'C': {'Ingenieria Informatica': 0, 'Derecho': 0, 'Medicina': 2}
        }
    },
    {
        'id': 2,
        'pregunta': 'Si tuvieras que elegir una materia para estudiar a fondo, ¿cuál sería?',
        'opciones': {
            'A': 'Algoritmos y estructuras de datos.',
            'B': 'Historia de las leyes y constitución.',
            'C': 'Biología molecular y anatomía.'
        },
        'impacto_carrera': {
            'A': {'Ingenieria Informatica': 2, 'Derecho': 0, 'Medicina': 0},
            'B': {'Ingenieria Informatica': 0, 'Derecho': 2, 'Medicina': 0},
            'C': {'Ingenieria Informatica': 0, 'Derecho': 0, 'Medicina': 2}
        }
    },
    {
        'id': 3,
        'pregunta': '¿Qué tipo de ambiente de trabajo prefieres?',
        'opciones': {
            'A': 'Un laboratorio de programación o una oficina tecnológica.',
            'B': 'Un tribunal, un bufete de abogados o una sala de mediación.',
            'C': 'Un hospital, una clínica o un centro de investigación médica.'
        },
        'impacto_carrera': {
            'A': {'Ingenieria Informatica': 1, 'Derecho': 0, 'Medicina': 0},
            'B': {'Ingenieria Informatica': 0, 'Derecho': 1, 'Medicina': 0},
            'C': {'Ingenieria Informatica': 0, 'Derecho': 0, 'Medicina': 1}
        }
    },
    {
        'id': 4,
        'pregunta': '¿Cómo te sentirías al trabajar con información muy detallada y precisa?',
        'opciones': {
            'A': 'Me encanta, especialmente si se trata de código o configuraciones.',
            'B': 'Es fundamental para asegurar la validez de un argumento o contrato.',
            'C': 'Crucial para diagnósticos y tratamientos correctos, me parece vital.'
        },
        'impacto_carrera': {
            'A': {'Ingenieria Informatica': 1, 'Derecho': 0, 'Medicina': 0},
            'B': {'Ingenieria Informatica': 0, 'Derecho': 1, 'Medicina': 0},
            'C': {'Ingenieria Informatica': 0, 'Derecho': 0, 'Medicina': 1}
        }
    },
    {
        'id': 5,
        'pregunta': '¿Qué te atrae más de ayudar a los demás?',
        'opciones': {
            'A': 'Crear herramientas o software que hagan la vida más fácil o eficiente.',
            'B': 'Defender los derechos de las personas o resolver disputas justas.',
            'C': 'Curar enfermedades, aliviar el sufrimiento o salvar vidas.'
        },
        'impacto_carrera': {
            'A': {'Ingenieria Informatica': 1, 'Derecho': 0, 'Medicina': 0},
            'B': {'Ingenieria Informatica': 0, 'Derecho': 1, 'Medicina': 0},
            'C': {'Ingenieria Informatica': 0, 'Derecho': 0, 'Medicina': 1}
        }
    }
]

@app.route('/')
def index():
    # Reiniciar el estado del test al visitar la página de inicio
    session['current_question_index'] = 0
    # Inicializar los puntajes para cada carrera
    session['scores'] = {
        'Ingenieria Informatica': 0,
        'Derecho': 0,
        'Medicina': 0
    }
    return render_template('index.html')

@app.route('/test', methods=['GET', 'POST'])
def test():
    if 'current_question_index' not in session:
        return redirect(url_for('index')) # Redirigir si no hay un test en progreso

    current_question_index = session.get('current_question_index')
    scores = session.get('scores')

    if request.method == 'POST':
        selected_option = request.form.get('option')
        if selected_option:
            current_question = questions[current_question_index]
            # Actualizar los puntajes basados en la opción seleccionada
            for carrera, puntos in current_question['impacto_carrera'].get(selected_option, {}).items():
                scores[carrera] += puntos

            session['scores'] = scores
            session['current_question_index'] += 1
            return redirect(url_for('test'))
        else:
            # Si el usuario no selecciona una opción, puedes mostrar un mensaje de error
            # o simplemente volver a la misma pregunta. Por simplicidad, aquí se vuelve a la pregunta.
            pass

    if current_question_index < len(questions):
        question = questions[current_question_index]
        return render_template('questions.html', question=question, question_number=current_question_index + 1, total_questions=len(questions))
    else:
        # Si todas las preguntas han sido respondidas, ir a la página de resultados
        return redirect(url_for('result'))

@app.route('/result')
def result():
    scores = session.get('scores', {})
    if not scores or sum(scores.values()) == 0:
        return redirect(url_for('index')) # Redirigir si no hay puntajes válidos

    # Determinar la carrera con el puntaje más alto
    recommended_career = max(scores, key=scores.get)

    return render_template('result.html', scores=scores, recommended_career=recommended_career)

if __name__ == '__main__':
    app.run(debug=True) # En producción, cambia debug=False