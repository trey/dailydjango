import web
import twitter
import time
import re
import markdown

urls = (
    '/', 'home',
    '/about/', 'about'
)

app = web.application(urls, globals())
myglobals = {'markdown': markdown.markdown, 'render': web.template.render('templates/')}
render = web.template.render('templates/', base='layout', globals=myglobals)

class home:
    def GET(self):
        api = twitter.Api()
        api.SetCacheTimeout(900) # Cache for 15 minutes.
        statuses = api.GetUserTimeline('DailyDjango')
        for s in statuses:
            s.text = re.sub(r'(http|https|ftp)(:\/\/[^\s]*)', r'<a href="\1\2">\1\2</a>', s.text)
            s.text = re.sub(r'@([a-zA-Z0-9_]*)', r'<a href="http://twitter.com/\1">@\1</a>', s.text)
            s.day = time.strftime('%B %d', time.localtime(s.created_at_in_seconds))
        return render.home(statuses)

class about:
    def GET(self):
        return render.about()

# app = web.application(urls, globals())
# application = app.wsgifunc()
# if __name__ == "__main__":
#     app.run()

application = web.application(urls, globals()).wsgifunc()
