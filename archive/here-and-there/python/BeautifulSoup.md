# Beautiful Soup
Assume we have a html like below:
```html
<!DOCUMENT html>
<head>
    <titel>This is a test html text.<title>
</head>

<body>
    <h2>This is a title</h2>
    <p>This is a...</p>
    <img src="this is a url" />
</body>
```

And may be you want to get some informations from this html document and the tags is really annoying.

So here comes the [`Beautiful Soup`](https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/).

```python
html_text = '''
<img src="this is a url" />
'''

>soup = BeautifulSoup(html_text)
>img  = soup.find('img')
# img has a attribute 'src' and we can get it like this
>src = img['src']
# But if you want to see weather an attribute is in the tag
# You cannot use this 'src' in img
# Cause it will return false even you think it is True
>'src' in img
False
# Use this instead
>if img.get('src', None):
...    do something
```