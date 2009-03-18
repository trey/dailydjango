import web
import twitter
import time
import re
import markdown
import os.path

web.config.debug = False

urls = (
    '/', 'home',
    '/about/', 'about'
)

application = web.application(urls, globals()).wsgifunc()
app = web.application(urls, globals())
globals = {'markdown': markdown.markdown, 'render': web.template.render(os.path.join(os.path.dirname(__file__), 'templates/'))}
render = web.template.render(os.path.join(os.path.dirname(__file__), 'templates/'), base='layout', globals=globals)

class home:
    def GET(self):
        api = twitter.Api(username='username', password='password')
        api.SetCacheTimeout(900) # Cache for 15 minutes.

        followers, counter = [], 1
        while not len(followers) % 100:
            followers += api.GetFollowers(page=counter)
            counter += 1

        follower_latest = followers[0]
        follower_count = len(followers)

        statuses = api.GetUserTimeline('DailyDjango')
        for s in statuses:
            s.text = re.sub(r'(http|https|ftp)(:\/\/[^\s]*)', r'<a href="\1\2">\1\2</a>', s.text)
            s.text = re.sub(r'@([a-zA-Z0-9_]*)', r'<a href="http://twitter.com/\1">@\1</a>', s.text)
            s.day = time.strftime('%B %d', time.localtime(s.created_at_in_seconds))
        return render.home(statuses, follower_latest, follower_count)

class about:
    def GET(self):
        return render.about()

if __name__ == "__main__":
    app.run()
