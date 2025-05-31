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
                <h1 class="text-3xl font-bold mb-2 border-l-4 border-blue-500 pl-4">{{ $factCheck->title }}</h1>

                <div class="mb-4 text-gray-600">
                    Викладено о {{ \Carbon\Carbon::parse($factCheck->published_at)->format('H:i, d F Y') }}
                    <a href="{{ $factCheck->href }}" class="text-blue-500 hover:underline ml-4" target="_blank">
                        Подивитися оригінальну сторінку статті
                    </a>
                </div>

                @if($factCheck->categories->count() > 0)
                    <div class="mb-4">
                        <div class="flex flex-wrap gap-2">
                            @foreach($factCheck->categories as $category)
                                <span class="px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-sm">
                                {{ $category->name }}
                            </span>
                            @endforeach
                        </div>
                    </div>
                @endif

                <div class="prose max-w-none mb-8">
                    @foreach($factCheck->paragraphs as $paragraph)
                        <p class="mb-4">{{ $paragraph->paragraph_text }}</p>
                    @endforeach
                </div>

                @if($factCheck->sources && $factCheck->sources->count() > 0)
                    <div class="mt-10 pt-6 border-t">
                        <h2 class="text-xl font-bold mb-4">Джерела</h2>
                        <ol class="list-decimal pl-6 space-y-2">
                            @foreach($factCheck->sources as $source)
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
