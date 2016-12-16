

<?php $__env->startSection('title', 'Databases'); ?>

<?php $__env->startSection('content'); ?>

	<div class="container container-fluid"> 
		<h1>Databases list</h1>  
		
		<br>
		<a href="" data-target="#modalAddNew" id="fetch" data-toggle="modal"  class="btn btn-primary">Add New</a>
		<br><br>

		<?php if(count($errors) > 0): ?>
			<div class="alert alert-danger">
				<ul>
					<?php $__currentLoopData = $errors->all(); $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $error): $__env->incrementLoopIndices(); $loop = $__env->getFirstLoop(); ?>
					<li><?php echo e($error); ?></li>
					<?php endforeach; $__env->popLoop(); $loop = $__env->getFirstLoop(); ?>
				</ul>
			</div>
		<?php endif; ?>

	<!-- Modal of addNew -->

		<div class="modal fade" id="modalAddNew" role="dialog" aria-labelledby="ModalLabel-AddNew">
			<div class="modal-dialog">
				<div class="modal-content">
				 	<div class="modal-header">
						<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
						<h2 class="modal-title">Add new Database</h2>
					</div>
					<div class="modal-body">

						<form class="form-horizontal" action="<?php echo e(action('DatabasesController@createAdd')); ?>" method="POST">
							<input type="hidden" name="_token" value="<?php echo e(csrf_token()); ?>" />
							
							<input type="hidden" name="created_id_user" value="<?php echo e(Auth::id()); ?>">
							
							<div class="form-group">
								<div class="col-md-10">
									<div class="input-group">									
										<span class="input-group-addon">Client name</span>
										<select type="id_client" class="form-control" name="id_client">
											<?php $__currentLoopData = $clients; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $c): $__env->incrementLoopIndices(); $loop = $__env->getFirstLoop(); ?>
												<option value="<?php echo e($c->id_client); ?>"><?php echo e($c->name); ?></option>
											<?php endforeach; $__env->popLoop(); $loop = $__env->getFirstLoop(); ?>
										</select>
									</div>
								</div>
							</div>

							<div class="form-group">
								<div class="col-md-10">
									<div class="input-group">									
										<span class="input-group-addon">Hostname</span>
										<select type="id_host" class="form-control" name="id_host">
											<?php $__currentLoopData = $hosts; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $h): $__env->incrementLoopIndices(); $loop = $__env->getFirstLoop(); ?>
												<option value="<?php echo e($h->id_host); ?>"><?php echo e($h->hostname); ?></option>
											<?php endforeach; $__env->popLoop(); $loop = $__env->getFirstLoop(); ?>
										</select>
									</div>
								</div>
							</div>

							<div class="form-group">
								<div class="col-md-10">
									<div class="input-group">					
											<span class="input-group-addon">Database(DB_NAME)</span>					
											<input name="db_name" type="text" class="form-control" value="<?php echo e(old('db_name')); ?>">
									</div>
								</div>
							</div>

							<div class="form-group">
								<div class="col-md-8">
									<div class="input-group">					
											<span class="input-group-addon">DBID</span>					
											<input name="dbid" type="text" class="form-control" value="<?php echo e(old('dbid')); ?>">
									</div>
								</div>
							</div>

							<div class="form-group">
								<div class="col-md-12">
									<div class="input-group">
											<span class="input-group-addon">Description</span>					
											<input name="description" type="text" class="form-control" value="<?php echo e(old('description')); ?>">
									</div>
								</div>
							</div>
							
							<div class="modal-footer">
								<a class="btn btn-default" data-dismiss="modal">Close</a>
								<button class="btn btn-primary" type="submit">Add</button>							
							</div>
						</form>
					</div>
				</div>
			</div>
		</div>
	<!-- End Modal of addNew -->

		<?php if(old('db_name')): ?>
		  <div class="alert alert-success">
		    <strong>Sucess!</strong> 
		        The host <?php echo e(old('db_name')); ?> was created or updated.
		  </div>
		<?php endif; ?>

		<div class="panel panel-default">
			<table class="table table-striped">
				<tr>
					<th class="text-center"><h4><strong>Client Name</strong></h4></th>
					<th class="text-center"><h4><strong>Hostname</strong></h4></th>
					<th class="text-center"><h4><strong>DB_NAME</strong></h4></th>
					<th class="text-center"><h4><strong>DBID</strong></h4></th>			
					<th class="text-center"><h4><strong>Description</strong></h4></th>
					<th class="text-center"><h4><strong>Options</strong></h4></th>
				</tr>
			<?php $__currentLoopData = $databases; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $d): $__env->incrementLoopIndices(); $loop = $__env->getFirstLoop(); ?> 
				<tr>
					<td class="text-center"><?php echo e($d->client->name); ?></td>
				    <td class="text-center"><?php echo e($d->host->hostname); ?></td>
				    <td class="text-center"><?php echo e($d->db_name); ?></td>
				    <td class="text-center"><?php echo e($d->dbid); ?></td>
				    <td class="text-center"><?php echo e($d->description); ?></td>
				    <td class="text-center">
						<a href="" data-target="#modalReadDetail-<?php echo e($d->id_database); ?>" id="fetch" data-toggle="modal"><span class="glyphicon glyphicon-search"></span></a>
						&nbsp&nbsp<a href="" data-target="#modalUpdate-<?php echo e($d->id_database); ?>" id="fetch" data-toggle="modal"><span class="glyphicon glyphicon-pencil"></span></a>
						&nbsp&nbsp<a href="" data-target="#modalDelete-<?php echo e($d->id_database); ?>" id="fetch" data-toggle="modal" ><span class="glyphicon glyphicon-trash"></span></a>	
				    </td>	
				</tr>

			<!-- Modal of ReadDetail -->

				<div class="modal fade" id="modalReadDetail-<?php echo e($d->id_database); ?>" role="dialog" aria-labelledby="ModalLabel-ReadDetail">
					<div class="modal-dialog">
						<div class="modal-content">
						 	<div class="modal-header">
								<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
								<h2 class="modal-title"><?php echo e($d->db_name); ?></h2>
							</div>
							<div class="modal-body">								
								<ul>
									<li>
										<b>Client name:</b> <?php echo e($d->client->name); ?> 
									</li>
									<li>
										<b>Hostname:</b> <?php echo e($d->host->hostname); ?>

									</li>
									<li>
										<b>DB_NAME:</b> <?php echo e($d->db_name); ?>

									</li>
									<li>
										<b>DBID:</b> <?php echo e($d->dbid); ?>

									</li>
									<li>
										<b>Client description:</b> <?php echo e($d->description); ?>

									</li>
								</ul>
							</div>
							<div class="modal-footer">
								<a class="btn btn-default" data-dismiss="modal">Close</a>								
							</div>
						</div>
					</div>
				</div>	

			<!-- Modal of update -->

				<div class="modal fade" id="modalUpdate-<?php echo e($d->id_database); ?>" role="dialog" aria-labelledby="ModalLabel-Update">
					<div class="modal-dialog">
						<div class="modal-content">
						 	<div class="modal-header">
								<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
								<h2 class="modal-title"><?php echo e($d->db_name); ?></h2>
							</div>
							<form class="form-horizontal" action="<?php echo e(action('DatabasesController@updateSave')); ?>" method="POST">
								<input type="hidden" name="_token" value="<?php echo e(csrf_token()); ?>" />
								<input type="hidden" name="id_database" value="<?php echo e($d->id_database); ?>"> 
								
								<div class="modal-body">
									<div class="row form-group">
										<div class="col-md-6">
											<div class="input-group">									
												<span class="input-group-addon">Client name</span>
												<select type="id_client" class="form-control" name="id_client">
														<option value="<?php echo e($d->id_client); ?>" selected><?php echo e($d->client->name); ?></option>
														<option disabled>------</option>
													<?php $__currentLoopData = $clients; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $c): $__env->incrementLoopIndices(); $loop = $__env->getFirstLoop(); ?>
														<option value="<?php echo e($c->id_client); ?>"><?php echo e($c->name); ?></option>
													<?php endforeach; $__env->popLoop(); $loop = $__env->getFirstLoop(); ?>
												</select>
											</div>
										</div>
									</div>

									<div class="row form-group">
										<div class="col-md-6">
											<div class="input-group">
												<span class="input-group-addon">Hostname</span>
												<select type="id_host" class="form-control" name="id_host">
														<option value="<?php echo e($d->id_host); ?>"><?php echo e($d->host->hostname); ?></option>
														<option disabled>------</option>
													<?php $__currentLoopData = $hosts; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $h): $__env->incrementLoopIndices(); $loop = $__env->getFirstLoop(); ?>
														<option value="<?php echo e($h->id_host); ?>"><?php echo e($h->hostname); ?></option>
													<?php endforeach; $__env->popLoop(); $loop = $__env->getFirstLoop(); ?>
												</select>
											</div>
										</div>
									</div>

									<div class="row form-group">
										<div class="col-md-8 ">
											<div class="input-group">
												<span class="input-group-addon">Hostname</span>
												<input type="db_name" class="form-control" name="db_name" value="<?php echo e($d->db_name); ?>">
											</div>
										</div>
									</div>

									<div class="row form-group">
										<div class="col-md-6 ">
											<div class="input-group">
												<span class="input-group-addon">DBID</span>
												<input t<input type="dbid" class="form-control" name="dbid" value="<?php echo e($d->dbid); ?>">
											</div>
										</div>
									</div>

									<div class="row form-group">
										<div class="col-md-12 ">
											<div class="input-group">
												<span class="input-group-addon">Description</span>
												<input type="description" class="form-control" name="description" value="<?php echo e($d->description); ?>">
											</div>
										</div>
									</div>
								</div>	
								<div class="modal-footer">
									<a class="btn btn-default" data-dismiss="modal">Close</a>
									<button class="btn btn-warning" type="submit">Update</button> 
								</div>
							</form>
						</div>
					</div>
				</div>

			<!-- Modal of Delete -->

				<div class="modal fade" id="modalDelete-<?php echo e($d->id_database); ?>" role="dialog" aria-labelledby="SmallModalLabel-Delete">
					<div class="modal-dialog">
						<div class="modal-content">
						 	<div class="modal-header">
								<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
								<h4 class="modal-title">Confirmation</h4>
							</div>
							<div class="modal-body">
								<h5>Really want to delete the client <b><?php echo e($d->db_name); ?></b>?</h5>
							</div>
							<div class="modal-footer">
								<a class="btn btn-default" data-dismiss="modal">Close</a>
								<a href="<?php echo e(action('DatabasesController@delete', [$d->id_database])); ?>" class="btn btn-danger">Delete</a>
							</div>
						</div>
					</div>
				</div>

			<?php endforeach; $__env->popLoop(); $loop = $__env->getFirstLoop(); ?>
			</table>
		</div>
		
	</div>

<?php $__env->stopSection(); ?>
<?php echo $__env->make('layout.principal', array_except(get_defined_vars(), array('__data', '__path')))->render(); ?>