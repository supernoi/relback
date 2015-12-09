<?php

namespace relback\Console;

use Illuminate\Console\Scheduling\Schedule;
use Illuminate\Foundation\Console\Kernel as ConsoleKernel;
use Illuminate\Support\Facades\DB;

class Kernel extends ConsoleKernel
{

    protected $commands = [
        \relback\Console\Commands\Inspire::class,
    ];

    protected function schedule(Schedule $schedule)
    {
        $schedule->call(function()
        {
            DB::statement('call RELBACK.SP_CREATE_SCHEDULE(sysdate-7)');
        })->twiceDaily(0, 6, 12, 18);
            //->sendOutputTo(storage_path() . "logs/exec_sp_create_schedule.log");
            //->twiceDaily(0, 6, 12, 18)
    }
}
