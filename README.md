# basketballSim-

this program is compatiable with python 3.5 and above
1.  install python wrapper for non-commercial use
```
$ python3 -m pip install ohmysportsfeedspy

$ python3 -m pip install matplotlib

$ python3 -m pip install pandas
```
add 
```
        if "player" in params:
            filename += "-" + params["player"]

        if "team" in params:
            filename += "-" + params["team"]
```
under FILE v1_0.py FUNCTION  __make_output_filename
/Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/site-packages/ohmysportsfeeds

2. go to https://www.mysportsfeeds.com/login and register a username and password
3. type in the username and password into the username_password.py file
4. cd into the main file 
5. run the sortData.py file and follow the instructions, data should be stored in a local filed called "results"
