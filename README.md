


#### Background

I have created a basic Django site with data as- small dataset of users (in 'data/userdata.csv') and their electricity consumption (in 'data/consumption/{user_id}.csv').
This application has following features :

* Components to read and store user data and consumption data
  	* This can be executed by running 'python manage.py import' in the terminal
* 'summary' view :
	* Line Chart to display total consumption for all users in given date range
	* If you click on a perticular point, a pop up screen will display top users, area and tariff wise counsumption			
	* A table listing all users with consumption details
* 'Detail' view	:
	* A line chart showing the consumption of an individual consumer, and a list of fields such as tariff, area, etc
	
sample urs to get data :

http://localhost:8000/detail/?start_date=2016-08-12&end_date=2016-08-20&user_id=3002

http://localhost:8000/?start_date=2016-08-12&end_date=2016-08-20

or 

http://localhost:8000/summary/?start_date=2016-08-12&end_date=2016-08-20

(shared screen captures of web pages-graphs)


![alt text](https://github.com/kul-amr/sample_project_Django/blob/master/summary_popup.png)


![alt text](https://github.com/kul-amr/sample_project_Django/blob/master/summary_screen.png)


![alt text](https://github.com/kul-amr/sample_project_Django/blob/master/detail_screen.png)
