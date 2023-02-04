from flask import Flask, request, render_template, send_file

from app.service.file_operator import FileOperator
from app.service.score_generator import ScoreGenerator

app = Flask(__name__)
app.config.from_object(__name__)

_score_generator = ScoreGenerator.load_default()

supported_extensions=['pdf', 'svg', 'midi']

@app.route('/')
def landing_page():
    return render_template("home.html")


@app.route('/', methods=['POST'])
def form_post(score_generator: ScoreGenerator = _score_generator,
              file_operator_factory: FileOperator = FileOperator):
    text = request.form['lilypond_text']
    extension = request.form['extension']

    file_operator_instance = file_operator_factory.load_default()
    
    if extension in supported_extensions:
        #why yes I am in fact paranoid
        extension = supported_extensions[supported_extensions.index(extension)]
    else:
        extension = supported_extensions[0];

    file_operator_instance.set_extension(extension)
    output_filepath = score_generator.run(text, file_operator_instance)

    if output_filepath is None:
        return '''
        Something went wrong, as the requested file does not exist. Please check the following:
        <ul>
            <li>Does the lilypond code compile properly?</li>
            <li>Is <i>layout</i> and/or <i>midi</i> included?</li>
            <li>If not using the web interface, is your filetype supported?</li>
        </ul>
        ''' + "Supported extensions: " + ','.join(str(e) for e in supported_extensions);
    else:
        return send_file(output_filepath,
                         #attachment_filename=output_filepath.split("/")[-1],
                         conditional=True)


if __name__ == "__main__":
    app.run(port=8080,
            host="0.0.0.0")
