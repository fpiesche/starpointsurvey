starpointsurvey
===============

Small python script to fill in that bloody Club Nintendo survey for claiming Star Points.

This will *not* register your codes for you, but if you have unclaimed points that need the survey filling in (e.g. from eShop purchases or previously-registered codes), this will open your Registered Products page, find survey links and fill the surveys in with random info and submit them.


Requirements
------------

Requires Python, the Selenium module and Firefox (default) or Chrome (which in turn requires chromedriver). To install selenium, run "pip install selenium" or "easy_install selenium".

https://code.google.com/p/selenium/wiki/ChromeDriver for ChromeDriver if you absolutely must use Chrome for this.


Usage
-----

    python starpointsurvey.py -e Club_Nintendo_login_email -p Club_Nintendo_login_password
        [-b chrome] [-c productcode]

If the script is not given a retail product code using the -c parameter, it will open the list of registered products on the account, scan it for open surveys and fill them in if needed (e.g. for eShop purchases).

Alternately, you can pass in the product code from the flyer included with retail games with the -c parameter to register it and fill in the survey, claiming your stars.
