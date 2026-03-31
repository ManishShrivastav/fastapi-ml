from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        number = int(request.form['number'])
        table = [(number, i, number * i) for i in range(1, 11)]
        return render_template('result.html', number=number, table=table)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)