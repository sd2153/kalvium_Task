from flask import Flask,render_template,jsonify
import re

app=Flask(__name__)

@app.route("/")
def home():
    return "Welcome to Maths Server"

@app.route("/<path:expression>", methods=['GET'])
def calculate(expression):
    expression = expression.replace("plus", "+").replace("minus", "-").replace("into", "*").replace("dividedby", "/").replace("power","**")
    tokens = expression.split('/')

    operands = []
    operators = []

    precedence = {"+": 1, "-": 1, "*": 2, "/": 2,"**":3}

    for token in tokens:
        if token.isdigit() or (token.startswith('-') and token[1:].isdigit()):
            operands.append(float(token))
        elif token in ["+", "-", "*", "/","**"]:
            while operators and precedence.get(operators[-1], 0) >= precedence.get(token, 0):
                operand2 = operands.pop()
                operand1 = operands.pop()
                operator = operators.pop()

                result = eval(str(operand1) + operator + str(operand2))
                operands.append(result)
            operators.append(token)
        else:
            return {"Invalid expression"}

    while operators:
        operand2 = operands.pop()
        operand1 = operands.pop()
        operator = operators.pop()

        result = eval(str(operand1) + operator + str(operand2))
        operands.append(result)

    question = expression
    answer = operands[-1]

    return {"question": question, "answer": answer}




if __name__=="__main__":
    app.run(host='0.0.0.0', debug=True)