#Question12_activity2
"""
Write a python program to iterate through the given list.

Given list
hosts=['host01','host02','host03','host04','host05']
Using membership operator test host03 exists or not

if ‘host03’ does not exists display suitable message to screen
"""

#activity_code:KL/EP-19/A-002
#platform: python 3.10,winx 10
#Author:Mr.Jithendran
#Role:Software Engineer

hosts=['host01','host02','host03','host04','host05']
if "host03" in hosts:
    print("exists")
else:
    print("does not exists")
