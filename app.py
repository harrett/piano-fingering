from flask import Flask, render_template, request
import main_flow

tmp_path = 'static/tmp/tmp.mid'

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    midi = request.files['midifile']
    midi.save(tmp_path)
    fingering = main_flow.flow(tmp_path)
    fing_r = fingering[0]
    fing_l = 6 - fingering[1]
    return render_template('result.html', fing_r=fing_r, fing_l=fing_l)

if __name__ == '__main__':
    app.run(debug=True)