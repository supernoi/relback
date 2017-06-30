<?php

return[
	'oracle' => array(
	    'driver'   => 'oracle',
	    'tns'      => env('DB_TNS', 'ORCL'),
	    'host'     => env('DB_HOST', 'HOSTNAME'),
	    'port'     => env('DB_PORT', '1521'),
	    'database' => env('DB_DATABASE', 'ORCL'),
	    'username' => env('DB_USERNAME', 'relback'),
	    'password' => env('DB_PASSWORD', 'relback'),
	    'charset'  => 'WE8ISO8859P1',
	    'prefix'   => '',
	)
];