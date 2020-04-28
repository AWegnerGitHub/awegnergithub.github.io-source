pip install pylinkvalidator
python -m pelican.server && cd - &
sleep 3
linkchecker http://localhost:8000
pgrep -f "^python -m pelican.server" | xargs kill -9
