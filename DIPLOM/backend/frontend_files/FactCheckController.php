<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Article;
use Illuminate\Support\Facades\DB;

class FactCheckController extends Controller
{
    public function index()
    {
        $factChecks = Article::where('status', 'processed')
            ->whereIn('outlet', ['voxukraine', 'stopfake'])
            ->orderBy('published_at', 'desc')
            ->paginate(10);

        return view('factchecks.index', compact('factChecks'));
    }

    public function show($id)
    {
        $factCheck = Article::with(['paragraphs', 'sources', 'categories'])
            ->findOrFail($id);

        return view('factchecks.show', compact('factCheck'));
    }
}
