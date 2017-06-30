<?php

namespace relback\Http\Controllers;

use relback\Http\Controllers\Controller;

class HomeController extends Controller
{

    public function index()
    {
        return view('home.homeIndex');
    }

    public function about()
    {
        return view('home.homeAboutCreators');
    }
}