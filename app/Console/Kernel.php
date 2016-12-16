<?php

namespace relback\Console;

use Illuminate\Console\Scheduling\Schedule;
use Illuminate\Foundation\Console\Kernel as ConsoleKernel;
use Illuminate\Support\Facades\DB;
use Mail;

use View;
use relback\Http\Controllers\ReportsMailController;

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

        $schedule->call(function()
        {
            $mailData = new ReportsMailController();
            $data = $mailData->mailDataDaily();

            Mail::send('reports.reportsReadMailDaily', array('reportMailDefault' => $data), function($message)
            {
                $message->to('juliano.ribeiro@ativas.com.br')->subject('relBackMail');
            });
        })->twiceDaily(0, 6, 12, 18)->everyMinute(2);      
    }
}
