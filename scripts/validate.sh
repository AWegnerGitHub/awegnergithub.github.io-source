pip install pylinkvalidator
python -m pelican.server && cd - &
sleep 3
pylinkvalidate.py -P http://localhost:8000
pgrep -f "^python -m pelican.server" | xargs kill -9
