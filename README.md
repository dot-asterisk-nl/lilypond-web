# Lilypond Web Service
- Lightweight service that runs simple webpage to access Lilypond functionalities
- Based on [chilledgeek/lilypond-web](https://www.github.com/chilledgeek/lilypond-web)
- Default port is set to 8080, no further configuration is necessary/possible

# How to use
- Ensure Docker is installed
- Run ```docker build -t lilypond-web .; docker run --rm -p 8080:8080 lilypond-web```
- Enjoy and paste in some lily code! Or don't lol. Please be responsible with Lilypond security, the [documentation](https://lilypond.org/doc/v2.22/Documentation/usage/command_002dline-usage#advanced-command-line-options-for-lilypond) has plenty of information about that.
