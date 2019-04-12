from flask import Flask, render_template, request

from countdown import Letters

app = Flask(__name__)


@app.route('/word_lookup', methods=['GET', 'POST'])
def word_search():
    return render_template('letter_input.html')


@app.route('/words_result', methods=['GET', 'POST'])
def word_results():
    letter_call = Letters()
    if request.method == 'POST':
        letters = [request.form.get('letter1'), request.form.get('letter2'), request.form.get('letter3'),
                   request.form.get('letter4'), request.form.get('letter5'), request.form.get('letter6'),
                   request.form.get('letter7'), request.form.get('letter8'), request.form.get('letter9')]

        result = letter_call.word_find(letters, with_definition=True)

        word_data = result['words']

        return render_template('result.html', runtime=result['runtime'], limit=len(result['words']),
                               perm_count=result['permutations'], word_data=word_data)
