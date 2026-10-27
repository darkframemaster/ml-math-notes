# Use session in django
Here is an example of using captcha to control some junk data post by robot, and here are what need to be done:

* Genarate the captcha and store the captcha code to a Session object, and we can get something like this: `(session_id, captcha_code)`
* When our app post the data to the right api, we will get the Session object , and verify the `user_code`: `captcha_code == user_code`.

## Use session provide by django
The first way to do this is use the django `Session` model, which means you need to add `'django.contrib.sessions'` to your `INSTALLED_APPS` settings, and add `'django.contrib.sessions.middleware.SessionMiddleware'` to your `MIDDLEWARE_CLASSES` settings, and your `settings` file of django may look like this.

```python
...

MIDDLEWARE_CLASSES = (
	...
	'django.contrib.sessions.middleware.SessionMiddleware',
	...
)

INSTALLED_APPS = (
	...
	'django.contrib.sessions',
	...
)

...
```

You can use lower interface to store and set the cookie of the record. 

```python
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session

# 1. use the database model
# update/create session record
    
# If the session is deleted after verify and we try to create
# a new one in here, it will not store the captcha_code to the
# session record.
session_id = request.COOKIES.get('sessionid', None)
if not session_id:
session = SessionStore()
else:
session = SessionStore(session_key = session_id)
    
session['CaptchaCode'] = captcha_code
session.save()
session_id = session.session_key
    
# set cookies for app client
response.set_cookie('sessionid', value=session_id)
```

And you can also use session in a easy way like this.

```python    
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session

# 2. the easy way
# store the captcha code in session
request.session['CaptchaCode'] = captcha_code
```

Then i verify the captcha like this:

```
from django.contrib.sessions.models import Session

# verify the captcha code
# get value from session using sessiondb
session_id = request.COOKIES['sessionid']
session = Session.objects.get(pk = session_id)
session_info = session.get_decoded()
captcha_code = session_info['CaptchaCode']
       
if str(user_code).lower() == str(captcha_code).lower():
	# once verified the captcha, delete session record 
	session.delete()
	return True
else:
	return u'wrong captcha'
```


## Use redis to store the session

```python
# use redis to store session
sessionid = uuid.uuid1().hex
redis_db.set(sessionid, captcha_code)
redis_db.expire(sessionid, 3 * 60)
response.set_cookie('sessionid', value=sessionid)
```

And get the `Session` object like this:

```
session_id = request.COOKIES['sessionid']
captcha_code = redis_db.get(session_id)

if not captcha_code or not user_code:
	return False
if str(user_code).lower() == str(captcha_code).lower():
	redis_db.delete(session_id)
	return True
else:
	return False
```

Redis give us a interface to control the session record, and it is more realiable because we know what is happening since we control the working flow.
