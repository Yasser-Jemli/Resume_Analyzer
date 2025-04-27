python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

export FLASK_APP=src.app
export FLASK_ENV=development
export PYTHONPATH=$PYTHONPATH:$(pwd)

echo "Testing DB connection ***************"
python3 src/tests/test_db.py


echo "running the app "
flask run