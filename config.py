import os


class Config:
    workdir = "/workdir" if os.getenv("WORKDIR") is None else os.environ[
        "WORKDIR"]
    lilypond_path = "/lilypond/bin/lilypond" if os.getenv("LILYPOND_PATH") is None else os.environ[
        "LILYPOND_PATH"]
    supported_extensions=['pdf', 'svg', 'midi', 'png']
