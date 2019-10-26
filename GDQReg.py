import mechanicalsoup
import time
from twilio.rest import Client

version = '0.1'

account_sid = "YUM"
auth_token = "YUMYUM"

client = Client(account_sid, auth_token)

browser = mechanicalsoup.StatefulBrowser()

browser.open("https://gamesdonequick.com/auth/login")

browser.select_form('form[action="https://gamesdonequick.com/auth/login"]')

browser["email"] = "techtml@gmail.com"
browser["password"] = "test123456"

browser.submit_selected()

browser.open("https://gamesdonequick.com/profile")

def parse():
    rawpercent = list(browser.get_current_page().find('div', class_="progress"))
    rawmax = list(browser.get_current_page().find('p', class_="text-center"))
    percent = str(rawpercent[1]).split(' ')
    percent = percent[8].replace(";","")
    dic = {"<strong>":"", "</strong>":"", "[":"", "]":""}
    maxim = str(rawmax)
    for fluff, blank in dic.items():
        maxim = maxim.replace(fluff, blank)
    return percent,maxim

def test():
    sms = "The tracker is now running!"
    client.messages.create(
        to="+15129021886",
        from_="",
        body=sms
    )

def main():
    print("=========================\nGDQ Registrant Tracker\n=========================\n")
    first = True
    oldpercent = ''
    oldmax = ''
    try:
        while True:
            browser.refresh()
            percent,maxim = parse()
            if first:
                test()
                print("Currently registration is at " + percent + " of capacity")
                print("\nThe total number of registrants is: " + maxim)
                first = False
                oldpercent = percent
                oldmax = maxim
                print(maxim[:4])
            if oldpercent != percent or oldmax != maxim:
                print("The number of registrants has changed!")
                print("Registration total is now at: " + maxim)
                if int(maxim[:4]) < 3000:
                    sms = "There are now " + maxim + "registrants. Go to https://gamesdonequick.com/profile to sign up"
                    client.messages.create(
                    to="+15129021886",
                    from_="",
                    body=sms
                    )
            time.sleep(5)
    except KeyboardInterrupt:
        print("Shutting down in 5 secs")
        time.sleep(5)
        exit()

main()
