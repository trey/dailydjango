import web
import twitter
import time

urls = (
    '/', 'home',
    '/about/', 'about'
)

app = web.application(urls, globals())
globals = {'time': time}
render = web.template.render('templates/', base='layout', globals=globals)

class home:
    def GET(self):
        api = twitter.Api()
        api.SetCacheTimeout(900) # Cache for 15 minutes.
        statuses = api.GetUserTimeline('DailyDjango')
        for s in statuses:
            s.day = time.strftime('%B %d', time.localtime(s.created_at_in_seconds))
        return render.home(statuses)

class about:
    def GET(self):
        return render.about()

if __name__ == "__main__":
    app.run()
