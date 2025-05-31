@extends('layouts.app')

@section('content')
    <div class="bg-gray-100 min-h-screen">
        <header class="bg-blue-100 p-4 border-b border-gray-300">
            <div class="container mx-auto flex justify-between items-center">
                <h1 class="text-3xl font-bold">NewsCheck</h1>
                <nav class="space-x-6">
                    <a href="{{ route('articles.index') }}" class="text-black hover:underline">Новини</a>
                    <a href="{{ route('factchecks.index') }}" class="text-black hover:underline">Викривання фейків</a>
                    <a href="{{ route('trends.index') }}" class="text-black hover:underline">Тренди дезінформації</a>
                </nav>
            </div>
        </header>

        <main class="container mx-auto p-4">
            <div class="bg-white rounded shadow p-6">
                <h1 class="text-3xl font-bold mb-2 border-l-4 border-blue-500 pl-4">{{ $article->title }}</h1>

                <div class="mb-4 text-gray-600">
                    Викладено о {{ \Carbon\Carbon::parse($article->published_at)->format('H:i, d F Y') }}
                    <a href="{{ $article->href }}" class="text-blue-500 hover:underline ml-4" target="_blank">
                        Подивитися оригінальну сторінку статті
                    </a>
                </div>

                <div class="prose max-w-none mb-8">
                    @foreach($article->paragraphs as $paragraph)
                        <p class="mb-4">{{ $paragraph->paragraph_text }}</p>
                    @endforeach
                </div>

                @if($article->metric)
                    <div class="border-t border-b py-4 my-6">
                        <h2 class="text-xl font-bold mb-3">Оцінки статті</h2>
                        <div class="flex flex-wrap gap-4">
                            <div class="relative group">
                            <span class="px-3 py-1 rounded-full flex items-center gap-2
                                    {{ strtolower($article->metric->emotionality_score) === 'нейтральна' ? 'bg-green-100 text-green-800' :
                                       (strtolower($article->metric->emotionality_score) === 'дещо емоційна' ? 'bg-yellow-100 text-yellow-800' : 'bg-red-100 text-red-800') }}
                            ">
                                Емоційність:
                                    {{ strtolower($article->metric->emotionality_score) === 'нейтральна' ? 'нейтральна' :
                                       (strtolower($article->metric->emotionality_score) === 'дещо емоційна' ? 'помірна' : 'дуже емоційна') }}
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853l.041-.021M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z" />
                                </svg>
                            </span>
                                <div class="absolute z-10 hidden group-hover:block bg-white border rounded p-3 shadow-lg w-64 text-sm text-gray-700 mt-1">
                                    {{ $article->metric->emotionality_reason ?: 'Немає пояснення' }}
                                </div>
                            </div>

                            <div class="relative group">
                            <span class="px-3 py-1 rounded-full flex items-center gap-2 {{ $article->metric->clickbaitness_score === 3  ? 'bg-green-100 text-green-800' : ($article->metric->clickbaitness_score === 2 ? 'bg-yellow-100 text-yellow-800' : 'bg-red-100 text-red-800') }}">
                                Сенсаційність: {{ $article->metric->clickbaitness_score === 3 ? 'нейтральна' : ($article->metric->clickbaitness_score === 2 ? 'помірна' : 'висока') }}
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853l.041-.021M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z" />
                                </svg>
                            </span>
                                <div class="absolute z-10 hidden group-hover:block bg-white border rounded p-3 shadow-lg w-64 text-sm text-gray-700 mt-1">
                                    {{ $article->metric->clickbaitness_reason ?: 'Немає пояснення' }}
                                </div>
                            </div>

                            <div class="relative group">
                            <span class="px-3 py-1 rounded-full flex items-center gap-2 {{ $article->metric->factuality_score > 3 ? 'bg-green-100 text-green-800' : ($article->metric->factuality_score > 1 ? 'bg-yellow-100 text-yellow-800' : 'bg-red-100 text-red-800') }}">
                                Фактичність: {{ $article->metric->factuality_score > 3 ? 'вище середнього' : ($article->metric->factuality_score > 1 ? 'середня' : 'низька') }}
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853l.041-.021M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z" />
                                </svg>
                            </span>
                                <div class="absolute z-10 hidden group-hover:block bg-white border rounded p-3 shadow-lg w-64 text-sm text-gray-700 mt-1">
                                    {{ $article->metric->factuality_reason ?: 'Немає пояснення' }}
                                </div>
                            </div>

                            <div class="relative group">
                            <span class="px-3 py-1 rounded-full flex items-center gap-2 {{ $article->metric->credibility_score > 3 ? 'bg-green-100 text-green-800' : ($article->metric->credibility_score > 1 ? 'bg-yellow-100 text-yellow-800' : 'bg-red-100 text-red-800') }}">
                                Джерела: {{ $article->metric->credibility_score > 3 ? 'достовірні' : ($article->metric->credibility_score > 1 ? 'сумнівні' : 'недостовірні') }}
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853l.041-.021M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z" />
                                </svg>
                            </span>
                                <div class="absolute z-10 hidden group-hover:block bg-white border rounded p-3 shadow-lg w-64 text-sm text-gray-700 mt-1">
                                    {{ $article->metric->credibility_reason ?: 'Немає пояснення' }}
                                </div>
                            </div>
                        </div>
                    </div>
                @endif

                @if($article->recommendedArticles->count() > 0)
                    <div class="mt-8">
                        <h2 class="text-xl font-bold mb-4">Схожі статті</h2>
                        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                            @foreach($article->recommendedArticles as $recommendedArticle)
                                <div class="border p-4 rounded hover:bg-gray-50">
                                    <h3 class="font-medium">
                                        <a href="{{ route('articles.show', $recommendedArticle->id) }}" class="hover:text-blue-600">
                                            {{ $recommendedArticle->title }}
                                        </a>
                                    </h3>
                                    <div class="text-sm text-gray-500 mt-2">
                                        Видання: {{ $recommendedArticle->outlet }}, {{ \Carbon\Carbon::parse($recommendedArticle->published_at)->format('H:i, d F Y') }}
                                    </div>
                                </div>
                            @endforeach
                        </div>
                    </div>
                @endif

                @if($article->sources && $article->sources->count() > 0)
                    <div class="mt-10 pt-6 border-t">
                        <h2 class="text-xl font-bold mb-4">Джерела</h2>
                        <ol class="list-decimal pl-6 space-y-2">
                            @foreach($article->sources as $source)
                                <li>
                                    @if($source->source_href)
                                        <a href="{{ $source->source_href }}" target="_blank" class="text-blue-600 hover:underline">
                                            {{ $source->source_href }}
                                        </a>
                                    @else
                                        <span class="text-gray-600">Джерело без посилання</span>
                                    @endif
                                </li>
                            @endforeach
                        </ol>
                    </div>
                @endif
            </div>
        </main>
    </div>
@endsection
