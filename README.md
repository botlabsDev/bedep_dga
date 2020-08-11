# bedep_dga - extended
 
Initially published and forked from https://github.com/arbor/bedep_dga #ThanksForSharing @tildedennis

The original bedep_dga.py script is awesome work, but it lacks an option to calculate the bedep 
domains used in the past.

This extended version provides:
* add an option to calculate all domains ever used by bedep
* fixed off by one bug - domains are valid from Thursday to next Wednesday   
* fixed "new year bug" - 2018-2019 has tuesdays with no currency data 
  




## Setup Environement
```shell script
$ git clone https://github.com/botlabsDev/bedep_dga
$ cd bedep_dga
$ . ./bootstrap # create virtualenv and activate 
```


## Execute DGA

```shell script
## get currently used domains for this week
(venv) $ bedep_dga

## get domains used for next week 
(venv) $ bedep_dga --next-week

## get domains from specific start date till today 
(venv) $ bedep_dga --start 2020-01-01

## get domains from specific start date till specific end
(venv) $ bedep_dga --start 2020-01-01 --end 2020-02-01

```

## Create CSV

```shell script
(venv) $ bedep_dga > domains.csv
```



