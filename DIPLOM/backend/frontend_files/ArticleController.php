<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Article;
use Illuminate\Support\Facades\DB;

class ArticleController extends Controller
{
    public function index(Request $request)
    {
        $query = Article::where('status', 'processed')
            ->whereIn('outlet', ['radiosvoboda', 'hromadske', 'espreso', 'ukrinform']);

        $this->applyFilters($query, $request);

        $articles = $query->orderBy('published_at', 'desc')
            ->paginate(10);

        $articles->appends($request->query());

        return view('articles.index', compact('articles'));
    }

    private function applyFilters($query, Request $request)
    {
        if ($request->has('outlets') && !empty($request->outlets)) {
            $query->whereIn('outlet', $request->outlets);
        }

        if ($request->has('emotionality') && !empty($request->emotionality)) {
            $query->whereHas('metric', function($q) use ($request) {
                $emotionalities = is_array($request->emotionality) ? $request->emotionality : [$request->emotionality];
                $q->whereIn('emotionality_score', $emotionalities);
            });
        }

        if ($request->has('credibility_min') || $request->has('credibility_max')) {
            $query->whereHas('metric', function($q) use ($request) {
                if ($request->has('credibility_min')) {
                    $q->where('credibility_score', '>=', $request->credibility_min);
                }
                if ($request->has('credibility_max')) {
                    $q->where('credibility_score', '<=', $request->credibility_max);
                }
            });
        }

        if ($request->has('factuality_min') || $request->has('factuality_max')) {
            $query->whereHas('metric', function($q) use ($request) {
                if ($request->has('factuality_min')) {
                    $q->where('factuality_score', '>=', $request->factuality_min);
                }
                if ($request->has('factuality_max')) {
                    $q->where('factuality_score', '<=', $request->factuality_max);
                }
            });
        }

        if ($request->has('clickbaitness_min') || $request->has('clickbaitness_max')) {
            $query->whereHas('metric', function($q) use ($request) {
                if ($request->has('clickbaitness_min')) {
                    $q->where('clickbaitness_score', '>=', $request->clickbaitness_min);
                }
                if ($request->has('clickbaitness_max')) {
                    $q->where('clickbaitness_score', '<=', $request->clickbaitness_max);
                }
            });
        }
    }

    public function show($id)
    {
        $article = Article::with([
            'paragraphs',
            'metric',
            'sources',
            'recommendedArticles' => function($query) {
                $query->orderBy('similarity_score', 'desc')
                    ->limit(5);
            }
        ])->findOrFail($id);

        return view('articles.show', compact('article'));
    }
}
