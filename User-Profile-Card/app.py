from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/profile', methods=['POST'])
def profile():

    name = request.form['name']
    bio = request.form['bio']
    image = request.form['image']

    return render_template(
        'index.html',
        name=name,
        bio=bio,
        image=image
    )

if __name__ == '__main__':
    app.run(debug=True)