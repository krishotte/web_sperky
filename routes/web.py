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
        Post('/admin/product/save-variant', 'EditPortfolioController@save_variant'),
        Post('/admin/product/delete-variant', 'EditPortfolioController@delete_variant'),
        Post('/admin/product/save-new-variant', 'EditPortfolioController@save_new_variant'),
        Get('/admin/update-cover', 'EditPortfolioController@update_cover'),

        # top products
        Get('/admin/top_products', 'AdminTopProductsController@show'),
        Get('/admin/top_product/new', 'AdminTopProductsController@choose_new'),
        Post('/admin/top_product/create', 'AdminTopProductsController@create_new'),
        Post('/admin/top_product/modify', 'AdminTopProductsController@show_existing'),
        Post('/admin/top_product/update', 'AdminTopProductsController@update_existing'),
        Post('/admin/top_product/delete', 'AdminTopProductsController@delete_existing'),

        Get('/admin/restart-server', 'EditPortfolioController@restart_server'),

        # related product chooser
        Get('/related_product/@product_id', 'EditPortfolioController@choose_related_products'),
        Post('/related_product/@product_id', 'EditPortfolioController@update_related_products'),

        # delete routes
        Post('/admin/image/delete', 'EditPortfolioController@delete_image'),

        # Admin Orders
        Get('/admin/orders', 'AdminOrdersController@show_all_orders'),
        Get('/admin/order/@order_id', 'AdminOrdersController@show_one_order'),
        Post('/admin/order-update-state', 'AdminOrdersController@update_order_status'),
        Post('/admin/order-update-discount', 'AdminOrdersController@update_order_discount'),

        # Admin Users
        Get('/admin/users', 'AdminUsersController@show_all_users'),

        # invoice routes
        Post('/admin/invoice-create', 'InvoiceController@create_invoice'),
        Get('/admin/invoice-show-one/@invoice_id', 'InvoiceController@show'),

        # test routes
        Get('/admin/test', 'TestController@show'),
        Get('/admin/test/welcome-email', 'TestController@send_welcome_email'),
        Get('/admin/test/welcome-email-queue', 'TestController@send_welcome_email_queue'),
        Get('/admin/test/new-user-email-queue', 'TestController@send_admins_new_user'),
        Get('/admin/test/new-order-email-queue', 'TestController@send_admins_new_order'),
        Get('/admin/test/welcome-email-more', 'TestController@send_more_welcome_email'),

    ], middleware=('admin', )),

    # User Dashboard routes
    RouteGroup([
        Get('/dashboard', 'DashboardController@show'),
        Get('/dashboard/profile', 'DashboardController@show_profile'),
        Get('/dashboard/orders', 'DashboardController@show_orders'),
        Get('/dashboard/order/@order_id', 'DashboardController@show_single_order'),
        Get('/dashboard/cart', 'DashboardController@show_cart'),
        # Get('/add-to-cart/@product_id', 'DashboardController@add_to_cart'),
        Post('/add-to-cart2', 'DashboardController@add_to_cart2'),
        Post('/remove-from-cart', 'DashboardController@remove_from_cart'),

        Get('/new-address', 'DashboardController@show_new_address'),
        Post('/new-address', 'DashboardController@store_new_address'),
        Get('/edit-address/@address_id', 'DashboardController@show_existing_address'),
        Post('/edit-address', 'DashboardController@store_existing_address'),
        Get('/delete-address/@address_id', 'DashboardController@delete_address'),

        # order routes
        Get('/order-user-details', 'DashboardController@order_show_user_details'),
        Post('/order-set-address', 'DashboardController@order_set_user_address'),
        Get('/order-shipping', 'DashboardController@order_show_shipping'),
        Post('order-set-shipping', 'DashboardController@order_set_shipping'),
        Post('/order-back-to-shipping', 'DashboardController@order_back_to_shipping'),
        Get('/order-review', 'DashboardController@order_review'),
        Post('/make-order', 'DashboardController@make_order'),

        # user management routes
        Get('/email/verify/send2', 'auth.ConfirmController@send_verify_email'),

    ], middleware=('auth', )),

    Get('/blog/@blog_id', 'BlogController@show_first'),

    Get('/about/contacts', 'MainController@show_contacts'),
    Get('/about/conditions', 'MainController@show_conditions'),

]

from masonite.auth import Auth 
ROUTES += Auth.routes()
