from flask import Flask, render_template, jsonify
import re
app = Flask(__name__)

    
operation_history = []
def storing_history():
    try:
        with open("operation_history.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split("|")
                if len(parts) == 2:
                    question, answer = parts
                    operation_history.append({"question": question, "answer": float(answer)})
    except FileNotFoundError:
        pass
storing_history()
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/<path:expression>", methods=['GET'])
def calculate(expression):
    expression=expression.replace("/"," ")
    expression = expression.replace("plus", "+").replace("minus", "-").replace("into", "*").replace("dividedby", "/").replace("power", "**")
    tokens = expression.split()

    operands = []
    operators = []

    precedence = {"+": 1, "-": 1, "*": 2, "/": 2, "**": 3}

    for token in tokens:
        if token.isdigit() or (token.startswith('-') and token[1:].isdigit()):
            operands.append(float(token))
        elif token in ["+", "-", "*", "/", "**"]:
            while operators and precedence.get(operators[-1], 0) >= precedence.get(token, 0):
                operand2 = operands.pop()
                operand1 = operands.pop()
                operator = operators.pop()

                result = eval(str(operand1) + operator + str(operand2))
                operands.append(result)
            operators.append(token)
        else:
            return jsonify({"error":"Invalid"})

    while operators:
        operand2 = operands.pop()
        operand1 = operands.pop()
        operator = operators.pop()

        result = eval(str(operand1) + operator + str(operand2))
        operands.append(result)

    question = expression
    answer = operands[-1]

    operation_history.append({"question": question, "answer": answer})
    with open("operation_history.txt", "a") as file:
        file.write(f"{question}|{answer}\n")
        if len(operation_history) > 20:
            operation_history.pop(0)

    return jsonify({"question": question, "answer": answer})

@app.route("/history")
def history():
    return jsonify(operation_history)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
