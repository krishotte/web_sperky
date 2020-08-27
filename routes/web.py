"""Web Routes."""

from masonite.routes import Get, Post

ROUTES = [
    Get('/', 'WelcomeController@show').name('welcome'),

    # Main route
    Get('/main', 'MainController@show'),

    # Portfolio route
    Get('/portfolio', 'PortfolioController@show')
]

from masonite.auth import Auth 
ROUTES += Auth.routes()
