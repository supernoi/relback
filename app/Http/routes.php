<?php

/*Route::controllers([
	'auth' => 'Auth\AuthController',
	'password' => 'Auth\PasswordController'
	]);*/

Route::get('/', 'HomeController@index');
Route::get('/about', 'HomeController@about');

Auth::routes();

//Rotas dos Clients

Route::get('/clients', 'ClientsController@read');
Route::get('/clients/read', 'ClientsController@read');
Route::get('/clients/read/detail/{id_client}', 'ClientsController@readDetail');

Route::get('/clients/create', 'ClientsController@create');
Route::post('/clients/create/add', 'ClientsController@createAdd');

Route::get('/clients/delete/{id_client}', 'ClientsController@delete');

Route::get('/clients/update/{id_client}', 'ClientsController@updateForm');
Route::post('/clients/update/save', 'ClientsController@updateSave');

//Rotas dos Hosts

Route::get('/hosts', 'HostsController@read');
Route::get('/hosts/read', 'HostsController@read');
Route::get('/hosts/read/detail/{hostname}', 'HostsController@readDetail');

Route::get('/hosts/create', 'HostsController@create');
Route::post('/hosts/create/add', 'HostsController@createAdd');

Route::get('/hosts/delete/{hostname}', 'HostsController@delete');

Route::get('/hosts/update/{hostname}', 'HostsController@updateForm');
Route::post('/hosts/update/save', 'HostsController@updateSave');

// Rotas dos Databases

Route::get('/databases', 'DatabasesController@read');
Route::get('/databases/read', 'DatabasesController@read');
Route::get('/databases/read/detail/{db_name}', 'DatabasesController@readDetail');

Route::get('/databases/create', 'DatabasesController@create');
Route::post('/databases/create/add', 'DatabasesController@createAdd');

Route::get('/databases/delete/{db_name}', 'DatabasesController@delete');

Route::get('/databases/update/{db_name}', 'DatabasesController@updateForm');
Route::post('/databases/update/save', 'DatabasesController@updateSave');

// Rotas das Politicas

Route::get('/policies', 'PoliciesController@read');
Route::get('/policies/read', 'PoliciesController@read');
Route::get('/policies/read/detail/{id_policy}', 'PoliciesController@readDetail');

Route::get('/policies/create', 'PoliciesController@create');
Route::post('/policies/create/add', 'PoliciesController@createAdd');

Route::get('/policies/delete/{id_policy}', 'PoliciesController@delete');

Route::get('/policies/update/{id_policy}', 'PoliciesController@updateForm');
Route::post('/policies/update/save', 'PoliciesController@updateSave');

// Rotas para o Report

Route::get('/reports', 'ReportsController@readDefault');
Route::get('/reports/readLogDetail/{db_name}/{id_policy}/{session_key}', 'ReportsController@readLogDetail');
Route::get('/reports/reportmail', 'ReportsMailController@mailDailyDefault');
