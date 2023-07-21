import os
import subprocess
from typing import Union

from app.service.file_operator import FileOperator
from config import Config


class ScoreGenerator:
    """
    Provide interface to access lilypond functionality
    """

    def __init__(self, lilypond_path):
        self._lilypond_path = lilypond_path

    @staticmethod
    def load_default():
        """
        :return: ScoreGenerator instance with loaded default values
        """
        score_generator = ScoreGenerator(Config.lilypond_path)
        return score_generator

    def run(self,
            input_text: str,
            file_operator: FileOperator) -> Union[str, None]:
        """
        Writes text to file and runs lilypond to generate output pdf file
        file_operator needs to be initiated everytime this is called to get a unique timestamp for input/output tracking
        :param input_text: text received input UI input
        :param file_operator: FileOperator object that stores info and functions for specific file operations
        :return: output_filepath
        """
        file_operator.create_workdir()
        file_operator.write_text_to_file(input_text)
        os.chdir(file_operator.workdir)

        flags = []
        if file_operator.get_extension() == 'svg':
            flags.append('-dbackend=svg')
        elif file_operator.get_extension() == 'png':
            flags += ['-dtall-page-formats=png','-dresolution=750']

        lily_process = subprocess.run(['timeout', '5', self._lilypond_path] + flags + [file_operator.input_filepath])

        if file_operator.get_extension() == 'mp3':
            command = 'timidity {fname}.midi -Ow -o - | ffmpeg -i - {fname}.mp3'.format(fname = file_operator.get_base_file_name())
            subprocess.run(["bash", "-c", command])

        file_operator.remove_input_file()

        output_filepath = file_operator.get_output_filepath()
        if os.path.isfile(output_filepath) and lily_process.returncode == 0:
            output = output_filepath
        else:
            output = None

        return output
