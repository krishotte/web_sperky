"""Web Routes."""

from masonite.routes import Get, Post, RouteGroup

ROUTES = [
    # Get('/', 'WelcomeController@show').name('welcome'),

    # Main route
    Get('/', 'MainController@show'),

    # Portfolio routes
    Get('/portfolio', 'PortfolioController@show'),
    Post('/portfolio/search', 'PortfolioController@show_search'),
    Get('/portfolio/@category_id', 'PortfolioController@show_one_category'),
    Get('/portfolio/@category_id/@material_id', 'PortfolioController@show_one_category_and_material'),
    Get('/product/@product_id', 'PortfolioController@show_one_product'),

    # Admin routes
    RouteGroup([
        Get('/admin/product/new', 'EditPortfolioController@empty_product'),
        Post('/admin/product/new', 'EditPortfolioController@store_product'),

        Get('/admin/product/edit', 'EditPortfolioController@get_all_products'),
        Get('/admin/product/edit/@product_id', 'EditPortfolioController@get_one_product'),
        Post('/admin/product/edit/@product_id', 'EditPortfolioController@update_product'),
        Get('/admin/update-cover', 'EditPortfolioController@update_cover'),

        # related product chooser
        Get('/related_product/@product_id', 'EditPortfolioController@choose_related_products'),
        Post('/related_product/@product_id', 'EditPortfolioController@update_related_products'),

        # delete routes
        Post('/admin/image/delete', 'EditPortfolioController@delete_image'),
    ], middleware=('admin', )),

    # User Dashboard routes
    RouteGroup([
        Get('/dashboard', 'DashboardController@show'),
        Get('/dashboard/profile', 'DashboardController@show_profile'),
        Get('/dashboard/orders', 'DashboardController@show_orders'),
        Get('/dashboard/order/@order_id', 'DashboardController@show_single_order'),
        Get('/dashboard/cart', 'DashboardController@show_cart'),
        Get('/add-to-cart/@product_id', 'DashboardController@add_to_cart'),
        Get('/make-order', 'DashboardController@make_order'),
        Get('/new-address', 'DashboardController@show_new_address'),
        Post('/new-address', 'DashboardController@store_new_address'),
        Get('/edit-address/@address_id', 'DashboardController@show_existing_address'),
        Post('/edit-address', 'DashboardController@store_existing_address'),
        Get('/delete-address/@address_id', 'DashboardController@delete_address'),
    ], middleware=('auth', ))

]

from masonite.auth import Auth 
ROUTES += Auth.routes()
