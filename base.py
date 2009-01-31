import web
import twitter

urls = (
    '/', 'home',
    '/about/', 'about'
)

app = web.application(urls, globals())
render = web.template.render('templates/', base='layout')

class home:
    def GET(self):
        api = twitter.Api()
        api.SetCacheTimeout(900) # Cache for 15 minutes.
        statuses = api.GetUserTimeline('DailyDjango')
        return render.home(statuses)

class about:
    def GET(self):
        return render.about()

if __name__ == "__main__":
    app.run()
