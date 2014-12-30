starpointsurvey
===============

Small python script to fill in that bloody Club Nintendo survey for claiming Star Points.

By default, this will open your Registered Products page, find survey links and fill the surveys in with random info and submit them. You can also pass in one or multiple retail product codes to register them to your account and claim the Star Points.


Requirements
------------

Requires Python, the Selenium module and Firefox (default) or Chrome (which in turn requires chromedriver). To install selenium, run <code>pip install selenium</code> or <code>easy_install selenium</code>.

https://code.google.com/p/selenium/wiki/ChromeDriver for ChromeDriver if you absolutely must use Chrome for this.


Usage
-----

    python starpointsurvey.py -e Club_Nintendo_login_email -p Club_Nintendo_login_password
        [-b chrome] [-c productcode]

If the script is not given a retail product code using the <code>-c</code> parameter, it will open the list of registered products on the account, scan it for open surveys and fill them in if needed (e.g. for eShop purchases).

Alternately, you can pass in the product code from the flyer included with retail games with the -c parameter to register it and fill in the survey, claiming your stars.

*PROTIP:* You can use <code>-c productcode</code> multiple times to register multiple product codes in one go.
