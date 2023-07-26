from flask import Flask, request, render_template, send_file, after_this_request, make_response
from flask_cors import CORS
from waitress import serve

from app.service.file_operator import FileOperator
from app.service.score_generator import ScoreGenerator, LilypondException, TimidityException

from config import Config

app = Flask(__name__)
CORS(app)
app.config.from_object(__name__)

_score_generator = ScoreGenerator.load_default()


@app.route('/')
def landing_page():
    return render_template("home.html")


@app.route('/', methods=['POST'])
def form_post(score_generator: ScoreGenerator = _score_generator,
              file_operator_factory: FileOperator = FileOperator):
    text = request.form['lilypond_text']
    extension = request.form['extension']

    file_operator_instance = file_operator_factory.load_default()

    if extension in Config.supported_extensions:
        # why yes I am in fact paranoid
        extension = Config.supported_extensions[Config.supported_extensions.index(extension)]
    else:
        extension = Config.supported_extensions[0]

    file_operator_instance.set_extension(extension)
    @after_this_request
    def delete_file(response):
        try:
            #file_operator_instance.clean_up()
            return response
        except Exception as ex:
            print(ex)
            return response

    try:
        output_filepath = score_generator.run(text, file_operator_instance)
        return send_file(output_filepath, conditional=True)
    except LilypondException as e:
        response = make_response(str(e), 400)
        response.headers.add_header("X-Error-Type", "LilypondException")
        response.mimetype = "text/plain"
        return response
    except TimidityException as e:
        response = make_response(str(e), 400)
        response.headers.add_header("X-Error-Type", "TimidityException")
        response.mimetype = "text/plain"
        return response


if __name__ == "__main__":
    serve(app, port=8080, host="0.0.0.0")
