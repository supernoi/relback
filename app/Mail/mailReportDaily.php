<?php

namespace relback\Mail;

use Illuminate\Bus\Queueable;
use Illuminate\Mail\Mailable;
use Illuminate\Queue\SerializesModels;
use Illuminate\Contracts\Queue\ShouldQueue;

class mailReportDaily extends Mailable
{
    use Queueable, SerializesModels;

    /**
     * Create a new message instance.
     *
     * @return void
     */
    public function __construct()
    {
        //teste
    }

    $address = 'juliano.ribeiro@ativas.com.br';
    $name = 'Juliano';
    $subject = 'relBack teste';

    public function build()
    {
        return $this->view('reports.reportsReadMailDaily')
                    ->replyTo($address, $name)
                    ->subject($subject);
    }
}
