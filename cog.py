from datetime import date
from tabulate import tabulate

def premiumPolicy():
    print("Welcome to policy simulator.")
    policyName = input("What is your policy name? ")
    startDate = input("What is your start date? (e.g 1/15/2021) ")
    endDate = input("What is your end date? (e.g 1/15/2022) ")
    premium = input("What is your premium? ")

    try:
        #Read through each date and create two date objects for both
        startDate = startDate.split("/")
        endDate = endDate.split("/")
        start = date(int(startDate[2]), int(startDate[0]), int(startDate[1]))
        end = date(int(endDate[2]), int(endDate[0]), int(endDate[1]))
    except:
        print("Inputs cannot be read, ending program")
        return

    #Using datetime module, we can get our total number of days
    totalDays = 0
    if end > start:
        totalDays = (end - start).days
    else: 
        #if start is greater than end, than there is an error and we can return
        print("Start date ends later than end date!")
        return

    #Get our difference in months. If less than 0, we add 12 to find the total
    monthDifference = (end.year - start.year) * 12 + end.month - start.month
    months = [31,28,31,30,31,30,31,31,30,31,30,31]

    #we use 13 here as this will ensure that we will have some range of values 1-12
    monthsLeft = 13 - start.month
    if start.year == end.year:
         monthsLeft = end.month - start.month

    AllData = []
    print(totalDays)
    for i in range(monthsLeft):
        curMonth = start.month + i
        curYear = start.year
        
        #if our policy is years in the future, we need to check 
        #how many years we need to account for
        if curMonth > 12:
            tempMonth = curMonth
            while tempMonth > 12:
                tempMonth -= 12
                curYear += 1
        
        amount = 0

        #Adjustment for leap years
        if curYear % 4 == 0 and curYear % 400 != 0:
            months[1] = 29
        else:
            months[1] = 28

        #if we are on our first month, instead of calculating the whole month
        #we want to use the amount of days in the month for our calculations
        if i == 0:
            curDays = months[start.month - 1] - float(start.day) + 1.0
            amount = round(((curDays/totalDays) * float(premium)), 2)

        #Similarly, on our last month, we want to go ahead and use
        #the days in the month we do count for our final month
        elif curYear == end.year and curMonth == end.month:
            amount = round(((end.day/totalDays) * float(premium)), 2)

        #Otherwise, we can go ahead and do our normal calculations
        else:
            amount = round(((months[curMonth - 1]/totalDays) * float(premium)), 2)

        #Minor text edits, just need to check if we need to put a zero in front of a single digit month
        curData = []
        if curMonth < 10:
            curData = [policyName, str(curYear) + " 0"  + str(curMonth), amount]
        else:
            curData = [policyName, str(curYear) + " "  + str(curMonth), amount]
        
        AllData.append(curData)

    #Write our data to a file.
    f = open("PN0001.txt", "w")
    f.write(tabulate(AllData, headers = ["Policy", "Month", "Amount"]))
    f.close()

premiumPolicy()

