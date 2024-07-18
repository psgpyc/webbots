import time

from booking.searchBooking import Booking
from selenium.webdriver.chrome.options import Options

with Booking() as bot:
    bot.land_first_page()
    bot.accept_cookies()
    status = bot.remove_login_popup()
    if status == 'success':
        bot.change_currency(currency='AUD')
        bot.select_vacation_destination('London')
        bot.select_arrival_date(dateval_checkin='2024-07-20', dateval_checkout='2024-08-11')
        bot.select_occupancy()
        bot.select_adults(7)
        bot.select_children(4)
        time.sleep(20)
    else:
        print('Service side issue occurred! Please rerun the program')
        bot.land_first_page()
        bot.accept_cookies()
        status = bot.remove_login_popup()
        if status == 'error':
            bot.change_currency(currency='AUD')
            bot.select_vacation_destination('London')
            bot.select_arrival_date(dateval_checkin='2024-07-20', dateval_checkout='2024-08-11')
            bot.select_occupancy()
            bot.select_adults(7)
            bot.select_children(2)
            time.sleep(20)






