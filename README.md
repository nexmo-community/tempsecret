# tempsecret
Script for setting a temporary api secret on your Nexmo account

This is a script to temporarily set an additional API secret on your nexmo account, its main use is when recording screencasts or giving webinars.

## Installation:
Copy the above code to somehere in your path thats executable eg `/usr/local/bin` and chmod it to 755
You can name the command anything you like, I use `tempsecret` witout the .py as that makes it easier to type.

Provided you have the Nexmo CLI installed it will use the same credentials file in `~/.nexmorc`

The only non-standard python library in use is `requests` you can install this by running `pip -r requirements.txt` however once you have pip then you will already have requests installed! 

## Running
By default the command will set a temporary secret of `Password123` for 5 mins (300 seconds) you can modify these by using `-p` and pasing in your own secret or `-t` for your own time
The secret must meet the nexmo requirements (8-25chars, Upper & Lower Alpha & Number)

setting the `-c` flag will just check how many secrets you have on your account and when they were created, you can have a maximum of 2 secrets at one time, to manage them use the Dashbaord.

## Important
You must leave the window open and the command running until the timer completes and the secret has been revoked otherwise it will stay on your account
