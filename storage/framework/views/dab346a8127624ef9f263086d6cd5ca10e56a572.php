

<?php $__env->startSection('title', 'Clients'); ?>

<?php $__env->startSection('content'); ?>
<div class="container container-fluid"> 
	<h1>Client list</h1>  
	
	<br>
		<a href="" class="btn btn-primary" data-target="#modalAddNew" data-toggle="modal">Add New</a>
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
						<h2 class="modal-title">Add new Client</h2>
					</div>
					<div class="modal-body">								

						<?php if(count($errors) > 0): ?>
							<div class="alert alert-danger">
								<ul>
									<?php $__currentLoopData = $errors->all(); $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $error): $__env->incrementLoopIndices(); $loop = $__env->getFirstLoop(); ?>
									<li><?php echo e($error); ?></li>
									<?php endforeach; $__env->popLoop(); $loop = $__env->getFirstLoop(); ?>
								</ul>
							</div>
						<?php endif; ?>

						<form class="form-horizontal" action="<?php echo e(action('ClientsController@createAdd')); ?>" method="POST">
							<input type="hidden" name="_token" value="<?php echo e(csrf_token()); ?>" />
							<input type="hidden" name="created_id_user" value="<?php echo e(Auth::id()); ?>">
										
								<div class="row form-group">
									<div class="col-md-8">
										<div class="input-group">									
											<span class="input-group-addon">Client Name</span>
											<input name="name" type="text" class="form-control" value="<?php echo e(old('name')); ?>">
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
							</div>

							<div class="modal-footer">
								<a class="btn btn-default" data-dismiss="modal">Close</a>
								<button class="btn btn-primary" type="submit">Add</button>							
							</div>
						</form>
					</div>
				</div>
			</div>
	<!-- End Modal of addNew -->	


	<?php if(old('name')): ?>
	  <div class="alert alert-success">
	    <strong>Sucess!</strong> 
	        The client <?php echo e(old('name')); ?> was created or updated.
	  </div>
	<?php endif; ?>

	<div class="panel panel-default">
		<table class="table table-striped">
			<tr>
				<td class="text-center"><h4><strong>Client Name</strong></h4></td>
				<td class="text-center"><h4><strong>Description</strong></h4></td>
				<td class="text-center"><h4><strong>Options</strong></h4></td>
			</tr>
		<?php $__currentLoopData = $clients; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $c): $__env->incrementLoopIndices(); $loop = $__env->getFirstLoop(); ?> 
			<tr>
				<td class="text-center"><?php echo e($c->name); ?></td>
				<td class="text-center"><?php echo e($c->description); ?></td>
				<td class="text-center">
					<a href="" data-target="#modalReadDetail-<?php echo e($c->id_client); ?>" id="fetch" data-toggle="modal" ><span class="glyphicon glyphicon-search"></span></a>
					&nbsp&nbsp<a href="" data-target="#modalUpdate-<?php echo e($c->id_client); ?>" id="fetch" data-toggle="modal"><span class="glyphicon glyphicon-pencil"></span></a>
					&nbsp&nbsp<a href="" data-target="#modalDelete-<?php echo e($c->id_client); ?>" id="fetch" data-toggle="modal" ><span class="glyphicon glyphicon-trash"></span></a>	
				</td>
			</tr>

			<!-- Modal of ReadDetail -->
				<div class="modal fade" id="modalReadDetail-<?php echo e($c->id_client); ?>" role="dialog" aria-labelledby="ModalLabel-ReadDetail">
					<div class="modal-dialog">
						<div class="modal-content">
						 	<div class="modal-header">
								<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
								<h2 class="modal-title"><?php echo e($c->name); ?></h2>
							</div>
							<div class="modal-body">								
								<ul>
									<li>
										<b>Client name:</b> <?php echo e($c->name); ?> 
									</li>
									<li>
										<b>Client description:</b> <?php echo e($c->description); ?>

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

				<div class="modal fade" id="modalUpdate-<?php echo e($c->id_client); ?>" role="dialog" aria-labelledby="ModalLabel-Update">
					<div class="modal-dialog">
						<div class="modal-content">
						 	<div class="modal-header">
								<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
								<h2 class="modal-title"><?php echo e($c->name); ?></h2>
							</div>
							<form class="form-horizontal" action="<?php echo e(action('ClientsController@updateSave')); ?>" method="POST">
								<input type="hidden" name="_token" value="<?php echo e(csrf_token()); ?>" />
								<input type="hidden" name="id_client" value="<?php echo e($c->id_client); ?>">
								
								<div class="modal-body">
									<div class="row form-group">
										<div class="col-md-8 ">
											<div class="input-group">
												<span class="input-group-addon">Client name</span>
												<input type="name" class="form-control" name="name" value="<?php echo e($c->name); ?>">
											</div>
										</div>
									</div>

									<div class="row form-group">
										<div class="col-md-12 ">
											<div class="input-group">
												<span class="input-group-addon">Description</span>
												<input type="description" class="form-control" name="description" value="<?php echo e($c->description); ?>">
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

				<div class="modal fade" id="modalDelete-<?php echo e($c->id_client); ?>" role="dialog" aria-labelledby="ModalLabel-Delete">
					<div class="modal-dialog">
						<div class="modal-content">
						 	<div class="modal-header">
								<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
								<h2 class="modal-title">Confirmation</h2>
							</div>
							<div class="modal-body">
								<p>Deleting the <b>Client</b>, all dependent <b>Hosts</b>, <b>Databases</b> and <b>Backup Policies</b> will also be deleted.</p>
								<p>Really want to delete the client <b><?php echo e($c->name); ?></b>?</p>
							</div>
							<div class="modal-footer">
								<a class="btn btn-default" data-dismiss="modal">Close</a>
								<a href="<?php echo e(action('ClientsController@delete', [$c->id_client])); ?>" class="btn btn-danger">Delete</a>
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