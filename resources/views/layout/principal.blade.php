<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>relBack - @yield('title')</title>

    <link rel="shortcut icon" href="{!! asset('images/favicon.ico') !!}" /> 
    
    <link href="{!! asset('css/bootstrap.min.css') !!}" rel="stylesheet" type="text/css" />
	<link href="{!! asset('css/octicons.css') !!}" rel="stylesheet"type="text/css" />
	<link href="{!! asset('css/datatables.css') !!}" rel="stylesheet"type="text/css" />

	<style>

		body {
			  font-family: 'Roboto', sans-serif;
			}

	</style>

</head>
<body>

	<span id="top"></span>

		<nav class="navbar navbar-inverse navbar-fixed-top">

			<div class="container-fluid">

				<div class="nav navbar-nav navbar-header">
					<a class="navbar-brand" href="{{ action('HomeController@index') }}"><font face='Courier' size='20' color='bdccd4'>rel</font><font face='Courier New Bold,Courier' size='20' color='569bbe'><b>Back</b></font></a>
				</div>

				<div class="navbar-text" align="bottom">
					Created by <a href="{{action('HomeController@about')}}">Creators</a>, duh!
				</div>

				<div id="navbar" class="navbar-collapse collapse">					
					<ul class="nav navbar-nav navbar-right">
						<li><a href="{{action('HomeController@index')}}">Home</a></li>
						<li><a href="{{action('ReportsController@readDefault')}}">Reports</a></li>
						<li><a href="{{action('ClientsController@read')}}">Clients</a></li>		
						<li><a href="{{action('HostsController@read')}}">Hosts</a></li>
						<li><a href="{{action('DatabasesController@read')}}">Databases</a></li>
						<li><a href="{{action('PoliciesController@read')}}">Backup Policies</a></li>

						<!-- With the update from 5.1 to 5.3, auth began to display error.
							 Pending correction / adaptation. -->

							@if(auth()->guest())
								@if(!Request::is('/login'))
									<li><a href="{{ route('login') }}">Login  </a></li>
								@endif
							@else
								<li class="dropdown">
									<a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false"> 
										{{ auth()->user()->name }} 
										<span class="caret"></span>
									</a>
									<ul class="dropdown-menu" role="menu">
										<li>
											<a href="{{ route('register') }}">Register  </a></li>
										<li>
											<a href="{{ route('logout') }}" onclick="event.preventDefault(); document.getElementById('logout-form').submit();">Logout  </a> 
											<form id="logout-form" action="{{ route('logout') }}" method="POST" style="display: none;">{{ csrf_field() }}</form>
										</li>
									</ul>
								</li>
							@endif 

						<li>&nbsp&nbsp&nbsp</li>
					</ul>
				</div>
			</div>
		</nav>

	<br><br><br>

	<!-- yield  -->
	@yield('content')

	<br><br>

	<footer class="container-fluid text-center">
		<a href="#top" title="To Top">
			<span class="glyphicon glyphicon-chevron-up"></span>
		</a>
		<p><h3>Random Report Company</h3></p>
			<a target="_blank" href="https://github.com/supernoi/relback" alt="GitHub of relBack">
				<span class="mega-octicon octicon-mark-github"></span>/relBack
			</a>
		<p><b>relBack v1.0.0</b></p>
		<p>Created by <a href="{{action('HomeController@about')}}">Creators</a>, duh!</p>

		<br>
	</footer>

	<!-- Scripts -->
	<script type="text/javascript" src="{!! asset('js/jquery.min.js') !!}" async></script>
	<script type="text/javascript" src="{!! asset('js/bootstrap.min.js') !!}" async></script>
	<script type="text/javascript" src="{!! asset('js/nanobar.min.js') !!}" async></script>

	<script type="text/javascript" src="{!! asset('js/moment.min.js') !!}" async></script>
	<script type="text/javascript" src="{!! asset('js/datatables.min.js') !!}" async></script>
	<script type="text/javascript" src="{!! asset('js/datatime-moment.js') !!}" async></script>
	<script type="text/javascript" src="{!! asset('js/main.js') !!}"></script>

	<link href='{!! asset('css/fonts.css') !!}' rel='stylesheet' type='text/css'>

	<script>
		var options = {
			bg: '#569bbe',
		};

		var nanobar = new Nanobar(options);
		nanobar.go(10);
		nanobar.go(100);
	</script>

</body>
</html>