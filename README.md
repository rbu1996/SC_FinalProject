# COVID-19 News Website
Software Carpentry Final Project 
Ride Bu

### System Requirements:
* Please check requirements.txt. 

### How to run?
* Run:
```python
python manage.py runserver
```
* Then you will see
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
May 06, 2020 - 15:07:18
Django version 3.0.5, using settings 'mysite.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
* Open url: [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser (I recommend Chrome here). 
* Successed! You can browse the COVID-19 News website now!

### How to use the website?
* Homepage:
You can enter any query in search bar. To get search results, please click 'submit' button. 
* Search Results Page:
Top 10 related news will be shown. You can click the title of news that you are interested in to read more. 
* News Page:
The news page shows news title, author, posted time, content body. You can visit news source website by clicking 'view source' botton. Also, in the right side of page, you can see other related news which has similar topics with your viewing one. 
* Related News:
You can read these related news by clicking their titles. 

### Algorithm
* Main functions and algorithm are in website/mysite/pools/views.py