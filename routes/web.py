"""Web Routes."""

from masonite.routes import Get, Post

ROUTES = [
    Get('/', 'WelcomeController@show').name('welcome'),

    # Main route
    Get('/main', 'MainController@show'),

    # Portfolio routes
    Get('/portfolio', 'PortfolioController@show'),
    Get('/portfolio/@category_id', 'PortfolioController@show_one_category'),
    Get('/portfolio/@category_id/@material_id', 'PortfolioController@show_one_category_and_material'),
    Get('/product/@product_id', 'PortfolioController@show_one_product'),

    # Admin routes
    Get('/admin/product/new', 'EditPortfolioController@empty_product'),
    Post('/admin/product/new', 'EditPortfolioController@store_product'),

    Get('/admin/product/edit', 'EditPortfolioController@get_all_products'),
    Get('/admin/product/edit/@product_id', 'EditPortfolioController@get_one_product'),
    Post('/admin/product/edit/@product_id', 'EditPortfolioController@update_product'),

    # related product chooser
    Get('/related_product/@product_id', 'EditPortfolioController@choose_related_products'),
    Post('/related_product/@product_id', 'EditPortfolioController@update_related_products')

]

from masonite.auth import Auth 
ROUTES += Auth.routes()
