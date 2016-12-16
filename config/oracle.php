<?php

return[
	'oracle' => array(
	    'driver'   => 'oracle',
	    'tns'      => env('DB_TNS', 'DBREL'),
	    'host'     => env('DB_HOST', 'oel-srvtcc01'),
	    'port'     => env('DB_PORT', '1521'),
	    'database' => env('DB_DATABASE', 'dbrel'),
	    'username' => env('DB_USERNAME', 'relback'),
	    'password' => env('DB_PASSWORD', 'relback'),
	    'charset'  => 'WE8ISO8859P1',
	    'prefix'   => '',
	)
];