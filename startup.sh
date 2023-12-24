pip3 install bs4==0.0.1
pip3 install dash==2.14.1
pip3 install dash-table==5.0.0
pip3 install Flask>=2.2.2
pip3 install numpy==1.18.0
pip3 install pandas==1.0.4
pip3 install requests==2.12.4
#python application.py
gunicorn --bind=0.0.0.0 --timeout 600 application:app
