create venv: python -m venv .venv
source venv: source .venv/bin/activate
install requirements.txt: pip install -r requirements.txt 
( create requirements.txt: pip freeze > requirements.txt )

clone the repo to the car with on ssh:
git clone https://github.com/moerli4/pheonix_robotics_mecanum_car_project_1.git
