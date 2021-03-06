<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>relBack - <?php echo $__env->yieldContent('title'); ?></title>

    <link rel="shortcut icon" href="images/icon/relback.ico" /> 
    
    <link href="<?php echo asset('css/bootstrap.min.css'); ?>" rel="stylesheet" type="text/css" />
	<link href="<?php echo asset('css/octicons.css'); ?>" rel="stylesheet"type="text/css" />
	<link href="<?php echo asset('css/datatables.css'); ?>" rel="stylesheet"type="text/css" />

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
					<a class="navbar-brand" href="<?php echo e(action('HomeController@index')); ?>"><font face='Courier' size='20' color='bdccd4'>rel</font><font face='Courier New Bold,Courier' size='20' color='569bbe'><b>Back</b></font></a>
				</div>

				<div class="navbar-text" align="bottom">
					Created by <a href="<?php echo e(action('HomeController@about')); ?>">Creators</a>, duh!
				</div>

				<div id="navbar" class="navbar-collapse collapse">					
					<ul class="nav navbar-nav navbar-right">
						<li><a href="<?php echo e(action('HomeController@index')); ?>">Home</a></li>
						<li><a href="<?php echo e(action('ReportsController@readDefault')); ?>">Reports</a></li>
						<li><a href="<?php echo e(action('ClientsController@read')); ?>">Clients</a></li>		
						<li><a href="<?php echo e(action('HostsController@read')); ?>">Hosts</a></li>
						<li><a href="<?php echo e(action('DatabasesController@read')); ?>">Databases</a></li>
						<li><a href="<?php echo e(action('PoliciesController@read')); ?>">Backup Policies</a></li>

						<!-- With the update from 5.1 to 5.3, auth began to display error.
							 Pending correction / adaptation.						
							<?php if(auth()->guest()): ?>
								<?php if(!Request::is('auth/login')): ?>
									<li><a href="<?php echo e(url('/auth/login')); ?>">Login  </a></li>
								<?php endif; ?>
							<?php else: ?>
								<li class="dropdown">
									<a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false"> 
										<?php echo e(auth()->user()->name); ?> 
										<span class="caret"></span>
									</a>
									<ul class="dropdown-menu" role="menu">
										<li><a href="<?php echo e(url('/auth/register')); ?>">Register  </a></li>
										<li><a href="<?php echo e(url('/auth/logout')); ?>">Logout  </a></li>
									</ul>
								</li>
							<?php endif; ?> -->

						<li>&nbsp&nbsp&nbsp</li>
					</ul>
				</div>
			</div>
		</nav>

	<br><br><br>

	<!-- yield  -->
	<?php echo $__env->yieldContent('content'); ?>

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
		<p>Created by <a href="<?php echo e(action('HomeController@about')); ?>">Creators</a>, duh!</p>

		<br>
	</footer>

	<!-- Scripts -->
	<script type="text/javascript" src="<?php echo asset('js/jquery.min.js'); ?>"></script>
	<script type="text/javascript" src="<?php echo asset('js/bootstrap.min.js'); ?>"></script>
	<script type="text/javascript" src="<?php echo asset('js/nanobar.min.js'); ?>"></script>

	<script type="text/javascript" src="<?php echo asset('js/datatables.min.js'); ?>"></script>
	<script type="text/javascript" src="<?php echo asset('js/main.js'); ?>"></script>

	<link href='<?php echo asset('css/fonts.css'); ?>' rel='stylesheet' type='text/css'>

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