# failiac
TL;DR: Profession to zodiac mapper of Freebase people.

I wanted to see, regardless of all previous research done to confirm what I already suspected, whether star signs can 
influence at all what profession is more suitable for one person or another.

## Purpose
Besides what it's written in description I wanted to gain some experience with larger external databases, especially 
those that don't deal with relations like SQL does: n-tuples.

The reason this project landed on GitHub is that it has to be viewable and clonable for any, however unlikely, peer review.
If it wouldn't be, this would be no research.

## Deployment

### Runtime
1. Clone
2. You will need Python3 (preferably 3.4)
3. Virtualenv and pip (not necessary, but I cannot advise you to pollute your setup)
3.1 Django (the newer, the better, but tested on 1.7)
3.2 pymongo (latest)
3.3 numpy
4. Activate virtualenv, navigate to the failiac folder and run "pip install -r requirements.txt"
4.1. If per chance you are using Windows and numpy doesn't want ot install, see requirements.txt for additional info
5. You will need mongodb (http://www.mongodb.org/). You might need to change some of the settings properties (settings.py) for this. Default is covered though.


### Data collection
1. You will need an account for Google's APIs and paste it to api/utils.py FREEBASE_API_KEY variable
2. To get people entities, run python manage.py getpeople
2.1. This is not optional: to parse people's birthdays and save them, run python manage.py parsebirthdays
3. To get professions, run python manage.py getprofessions
4. To prepare mongo collection about zodiac distributions, run python manage.py getzodiac
4.1 To import or export this collection (the actual result of all the downloading, poarsing and organizing, use python manage.py export/import, so you don't have to go through any of the previous steps all the time
5. To prepare the actual JS for usage, run python manage.py preparezodiacjs
6. If you want to deploy the actual result (which you view in your browser) as a standalone page, run python manage.py exportstatic

Some of the scripts (those that take long time to execute) will try to give you progress and time "estimates".

### Future
* Switch to WikiData, as Freebase is closing (if not closed already)
