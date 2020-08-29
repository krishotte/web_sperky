"""Web Routes."""

from masonite.routes import Get, Post

ROUTES = [
    Get('/', 'WelcomeController@show').name('welcome'),

    # Main route
    Get('/main', 'MainController@show'),

    # Portfolio route
    Get('/portfolio', 'PortfolioController@show'),

    # /porfolio/@category_id
    Get('/portfolio/@category_id', 'PortfolioController@show_one_category'),

    Get('/portfolio/@category_id/@material_id', 'PortfolioController@show_one_category_and_material'),

    # /product/@product_id

]

from masonite.auth import Auth 
ROUTES += Auth.routes()
