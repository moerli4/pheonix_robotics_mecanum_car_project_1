create venv: python -m venv .venv
source venv: source .venv/bin/activate
install requirements.txt: pip install -r requirements.txt 
( create requirements.txt: pip freeze > requirements.txt )
