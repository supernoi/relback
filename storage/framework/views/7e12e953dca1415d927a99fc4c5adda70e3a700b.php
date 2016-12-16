

<?php $__env->startSection('title', 'Hosts'); ?>

<?php $__env->startSection('content'); ?>
<div class="container container-fluid"> 
	<h1>Hosts list</h1>  
	
	<br>
	<a href="" data-target="#modalAddNew" id="fetch" data-toggle="modal" class="btn btn-primary">Add New</a>
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
						<h2 class="modal-title">Add new Host</h2>
					</div>
					<div class="modal-body">

						<form class="form-horizontal" action="<?php echo e(action('HostsController@createAdd')); ?>" method="POST">
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
										<input name="hostname" type="text" class="form-control" value="<?php echo e(old('hostname')); ?>">
									</div>
								</div>
							</div>

							<div class="form-group">
								<div class="col-md-8">
									<div class="input-group">					
											<span class="input-group-addon">IP</span>					
											<input name="ip" type="text" class="form-control" value="<?php echo e(old('ip')); ?>">
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

	<?php if(old('hostname')): ?>
	  <div class="alert alert-success">
	    <strong>Sucess!</strong> 
	        The host <?php echo e(old('hostname')); ?> was created or updated.
	  </div>
	<?php endif; ?>

	<div class="panel panel-default">
		<table class="table table-striped">
			<tr>
				<td class="text-center"><h4><strong>Client Name</strong></h4></td>
				<td class="text-center"><h4><strong>Hostname</strong></h4></td>
				<td class="text-center"><h4><strong>Description</strong></h4></td>
				<td class="text-center"><h4><strong>Options</strong></h4></td>
			</tr>
		<?php $__currentLoopData = $hosts; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $h): $__env->incrementLoopIndices(); $loop = $__env->getFirstLoop(); ?> 
			<tr>
				<td class="text-center"><?php echo e($h->client->name); ?></td>
			    <td class="text-center"><?php echo e($h->hostname); ?></td>
			    <td class="text-center"><?php echo e($h->description); ?></td>
			    <td class="text-center">
					<a href="" data-target="#modalReadDetail-<?php echo e($h->id_host); ?>" id="fetch" data-toggle="modal"><span class="glyphicon glyphicon-search"></span></a>
					&nbsp&nbsp<a href="" data-target="#modalUpdate-<?php echo e($h->id_host); ?>" id="fetch" data-toggle="modal"><span class="glyphicon glyphicon-pencil"></span></a>
					&nbsp&nbsp<a href="" data-target="#modalDelete-<?php echo e($h->id_host); ?>" id="fetch" data-toggle="modal"><span class="glyphicon glyphicon-trash"></span></a>	
			    </td>	
			</tr>

			<!-- Modal of ReadDetail -->

				<div class="modal fade" id="modalReadDetail-<?php echo e($h->id_host); ?>" role="dialog" aria-labelledby="ModalLabel-ReadDetail">
					<div class="modal-dialog">
						<div class="modal-content">
						 	<div class="modal-header">
								<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
								<h2 class="modal-title"><?php echo e($h->hostname); ?></h2>
							</div>
							<div class="modal-body">								
								<ul>
									<li>
										<b>Client name:</b> <?php echo e($h->client->name); ?> 
									</li>
									<li>
										<b>Hostname:</b> <?php echo e($h->hostname); ?>

									</li>
									<li>
										<b>IP Address:</b> <?php echo e($h->ip); ?>

									</li>
									<li>
										<b>Client description:</b> <?php echo e($h->description); ?>

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

				<div class="modal fade" id="modalUpdate-<?php echo e($h->id_host); ?>" role="dialog" aria-labelledby="ModalLabel-Update">
					<div class="modal-dialog">
						<div class="modal-content">
						 	<div class="modal-header">
								<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
								<h2 class="modal-title"><?php echo e($h->hostname); ?></h2>
							</div>
							<form class="form-horizontal" action="<?php echo e(action('HostsController@updateSave')); ?>" method="POST">
								<input type="hidden" name="_token" value="<?php echo e(csrf_token()); ?>" />
								<input type="hidden" name="id_host" value="<?php echo e($h->id_host); ?>"> 
								
								<div class="modal-body">
									<div class="row form-group">
										<div class="col-md-6">
											<div class="input-group">									
												<span class="input-group-addon">Client name</span>
												<select type="id_client" class="form-control" name="id_client">
														<option value="<?php echo e($h->id_client); ?>" selected><?php echo e($h->client->name); ?></option>
														<option disabled>------</option>
													<?php $__currentLoopData = $clients; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $c): $__env->incrementLoopIndices(); $loop = $__env->getFirstLoop(); ?>
														<option value="<?php echo e($c->id_client); ?>"><?php echo e($c->name); ?></option>
													<?php endforeach; $__env->popLoop(); $loop = $__env->getFirstLoop(); ?>
												</select>
											</div>
										</div>
									</div>

									<div class="row form-group">
										<div class="col-md-8 ">
											<div class="input-group">
												<span class="input-group-addon">Hostname</span>
												<input type="hostname" class="form-control" name="hostname" value="<?php echo e($h->hostname); ?>">
											</div>
										</div>
									</div>

									<div class="row form-group">
										<div class="col-md-6 ">
											<div class="input-group">
												<span class="input-group-addon">IP Address</span>
												<input t<input type="ip" class="form-control" name="ip" value="<?php echo e($h->ip); ?>">
											</div>
										</div>
									</div>

									<div class="row form-group">
										<div class="col-md-12 ">
											<div class="input-group">
												<span class="input-group-addon">Description</span>
												<input type="description" class="form-control" name="description" value="<?php echo e($h->description); ?>">
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

			<div class="modal fade" id="modalDelete-<?php echo e($h->id_host); ?>" role="dialog" aria-labelledby="SmallModalLabel-Delete">
				<div class="modal-dialog">
					<div class="modal-content">
					 	<div class="modal-header">
							<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
							<h4 class="modal-title">Confirmation</h4>
						</div>
						<div class="modal-body">
							<h5>Really want to delete the client <bolt><?php echo e($h->hostname); ?></bolt>?</h5>
						</div>
						<div class="modal-footer">
							<a class="btn btn-default" data-dismiss="modal">Close</a>
							<a href="<?php echo e(action('HostsController@delete', [$h->id_host])); ?>" class="btn btn-danger">Delete</a>
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