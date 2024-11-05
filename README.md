
### Set up

Depois de criar um env e executar `pip install -r requirements.txt` :

`pre-commit install`

`pre-commit run --all-files`

Ao executar pre-commit install, sempre, antes de um commit ser confirmado, serão executados os tests, um linter e um formatador, e o commit só passará se todos retornarem "passed".
