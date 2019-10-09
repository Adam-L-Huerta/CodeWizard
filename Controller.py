import web
from Models import RegisterModel
from Models import LoginModel
from Models import Posts


web.config.debug = False
urls = (
    '/', 'Home',
    '/register', 'Register',
    '/postregistration', 'PostRegistration',
    '/login', 'Login',
    '/logout', 'Logout',
    '/check-login', 'CheckLogin',
    '/post-activity', 'PostActivity'
)


app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore("sessions"),initializer={"user": None})
session_data = session._initializer

render = web.template.render("Views/Templates", base="MainLayout", globals= {"session": session_data, 'current_user': session_data["user"]})


# Classes / Routes


class Home:
    def GET(self):
        data = type('obj', (object,), {'username': 'adam1', 'password': '12345'})

        login = LoginModel.LoginModel()
        is_correct = login.check_login(data)

        if is_correct:
            session_data["user"] = is_correct

        posts_model = Posts.Posts()
        posts = posts_model.get_all_posts()

        return render.Home(posts)


class Register:
    def GET(self):
        return render.Register()


class PostRegistration:
    def POST(self):
        data = web.input()

        reg_model = RegisterModel.RegisterModel()
        reg_model.insert_user(data)
        return data.username


class Login:
    def GET(self):
        return render.Login()


class CheckLogin:
    def POST(self):
        data = web.input()
        login = LoginModel.LoginModel()
        is_correct = login.check_login(data)

        if is_correct:
            session_data["user"] = is_correct
            return is_correct

        return "error"


class Logout:
    def GET(self):
        session['user'] = None
        session_data['user'] = None

        session.kill()
        return "success"


class PostActivity:
    def POST(self):
        data = web.input()
        data.username = session_data['user']['username']

        post_model = Posts.Posts()
        post_model.insert_post(data)
        return "success"


if __name__ == "__main__":
    app.run()