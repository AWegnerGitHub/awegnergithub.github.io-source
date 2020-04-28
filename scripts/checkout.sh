git clone https://github.com/AWegnerGithub/awegnergithub.github.io-source.git source
mkdir source/content
rsync -av --progress ./* source/content --exclude source
cd source
pip install --upgrade pip
pip install -r requirements.txt
