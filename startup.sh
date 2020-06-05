pip3 install bs4==0.0.1
pip3 install dash==1.12.0
pip3 install dash-table==4.7.0
pip3 install Flask==1.1.2
pip3 install numpy==1.18.0
pip3 install pandas==1.0.4
pip3 install requests==2.12.4
gunicorn --bind=0.0.0.0 --timeout 600 application:app