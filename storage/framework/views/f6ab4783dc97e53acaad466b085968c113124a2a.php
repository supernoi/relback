

<?php $__env->startSection('title', 'Backup Policies'); ?>

<?php $__env->startSection('content'); ?>

	<div class="container container-fluid"> 
		<h1>Backup Policy list</h1>  
		
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

		<!-- Modal of ReadDetail -->

		<div class="modal fade" id="modalAddNew" role="dialog" aria-labelledby="ModalLabel-ReadDetail">
			<div class="modal-dialog modal-lg">
				<div class="modal-content">
				 	<div class="modal-header">
						<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
						<h2 class="modal-title">Add new Backup Policy</h2>
					</div>
					<div class="modal-body">
						
						<form class="form-horizontal" action="<?php echo e(action('PoliciesController@createAdd')); ?>" method="POST">
							<input type="hidden" name="_token" value="<?php echo e(csrf_token()); ?>" />

							<input type="hidden" name="created_id_user" value="<?php echo e(Auth::id()); ?>">

							<div class="form-group">

								<div class="col-md-3">
									<div class="input-group">
											<span class="input-group-addon">Status</span>					
											<select type="status" class="form-control" name="status">
												<option value="ACTIVE">ACTIVE</option>
												<option value="INACTIVE">INACTIVE</option>
											</select>
									</div>
								</div>

								<div class="col-md-9">
									<div class="input-group">
										<span class="input-group-addon">Policy Name</span>					
										<input name="policy_name" type="text" class="form-control" value="<?php echo e(old('policy_name')); ?>">
									</div>
								</div>
							</div>
							
							<div class="form-group">

								<div class="col-md-4">
									<div class="input-group">									
										<span class="input-group-addon">Client name</span>
										<select type="id_client" class="form-control" name="id_client">
											<?php $__currentLoopData = $clients; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $c): $__env->incrementLoopIndices(); $loop = $__env->getFirstLoop(); ?>
												<option value="<?php echo e($c->id_client); ?>"><?php echo e($c->name); ?></option>
											<?php endforeach; $__env->popLoop(); $loop = $__env->getFirstLoop(); ?>
										</select>
									</div>
								</div>

								<div class="col-md-4">
									<div class="input-group">									
										<span class="input-group-addon">Hostname</span>
										<select type="id_host" class="form-control" name="id_host">
											<?php $__currentLoopData = $hostnames; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $h): $__env->incrementLoopIndices(); $loop = $__env->getFirstLoop(); ?>
												<option value="<?php echo e($h->id_host); ?>"><?php echo e($h->hostname); ?></option>
											<?php endforeach; $__env->popLoop(); $loop = $__env->getFirstLoop(); ?>
										</select>
									</div>
								</div>

								<div class="col-md-4">
									<div class="input-group">									
										<span class="input-group-addon">Database(DB_NAME)</span>
										<select type="id_database" class="form-control" name="id_database">
											<?php $__currentLoopData = $databases; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $d): $__env->incrementLoopIndices(); $loop = $__env->getFirstLoop(); ?>
												<option value="<?php echo e($d->id_database); ?>"><?php echo e($d->db_name); ?></option>
											<?php endforeach; $__env->popLoop(); $loop = $__env->getFirstLoop(); ?>
										</select>
									</div>
								</div>
							</div>

							<div class="form-group">
								<div class="col-md-6">
									<div class="input-group">									
										<span class="input-group-addon">Backup Type</span>
										<select type="backup_type" class="form-control" name="backup_type">
											<option value="ARCHIVELOG">ARCHIVELOG</option>
											<option value="DB FULL">DB FULL</option>
											<option value="DB INCR">DB INCR</option>
											<option value="RECVR AREA">RECVR AREA</option>
											<option value="BACKUPSET">BACKUPSET</option>
										</select>
									</div>
								</div>

								<div class="col-md-6">
									<div class="input-group">									
										<span class="input-group-addon">Destination</span>
										<select type="destination" class="form-control" name="destination">
											<option value="SBT_TAPE">SBT_TAPE</option>
											<option value="DISK">DISK</option>
										</select>
									</div>
								</div>
							</div>

							<div class="form-group">

								<div class="col-md-2">
										<div class="input-group">
												<span class="input-group-addon">Minute</span>					
												<input name="minute" type="text" class="form-control" value="<?php echo e(old('minute', '*')); ?>">
										</div>
									</div>

								<div class="col-md-2">
									<div class="input-group">
											<span class="input-group-addon">Hour</span>					
											<input name="hour" type="text" class="form-control" value="<?php echo e(old('hour', '*')); ?>">
									</div>
								</div>

								<div class="col-md-2">
									<div class="input-group">
											<span class="input-group-addon">Day</span>					
											<input name="day" type="text" class="form-control" value="<?php echo e(old('day', '*')); ?>">
									</div>
								</div>

								<div class="col-md-3">
									<div class="input-group">
											<span class="input-group-addon">Day Month</span>					
											<input name="month" type="text" class="form-control" value="<?php echo e(old('month', '*')); ?>">
									</div>
								</div>

								<div class="col-md-3">
									<div class="input-group">
											<span class="input-group-addon">Day Week</span>					
											<input name="day_week" type="text" class="form-control" value="<?php echo e(old('day_week', '*')); ?>">
									</div>
								</div>

							</div>

							<div class="form-group">
								<div class="col-md-6">
									<div class="input-group">
											<span class="input-group-addon">Duration Estimate</span>					
											<input name="duration" type="text" class="form-control" value="<?php echo e(old('duration')); ?>">
									</div>
								</div>

								<div class="col-md-6">
									<div class="input-group">
											<span class="input-group-addon">Backup Size Estimate</span>					
											<input name="size_backup" type="text" class="form-control" value="<?php echo e(old('size_backup')); ?>">
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

		<!-- End Modal of ReadDetail -->

		<?php if(old('id_policy')): ?>
		  <div class="alert alert-success">
		    <strong>Sucess!</strong> 
		        The Policy number <?php echo e(old('id_policy')); ?> was created or updated.
		  </div>
		<?php endif; ?>
		<div class="panel panel-default">
			<table class="table table-striped">
				<tr>
					<th class="text-center">Id Policy</th class="text-center">
					<th class="text-center">Hostname</th class="text-center">
					<th class="text-center">DB_NAME</th class="text-center">
					<th class="text-center">Backup Type</th class="text-center">
					<th class="text-center">Status</th class="text-center">
					<th class="text-center">Description</th class="text-center">
					<th class="text-center">Option</th class="text-center">	

				</tr>
			<?php $__currentLoopData = $policies; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $p): $__env->incrementLoopIndices(); $loop = $__env->getFirstLoop(); ?> 
				<tr>
					<td class="text-center"><?php echo e($p->id_policy); ?></td>
					<td class="text-center"><?php echo e($p->host->hostname); ?></td>
					<td class="text-center"><?php echo e($p->database->db_name); ?></td>
					<td class="text-center"><?php echo e($p->backup_type); ?></td>
					<td class="text-center"><?php echo e($p->status); ?></td>
					<td class="text-center"><?php echo e($p->description); ?></td>
				    <td class="text-center">
						<a href="" data-target="#modalReadDetail-<?php echo e($p->id_policy); ?>" id="fetch" data-toggle="modal"><span class="glyphicon glyphicon-search"></span></a>
						&nbsp&nbsp<a href="" data-target="#modalUpdate-<?php echo e($p->id_policy); ?>" id="fetch" data-toggle="modal"><span class="glyphicon glyphicon-pencil"></span></a>
						&nbsp&nbsp<a href="" data-target="#modalDelete-<?php echo e($p->id_policy); ?>" id="fetch" data-toggle="modal"><span class="glyphicon glyphicon-trash"></span></a>	
				    </td>	
				</tr>
				
				<!-- Modal of ReadDetail -->

				<div class="modal fade" id="modalReadDetail-<?php echo e($p->id_policy); ?>" role="dialog" aria-labelledby="ModalLabel-ReadDetail">
					<div class="modal-dialog">
						<div class="modal-content">
						 	<div class="modal-header">
								<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
								<h2 class="modal-title"><?php echo e($p->policy_name); ?></h2>
							</div>
							<div class="modal-body">								
								<ul>
									<li>
										<b>Id Policy:</b> <?php echo e($p->id_policy); ?> 
									</li>
									<li>
										<b>Client name:</b> <?php echo e($p->client->name); ?> 
									</li>
									<li>
										<b>Database(DB_NAME):</b> <?php echo e($p->database->db_name); ?> 
									</li>
									<li>
										<b>Hostname:</b> <?php echo e($p->host->hostname); ?>

									</li>
									<li>
										<b>Backup Type:</b> <?php echo e($p->backup_type); ?>

									</li>
									<li>
										<b>Destination:</b> <?php echo e($p->destination); ?>

									</li>
									<li>
										<b>Minute:</b> <?php echo e($p->minute); ?>

									</li>
									<li>
										<b>Hour:</b> <?php echo e($p->hour); ?>

									</li>
									<li>
										<b>Day:</b> <?php echo e($p->day); ?>

									</li>
									<li>
										<b>Month:</b> <?php echo e($p->month); ?>

									</li>
									<li>
										<b>Day Week:</b> <?php echo e($p->day_week); ?>

									</li>
									<li>
										<b>Duration Estimate:</b> <?php echo e($p->duration); ?>

									</li>
									<li>
										<b>Backup Size Estimate:</b> <?php echo e($p->size_backup); ?>

									</li>
									<li>
										<b>Status:</b> <?php echo e($p->status); ?>

									</li>
									<li>
										<b>Description:</b> <?php echo e($p->description); ?>

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

				<div class="modal fade" id="modalUpdate-<?php echo e($p->id_policy); ?>" role="dialog" aria-labelledby="ModalLabel-Update">
					<div class="modal-dialog modal-lg">
						<div class="modal-content">
						 	<div class="modal-header">
								<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
								<h2 class="modal-title"><?php echo e($p->policy_name); ?></h2>
							</div>

							<div class="modal-body">
								<form class="form-horizontal" action="<?php echo e(action('PoliciesController@updateSave')); ?>" method="POST">
									<input type="hidden" name="_token" value="<?php echo e(csrf_token()); ?>" />

									<input type="hidden" name="id_policy" value="<?php echo e($p->id_policy); ?>">
									<input type="hidden" name="updated_id_user" value="<?php echo e(Auth::id()); ?>">

										<div class="row form-group">

											<div class="col-md-3">
												<div class="input-group">
														<span class="input-group-addon">Status</span>					
														<select type="status" class="form-control" name="status">
															<option value="<?php echo e($p->status); ?>"><?php echo e($p->status); ?></option>
															<option value="">------</option>
															<option value="ACTIVE">ACTIVE</option>
															<option value="INACTIVE">INACTIVE</option>
														</select>
												</div>
											</div>

											<div class="col-md-9">
												<div class="input-group">
														<span class="input-group-addon">Policy Name</span>					
														<input name="policy_name" type="text" class="form-control" value="<?php echo e($p->policy_name); ?>">
												</div>
											</div>
										</div>
										
										<div class="row form-group">

											<div class="col-md-4">
												<div class="input-group">									
													<span class="input-group-addon">Client name</span>
													<select type="id_client" class="form-control" name="id_client">
														<option value="<?php echo e($p->id_client); ?>" selected><?php echo e($p->client->name); ?></option>
														<option value="">------</option>
														<?php $__currentLoopData = $clients; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $c): $__env->incrementLoopIndices(); $loop = $__env->getFirstLoop(); ?>
															<option value="<?php echo e($c->id_client); ?>"><?php echo e($c->name); ?></option>
														<?php endforeach; $__env->popLoop(); $loop = $__env->getFirstLoop(); ?>
													</select>
												</div>
											</div>

											<div class="col-md-4">
												<div class="input-group">									
													<span class="input-group-addon">Hostname</span>
													<select type="id_host" class="form-control" name="id_host">
														<option value="<?php echo e($p->host->id_host); ?>" selected><?php echo e($p->host->hostname); ?></option>
														<option value="">------</option>
														<?php $__currentLoopData = $hostnames; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $h): $__env->incrementLoopIndices(); $loop = $__env->getFirstLoop(); ?>
															<option value="<?php echo e($h->id_host); ?>"><?php echo e($h->hostname); ?></option>
														<?php endforeach; $__env->popLoop(); $loop = $__env->getFirstLoop(); ?>
													</select>
												</div>
											</div>

											<div class="col-md-4">
												<div class="input-group">									
													<span class="input-group-addon">Database(DB_NAME)</span>
													<select type="id_database" class="form-control" name="id_database">
														<option value="<?php echo e($p->id_database); ?>" selected><?php echo e($p->database->db_name); ?></option>
														<option value="">------</option>
														<?php $__currentLoopData = $databases; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $d): $__env->incrementLoopIndices(); $loop = $__env->getFirstLoop(); ?>
															<option value="<?php echo e($d->id_database); ?>"><?php echo e($d->db_name); ?></option>
														<?php endforeach; $__env->popLoop(); $loop = $__env->getFirstLoop(); ?>
													</select>
												</div>
											</div>
										</div>

										<div class="row form-group">
											<div class="col-md-6">
												<div class="input-group">									
													<span class="input-group-addon">Backup Type</span>
													<select type="backup_type" class="form-control" name="backup_type">
														<option value="<?php echo e($p->backup_type); ?>"><?php echo e($p->backup_type); ?></option>
														<option value="">------</option>
														<option value="ARCHIVELOG">ARCHIVELOG</option>
														<option value="DB FULL">DB FULL</option>
														<option value="DB INCR">DB INCR</option>
														<option value="RECVR AREA">RECVR AREA</option>
														<option value="BACKUPSET">BACKUPSET</option>
													</select>
												</div>
											</div>

											<div class="col-md-6">
												<div class="input-group">									
													<span class="input-group-addon">Destination</span>
													<select type="destination" class="form-control" name="destination">
														<option value="<?php echo e($p->destination); ?>"><?php echo e($p->destination); ?></option>
														<option value="">="">------</</option>
														<option value="SBT_TAPE">SBT_TAPE</option>
														<option value="DISK">DISK</option>
													</select>
												</div>
											</div>
										</div>

										<div class="row form-group">
											<div class="col-md-2">
												<div class="input-group">
														<span class="input-group-addon">Minute</span>					
														<input name="minute" type="text" class="form-control" value="<?php echo e($p->minute); ?>">
												</div>
											</div>

											<div class="col-md-2">
												<div class="input-group">
														<span class="input-group-addon">Hour</span>					
														<input name="hour" type="text" class="form-control" value="<?php echo e($p->hour); ?>">
												</div>
											</div>

											<div class="col-md-2">
												<div class="input-group">
														<span class="input-group-addon">Day</span>					
														<input name="day" type="text" class="form-control" value="<?php echo e($p->day); ?>">
												</div>
											</div>

											<div class="col-md-2">
												<div class="input-group">
														<span class="input-group-addon">Month</span>					
														<input name="month" type="text" class="form-control" value="<?php echo e($p->month); ?>">
												</div>
											</div>

											<div class="col-md-4">
												<div class="input-group">
														<span class="input-group-addon">Day Week</span>					
														<input name="day_week" type="text" class="form-control" value="<?php echo e($p->day_week); ?>">
												</div>
											</div>
										</div>

										<div class="row form-group">
											<div class="col-md-6">
												<div class="input-group">
														<span class="input-group-addon">Duration Estimate</span>					
														<input name="duration" type="text" class="form-control" value="<?php echo e($p->duration); ?>">
												</div>
											</div>							

											<div class="col-md-6">
												<div class="input-group">
														<span class="input-group-addon">Backup Size Estimate</span>					
														<input name="size_backup" type="text" class="form-control" value="<?php echo e($p->size_backup); ?>">
												</div>
											</div>
										</div>

										<div class="row form-group">
											<div class="col-md-12">
												<div class="input-group">
														<span class="input-group-addon">Description</span>					
														<input name="description" type="text" class="form-control" value="<?php echo e($p->description); ?>">
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
				</div>

			<!-- Modal of Delete -->

				<div class="modal fade" id="modalDelete-<?php echo e($p->id_policy); ?>" role="dialog" aria-labelledby="SmallModalLabel-Delete">
					<div class="modal-dialog">
						<div class="modal-content">
						 	<div class="modal-header">
								<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
								<h4 class="modal-title">Confirmation</h4>
							</div>
							<div class="modal-body">
								<h5>Really want to delete the client <b><?php echo e($p->policy_name); ?></b>?</h5>
							</div>
							<div class="modal-footer">
								<a class="btn btn-default" data-dismiss="modal">Close</a>
								<a href="<?php echo e(action('PoliciesController@delete', [$p->id_policy])); ?>" class="btn btn-danger">Delete</a>
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