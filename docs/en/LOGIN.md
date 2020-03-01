# Simulated login

## Login a website with three lines of code
You can use the following three lines of code to easily implement a simulated login operation for any 
website in the support list. Take twitter as an example:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.twitter(username='Your Username', password='Your Password')
```
where infos_return is a dict object, which contains some user information(e.g. userid) that may be useful. The session is a 
requests.Session object after login in the target website.