starpointsurvey
===============

Small python script to fill in that bloody Club Nintendo survey for claiming Star Points.

By default, this will open your Registered Products page, find survey links and fill the surveys in with random info and submit them. You can also pass in one or multiple retail product codes to register them to your account and claim the Star Points.


Requirements
------------

Requires Python, the Selenium module and Firefox (default) or Chrome (which in turn requires chromedriver).

- *On Windows only*, install Python: download the installer from http://www.python.org/ and install.
- Install selenium: open a terminal/command prompt window and run <code>pip install selenium</code> or <code>easy_install selenium</code>. On Windows, you MAY have to run this as <code>c:\Python27\Scripts\pip.exe install selenium</code> (or <code>c:\Python34\Scripts\pip.exe install selenium</code> if you installed Python 3.4)
- *If* you want to use Chrome, visit https://code.google.com/p/selenium/wiki/ChromeDriver, download chromedriver.exe and store it in the same directory as starpointsurvey.py.


Usage
-----

    python starpointsurvey.py -e Club_Nintendo_login_email -p Club_Nintendo_login_password
        [-b chrome] [-c productcode]

If the script is not given a retail product code using the <code>-c</code> parameter, it will open the list of registered products on the account, scan it for open surveys and fill them in if needed (e.g. for eShop purchases).

Alternately, you can pass in the product code from the flyer included with retail games with the -c parameter to register it and fill in the survey, claiming your stars.

*PROTIP:* You can use <code>-c productcode</code> multiple times to register multiple product codes in one go, or dump all your product codes into a text file (one per line) and use <code>-c productcodes.txt</code> to get them all.
