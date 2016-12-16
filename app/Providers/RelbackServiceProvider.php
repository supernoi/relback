<?php

namespace supernoi\relbackSource;

use Illuminate\Support\ServiceProvider;

class RelbackServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap the application services.
     *
     * @return void
     */
    public function boot()
    {
	
		/* Routes */
		
		$this->publishes([ __DIR__ . '/app/Http/Kernel.php' 	=> base_path('app/Http/Kernel.php'), ]);
		$this->publishes([ __DIR__ . '/app/Http/routes.php' 	=> base_path('app/Http/routes.php'), ]);		
		
		/* Schedule */
		
		$this->publishes([ __DIR__ . '/app/Console/Kernel.php' 	=> base_path('app/Console/Kernel.php'), ]);
		
		/* Models */
		
		$this->publishes([ __DIR__ . '/app/User.php'					=> base_path('app/User.php'), ]);
		$this->publishes([ __DIR__ . '/app/Client.php'					=> base_path('app/Client.php'), ]);
		$this->publishes([ __DIR__ . '/app/Host.php'					=> base_path('app/Host.php'), ]);
		$this->publishes([ __DIR__ . '/app/Database.php'				=> base_path('app/Database.php'), ]);
		$this->publishes([ __DIR__ . '/app/Policy.php'					=> base_path('app/Policy.php'), ]);
		$this->publishes([ __DIR__ . '/app/RmanBackupJobDetails.php'	=> base_path('app/RmanBackupJobDetails.php'), ]);
		$this->publishes([ __DIR__ . '/app/RmanOutput.php'				=> base_path('app/RmanOutput.php'), ]);
				
		/* Controllers */
		
		$this->publishes([ __DIR__ . '/app/Http/Controllers/HomeController.php' 		=> base_path('app/Http/Controllers/HomeController.php'), ]);
		$this->publishes([ __DIR__ . '/app/Http/Controllers/ClientsController.php' 		=> base_path('app/Http/Controllers/ClientsController.php'), ]);
		$this->publishes([ __DIR__ . '/app/Http/Controllers/HostsController.php' 		=> base_path('app/Http/Controllers/HostsController.php'), ]);
		$this->publishes([ __DIR__ . '/app/Http/Controllers/DatabasesController.php' 	=> base_path('app/Http/Controllers/DatabasesController.php'), ]);
		$this->publishes([ __DIR__ . '/app/Http/Controllers/PoliciesController.php' 	=> base_path('app/Http/Controllers/PoliciesController.php'), ]);
		$this->publishes([ __DIR__ . '/app/Http/Controllers/ReportsController.php' 		=> base_path('app/Http/Controllers/ReportsController.php'), ]);
		$this->publishes([ __DIR__ . '/app/Http/Controllers/Auth/AuthController.php' 	=> base_path('app/Http/Controllers/Auth/AuthController.php'), ]);
		$this->publishes([ __DIR__ . '/app/Http/Controllers/Auth/PasswordController.php'=> base_path('app/Http/Controllers/Auth/PasswordController.php'), ]);
		
		/* Views */
		
		$this->publishes([ __DIR__ . '/resources/views/home.blade.php'							=> base_path('resources/views/home.blade.php'), ]);
		$this->publishes([ __DIR__ . '/resources/views/clients/clientsRead.blade.php'			=> base_path('resources/views/clients/clientsRead.blade.php'), ]);
		$this->publishes([ __DIR__ . '/resources/views/hosts/hostsRead.blade.php'				=> base_path('resources/views/hosts/hostsRead.blade.php'), ]);
		$this->publishes([ __DIR__ . '/resources/views/databases/databasesRead.blade.php'		=> base_path('resources/views/databases/databasesRead.blade.php'), ]);
		$this->publishes([ __DIR__ . '/resources/views/policies/policiesRead.blade.php'			=> base_path('resources/views/policies/policiesRead.blade.php'), ]);
		$this->publishes([ __DIR__ . '/resources/views/layout/principal.blade.php'				=> base_path('resources/views/layout/principal.blade.php'), ]);
		$this->publishes([ __DIR__ . '/resources/views/home/homeAboutCreators.blade.php'		=> base_path('resources/views/home/homeAboutCreators.blade.php'), ]);
		$this->publishes([ __DIR__ . '/resources/views/home/homeIndex.blade.php'				=> base_path('resources/views/home/homeIndex.blade.php'), ]);
		$this->publishes([ __DIR__ . '/resources/views/reports/reportsReadDefault.blade.php'	=> base_path('resources/views/reports/reportsReadDefault.blade.php'), ]);
		$this->publishes([ __DIR__ . '/resources/views/reports/reportsReadLogDetail.blade.php'	=> base_path('resources/views/reports/reportsReadLogDetail.blade.php'), ]);
		$this->publishes([ __DIR__ . '/resources/views/auth/login.blade.php'					=> base_path('resources/views/auth/login.blade.php'), ]);
		$this->publishes([ __DIR__ . '/resources/views/auth/register.blade.php'					=> base_path('resources/views/auth/register.blade.php'), ]);
		$this->publishes([ __DIR__ . '/resources/views/auth/password.blade.php'					=> base_path('resources/views/auth/password.blade.php'), ]);
		$this->publishes([ __DIR__ . '/resources/views/auth/reset.blade.php'					=> base_path('resources/views/auth/reset.blade.php'), ]);
		
		/* Requests */
		
		$this->publishes([ __DIR__ . '/app/Http/Requests/ClientsRequest.php' 	=> base_path('app/Http/Requests/ClientsRequest.php'), ]);
		$this->publishes([ __DIR__ . '/app/Http/Requests/HostsRequest.php' 		=> base_path('app/Http/Requests/HostsRequest.php'), ]);
		$this->publishes([ __DIR__ . '/app/Http/Requests/DatabasesRequest.php' 	=> base_path('app/Http/Requests/DatabasesRequest.php'), ]);
		$this->publishes([ __DIR__ . '/app/Http/Requests/PoliciesRequest.php' 	=> base_path('app/Http/Requests/PoliciesRequest.php'), ]);
		
		/* Public */
		
		$this->publishes([ __DIR__ . '/public/robots.txt' 								=> base_path('public/robots.txt'), ]);
		$this->publishes([ __DIR__ . '/public/index.php' 								=> base_path('public/index.php'), ]);
		$this->publishes([ __DIR__ . '/public/css/bootstrap.min.css' 					=> base_path('public/css/bootstrap.min.css'), ]);
		$this->publishes([ __DIR__ . '/public/css/fonts.css' 							=> base_path('public/css/fonts.css'), ]);
		$this->publishes([ __DIR__ . '/public/css/octicons.css' 						=> base_path('public/css/octicons.css'), ]);
		$this->publishes([ __DIR__ . '/public/css/bootstrap.css' 						=> base_path('public/css/bootstrap.css'), ]);
		$this->publishes([ __DIR__ . '/public/js/bootstrap.js' 							=> base_path('public/js/bootstrap.js'), ]);
		$this->publishes([ __DIR__ . '/public/js/bootstrap.min.js' 						=> base_path('public/js/bootstrap.min.js'), ]);
		$this->publishes([ __DIR__ . '/public/js/jquery.min.js' 						=> base_path('public/js/jquery.min.js'), ]);
		$this->publishes([ __DIR__ . '/public/js/angular.min.js' 						=> base_path('public/js/angular.min.js'), ]);
		$this->publishes([ __DIR__ . '/public/fonts/glyphicons-halflings-regular.woff2' => base_path('public/fonts/glyphicons-halflings-regular.woff2'), ]);
		$this->publishes([ __DIR__ . '/public/fonts/Roboto-Regular.woff2' 				=> base_path('public/fonts/Roboto-Regular.woff2'), ]);
		$this->publishes([ __DIR__ . '/public/fonts/octicons.woff' 						=> base_path('public/fonts/octicons.woff'), ]);
		$this->publishes([ __DIR__ . '/public/fonts/octicons.ttf' 						=> base_path('public/fonts/octicons.ttf'), ]);
		$this->publishes([ __DIR__ . '/public/images/creator01.png' 					=> base_path('public/images/creator01.png'), ]);
		$this->publishes([ __DIR__ . '/public/images/creator02.png' 					=> base_path('public/images/creator02.png'), ]);
		$this->publishes([ __DIR__ . '/public/images/esquema01.png' 					=> base_path('public/images/esquema01.png'), ]);
		$this->publishes([ __DIR__ . '/public/images/In-2C-21px-R.png' 					=> base_path('public/images/In-2C-21px-R.png'), ]);
		$this->publishes([ __DIR__ . '/public/images/In-2C-34px-R.png' 					=> base_path('public/images/In-2C-34px-R.png'), ]);
		$this->publishes([ __DIR__ . '/public/images/logo01.png' 						=> base_path('public/images/logo01.png'), ]);
		
		
    }

    /**
     * Register the application services.
     *
     * @return void
     */
    public function register()
    {
        //
    }
}