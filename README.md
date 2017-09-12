## This is a work-in-progress project

# project1_Django

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
	

![Alt text](/summary_screen.png?raw=true "Summary"	
![Alt text](/summary_popup.png?raw=true "Summary Popup"
![Alt text](/detail_screen.png?raw=true "Detail"
