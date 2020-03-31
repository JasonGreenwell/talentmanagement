import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask import Flask, request, redirect
from werkzeug import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = '/Uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


# This is the main page
@app.route('/')
def hello_world():
    return '''

    <Title> Kara Marszalek </Title>

    <Head> This is a matplotlib plot generated as a PNG image <Head> <br><br>

    <i> Will have to think up a way to auto refresh and auto generate new plots </i> <br><br>

    <form action = "http://localhost:5000/uploader" method = "POST" 
         enctype = "multipart/form-data">
         <input type = "file" name = "file" />
         <input type = "submit"/>
      </form>

    <img src="/plot.png" alt="my plot">

    '''


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return redirect("/", code=302)


# This is the png image generated from matplotlib
@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig


if __name__ == '__main__':
    app.run()