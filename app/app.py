# app/app.py
from flask import Flask, request, render_template, jsonify
from calculator import sqrt, factorial, ln, power

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/compute', methods=['POST'])
def compute():
    op = request.form.get('operation')
    try:
        if op == 'sqrt':
            x = request.form.get('x')
            result = sqrt(x)
        elif op == 'factorial':
            n = request.form.get('n')
            result = factorial(n)
        elif op == 'ln':
            x = request.form.get('x')
            result = ln(x)
        elif op == 'power':
            x = request.form.get('x')
            b = request.form.get('b')
            result = power(x, b)
        else:
            return jsonify({'error': 'unknown operation'}), 400
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



