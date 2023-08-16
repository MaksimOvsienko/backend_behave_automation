This is my pet project to try myself in test automation of api, which was developed on my previous job, and which I tested as manual qa.

### About the product, api of which I tested

It's an app for letting and renting apartments. 
It has 2 roles:
* landlord - can create announcement about his apartment
* tenant - can view announcements

### Main features

* End to end tests:
* * User authorization, creation and deletion of announcement
* * Getting user profile data, editing and successfully saving it
* Custom logger

### Demo gif
Both scenarios successfull:

[![SceJi.gif](https://s11.gifyu.com/images/SceJi.gif)](https://gifyu.com/image/SceJi)

### Technologies used

* behavior driven development framework "behave" (also known as Cucumber) with Gherkin language
* SQLAlchemy in pair with postgres database, which is running in docker container
* Python version 3.11


### How to run project:

1. In properties.ini type correct endpoint in format "endpoint = link"
2. Write "behave" into console and enjoy
