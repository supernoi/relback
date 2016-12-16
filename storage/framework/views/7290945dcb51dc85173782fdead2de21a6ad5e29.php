

<?php $__env->startSection('title', 'Reports'); ?>

<?php $__env->startSection('content'); ?>
<div>
	<div class="container container-fluid">
		
		<?php if(old('empty_session_key')): ?>
		  <div class="alert alert-warning">
		    <strong>Warning!</strong> 
		        The log for this scheduler not exist. Possible not run.
		  </div>
		<?php endif; ?>
		<div class="panel panel-default" >
			<div class="panel-heading text-center"><h3>Report Backup Policy</h3></div>	
		
				<table class="table table-striped table-responsive display" id="myTable" >
					<thead>
						<tr>
							<th class="text-center">Policy</th>
							<th class="text-center">Hostname</th>
							<th class="text-center">DB_NAME</th>				
							<th class="text-center">Expected<br>Start</th>
							<th class="text-center">Start<br>Realized</th>
							<th class="text-center">Executed<br>Time</th>
							<th class="text-center">Status</th>				
							<th class="text-center">Destination</th>	
							<th class="text-center">Backup<br>Type</th>						
							<th class="text-center">Details</th>
						</tr>
					</thead>

					<tfoot>
						<tr>
							<!-- space reserved for select-filter -->
							<th></th>
							<th></th>
							<th></th>
							<th></th>
							<th></th>
							<th></th>
							<th></th>
							<th></th>
							<th></th>
						</tr>
					</tfoot>

					<tbody>
					<?php $__currentLoopData = $report; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $r): $__env->incrementLoopIndices(); $loop = $__env->getFirstLoop(); ?>

						<?php if($r->status=='COMPLETED'): ?> 
							<?php  $trStyle = 'success'  ?>
						<?php elseif($r->status=='SCHEDULED'): ?>
							<?php  $trStyle = 'info'  ?>				
						<?php elseif($r->status=='NOT RUN'): ?>
							<?php  $trStyle = 'danger'  ?>							
						<?php elseif($r->status=='RUNNING'): ?> 
							<?php  $trStyle = 'active'  ?>
						<?php elseif($r->status=='COMPLETED WITH WARNINGS'): ?> 
							<?php  $trStyle = 'warning'  ?>
						<?php elseif($r->status=='FAILED'): ?> 
							<?php  $trStyle = 'danger'  ?>
						<?php endif; ?>

						<tr class="<?php echo $trStyle; ?>" style="font-size:12px">
						
							<td class="text-center" > <?php echo $r->id_policy; ?> </td>
							<td class="text-center" > <?php echo $r->hostname; ?> </td>
							<td class="text-center" > <?php echo $r->db_name; ?> </td>
							<td class="text-center" > <?php echo $r->schedule_start; ?> </td>
							<td class="text-center" > <?php echo $r->start_r; ?> </td>							
							<td class="text-center" > <?php echo $r->duration_r; ?> </td>
							<td class="text-center" > <?php echo $r->status; ?> </td>
							<td class="text-center" > <?php echo $r->destination; ?> </td>
							<td class="text-center" > <?php echo $r->backup_type; ?> </td>

							<td class="text-center">

								<?php if( !empty($r->session_key) ): ?>
									<a class="glyphicon glyphicon-eye-open" href="<?php echo action('ReportsController@readLogDetail', [ $r->id_policy, $r->db_key, $r->session_key] ); ?>" />
								<?php else: ?>
									<span class="glyphicon glyphicon-eye-close" />
								<?php endif; ?>									
							</td>
						</tr>
					<?php endforeach; $__env->popLoop(); $loop = $__env->getFirstLoop(); ?>
					</tbody>
				</table>
				
			</div>	
		</div>
	</div>
</div>

<!-- modify select-filter of botton to top table -->
<style type="text/css">
	tfoot {
		display: table-header-group;
	}
</style>

<?php $__env->stopSection(); ?>
<?php echo $__env->make('layout.principal', array_except(get_defined_vars(), array('__data', '__path')))->render(); ?>