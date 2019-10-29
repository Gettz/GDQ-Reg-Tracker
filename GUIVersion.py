import mechanicalsoup
import time
from twilio.rest import Client
from tkinter import *

version = '0.3'

account_sid = "AC239933d64979964a4144a2c6b19e20eb"
auth_token = "28e9e243be9876944987cb65b41053cb"

client = Client(account_sid, auth_token)

browser = mechanicalsoup.StatefulBrowser()

showhide = TRUE
running = FALSE
first = TRUE
idx = 0


def login():
    browser.open("https://gamesdonequick.com/auth/login")
    browser.select_form('form[action="https://gamesdonequick.com/auth/login"]')
    browser["email"] = emailentry.get()
    browser["password"] = passentry.get()
    login_page = browser.submit_selected()

    if 'These credentials do not match our records.' in login_page.soup.get_text():
        output.configure(state="normal", fg="red")
        output.delete(0.0, END)
        output.insert(END, "Login Failed")
        output.configure(state="disabled")
    else:
        output.configure(state="normal", fg="black")
        output.delete(0.0, END)
        output.insert(END, "Login Successful!")
        output.configure(state="disabled")
        browser.open("https://gamesdonequick.com/profile")
        create()


def parse():
    rawpercent = list(browser.get_current_page().find('div', class_="progress"))
    rawmax = list(browser.get_current_page().find('p', class_="text-center"))
    percent = str(rawpercent[1]).split(' ')
    percent = percent[8].replace(";","")
    dic = {"<strong>": "", "</strong>": "", "[": "", "]": "", " ": ""}
    maxim = str(rawmax)
    for fluff, blank in dic.items():
        maxim = maxim.replace(fluff, blank)
    return percent, maxim


def test():
    percent, maxim = parse()
    sms = "SMS Messaging is working! There are currently: " + maxim + "registrants"
    client.messages.create(
        to="+15129021886",
        from_="+17734668036",
        body=sms
    )


#def check():
#    first = True
#    oldpercent = ''
#    oldmax = ''
#    try:
#        while True:
#            browser.refresh()
#            percent, maxim = parse()
#            if first:
#                print("Currently registration is at " + percent + " of capacity")
#                print("\nThe total number of registrants is: " + maxim)
#                first = False
#                oldpercent = percent
#                oldmax = maxim
#            if oldpercent != percent or oldmax != maxim:
#                print("The number of registrants has changed!")
#                print("Registration total is now at: " + maxim)
#                oldpercent = percent
#                oldmax = maxim
#                if int(maxim[:4]) < 3006:
#                    sms = "There are now " + maxim + "registrants. Go to https://gamesdonequick.com/profile to sign up"
#                    client.messages.create(
#                        to="+15129021886",
#                        from_="+17734668036",
#                        body=sms
#                    )
#            time.sleep(5)
#    except KeyboardInterrupt:
#        print("Shutting down in 5 secs")
#        time.sleep(5)
#        exit()

def check():
    global showhide
    global first
    first = FALSE
    print("checking")
    if running:
            browser.refresh()
            percent, maxim = parse()

            maxtext.configure(state="normal")
            maxtext.delete(0.0, END)
            maxtext.configure(width=11)
            maxtext.insert(END, maxim + "\nRegistrants")
            maxtext.configure(state="disabled")

            percenttext.configure(state="normal")
            percenttext.delete(0.0, END)
            percenttext.configure(width=(len(percent) + 10))
            percenttext.insert(END, percent + " of total")
            percenttext.configure(state="disabled")

            if int(maxim[:4]) < 3006:
                sms = "There are now " + maxim + "registrants. Go to https://gamesdonequick.com/profile to sign up"
                client.messages.create(
                    to="+15129021886",
                    from_="+17734668036",
                    body=sms
                )
            print("checked")
    window.after(1000, check)


def create():
    emailentry.configure(state="disabled")
    passentry.configure(state="disabled")
    subbutton.configure(state="disabled")
    line = Text(window, width=15, height=1, background="teal", borderwidth=0, font="none 12 bold")
    line.grid(row=5, column=0, columnspan=4, sticky="EW")
    line.insert(END, "-------------------------------------------------------------------------------------------")
    line.configure(state="disabled")

    startbutton.place(x=250, y=265)

#    stopbutton = Button(window, text="Stop", width=9, command=login, state=NORMAL)
#    stopbutton.place(x=150, y=250)

    testbutton.place(x=50, y=265)


def startstop():
    global showhide
    global first
    global running

    if showhide:
        if first:
            running = TRUE
            testbutton.place_forget()
            startbutton.configure(text="Stop")
            showhide = FALSE
            check()
        else:
            testbutton.place_forget()
            startbutton.configure(text="Stop")
            showhide = FALSE
            running = FALSE
    else:
        testbutton.place(x=50, y=265)
        startbutton.configure(text="Start")
        showhide = TRUE
        running = TRUE
        check()


window = Tk()
window.title("GDQ Registration Tracker")
window.configure(background="teal")
window.geometry("400x300")

logo = PhotoImage(file="GDQLogo2.png")
Label(window, image=logo, bg="teal").grid(row=0, column=2, sticky="news", columnspan=2, rowspan=2, padx=5, pady=5)

Label(window, text="Email:           ", bg="teal", fg="white", font="none 12 bold").grid(row=0, column=0, sticky="W")
emailentry = Entry(window, width=20, bg="white", font="none 12")
emailentry.grid(row=0, column=1, sticky="W")

Label(window, text="Password:  ", bg="teal", fg="white", font="none 12 bold").grid(row=1, column=0, sticky="W")
passentry = Entry(window, width=20, bg="white", font="none 12", show="*")
passentry.grid(row=1, column=1, sticky="W")

subbutton = Button(window, text="Submit", width=4, command=login, state=NORMAL)
subbutton.grid(row=3, column=2, columnspan=2, sticky="EW", padx=5)

output = Text(window, width=15, height=1, background="teal", state="disabled", borderwidth=0, font="none 12 bold")
output.grid(row=3, column=0, columnspan=2, sticky="EW", padx=5)

startbutton = Button(window, text="Start", width=9, command=startstop, state=NORMAL)

testbutton = Button(window, text="Test SMS", width=9, command=test, state=NORMAL)

maxtext = Text(window, width=0, height=2, background="teal", state="disabled", borderwidth=0, font="none 20 bold")
maxtext.grid(row=6, column=0, columnspan=4, padx=20, pady=20)

percenttext = Text(window, width=0, height=1, background="teal", state="disabled", borderwidth=0, font="none 12 bold")
percenttext.grid(row=7, column=0, columnspan=4, padx=20, pady=20)

mainloop()

