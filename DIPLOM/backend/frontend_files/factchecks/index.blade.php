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
            <div class="flex justify-between items-center mb-4">
                <h2 class="text-2xl border-l-4 border-blue-500 pl-2">Викривання фейків</h2>
            </div>

            <div class="bg-white rounded shadow">
                @forelse ($factChecks as $factCheck)
                    <div class="border-b last:border-b-0">
                        <div class="flex items-start p-4">
                            <div class="w-20 text-right text-gray-500 pr-6">
                                {{ \Carbon\Carbon::parse($factCheck->published_at)->format('d.m.y') }}
                            </div>
                            <div class="flex-grow">
                                <h3 class="text-lg font-medium">
                                    <a href="{{ route('factchecks.show', $factCheck->id) }}" class="hover:text-blue-600">
                                        {{ $factCheck->title }}
                                    </a>
                                </h3>
                            </div>
                            <div class="w-32 text-right text-gray-500">
                                {{ $factCheck->outlet }}
                            </div>
                        </div>
                    </div>
                @empty
                    <div class="p-4 text-center text-gray-500">
                        Викривань фейків не знайдено
                    </div>
                @endforelse
            </div>

            <div class="mt-6">
                {{ $factChecks->links() }}
            </div>
        </main>
    </div>
@endsection
