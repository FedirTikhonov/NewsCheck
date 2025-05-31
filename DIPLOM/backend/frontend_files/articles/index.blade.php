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
                <h2 class="text-2xl border-l-4 border-blue-500 pl-2">Новини</h2>
                <div class="relative">
                    <button id="filterButton" class="p-2 hover:bg-gray-100 rounded">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
                        </svg>
                    </button>
                </div>
            </div>

            <div class="bg-white rounded shadow">
                @forelse ($articles as $article)
                    <div class="border-b last:border-b-0">
                        <div class="flex items-start p-4">
                            <div class="w-20 text-right text-gray-500 pr-6">
                                {{ \Carbon\Carbon::parse($article->published_at)->format('d.m.y H:i') }}
                            </div>
                            <div class="flex-grow">
                                <h3 class="text-lg font-medium">
                                    <a href="{{ route('articles.show', $article->id) }}" class="hover:text-blue-600">
                                        {{ $article->title }}
                                    </a>
                                </h3>
                            </div>
                            <div class="w-32 text-right text-gray-500">
                                {{ $article->outlet }}
                            </div>
                        </div>
                    </div>
                @empty
                    <div class="p-4 text-center text-gray-500">
                        No articles found
                    </div>
                @endforelse
            </div>

            <div class="mt-6">
                {{ $articles->links() }}
            </div>
        </main>
        <div id="filterModal" class="fixed inset-0 bg-black bg-opacity-50 hidden items-center justify-center z-50">
            <div class="bg-white rounded-2xl p-8 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
                <div class="flex justify-between items-center mb-6">
                    <h2 class="text-2xl font-bold">Фільтр новин</h2>
                    <button id="closeModal" class="text-gray-500 hover:text-gray-700">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>

                <form id="filterForm">
                    <div class="mb-8">
                        <h3 class="text-lg font-semibold mb-4">Видання</h3>
                        <div class="grid grid-cols-2 gap-3">
                            <div class="checkbox-container flex items-center cursor-pointer">
                                <input type="checkbox" name="outlets[]" value="ukrinform" class="sr-only">
                                <div class="checkbox-visual w-6 h-6 border-2 border-gray-300 rounded-md flex items-center justify-center mr-3"></div>
                                <span>Укрінформ</span>
                            </div>
                            <div class="checkbox-container flex items-center cursor-pointer">
                                <input type="checkbox" name="outlets[]" value="espreso" class="sr-only">
                                <div class="checkbox-visual w-6 h-6 border-2 border-gray-300 rounded-md flex items-center justify-center mr-3"></div>
                                <span>Еспресо</span>
                            </div>
                            <div class="checkbox-container flex items-center cursor-pointer">
                                <input type="checkbox" name="outlets[]" value="hromadske" class="sr-only">
                                <div class="checkbox-visual w-6 h-6 border-2 border-gray-300 rounded-md flex items-center justify-center mr-3"></div>
                                <span>Громадське</span>
                            </div>
                            <div class="checkbox-container flex items-center cursor-pointer">
                                <input type="checkbox" name="outlets[]" value="radiosvoboda" class="sr-only">
                                <div class="checkbox-visual w-6 h-6 border-2 border-gray-300 rounded-md flex items-center justify-center mr-3"></div>
                                <span>Радіо Свобода</span>
                            </div>
                        </div>
                    </div>
                    <div class="mb-8">
                        <h3 class="text-lg font-semibold mb-4">Емоційне забарвлення</h3>
                        <div class="flex gap-4">
                            <div class="checkbox-container flex items-center cursor-pointer">
                                <input type="checkbox" name="emotionality[]" value="дуже емоційна" class="sr-only">
                                <div class="checkbox-visual w-6 h-6 border-2 border-gray-300 rounded-md flex items-center justify-center mr-3"></div>
                                <span>Дуже емоційні</span>
                            </div>
                            <div class="checkbox-container flex items-center cursor-pointer">
                                <input type="checkbox" name="emotionality[]" value="дещо емоційна" class="sr-only">
                                <div class="checkbox-visual w-6 h-6 border-2 border-gray-300 rounded-md flex items-center justify-center mr-3"></div>
                                <span>Дещо емоційні</span>
                            </div>
                            <div class="checkbox-container flex items-center cursor-pointer">
                                <input type="checkbox" name="emotionality[]" value="нейтральна" class="sr-only">
                                <div class="checkbox-visual w-6 h-6 border-2 border-gray-300 rounded-md flex items-center justify-center mr-3"></div>
                                <span>Нейтральні</span>
                            </div>
                        </div>
                    </div>
                    <div class="mb-8">
                        <h3 class="text-lg font-semibold mb-4">Достовірність джерел</h3>
                        <div class="px-4">
                            <div class="flex justify-between text-sm text-gray-600 mb-2">
                                <span>Анонімні, неперевірені джерела</span>
                                <span>Відомі, перевірені і надійні джерела</span>
                            </div>
                            <div id="credibilitySlider" class="mb-4"></div>
                            <div class="flex justify-between text-xs">
                                <span>1</span>
                                <span>2</span>
                                <span>3</span>
                                <span>4</span>
                                <span>5</span>
                            </div>
                        </div>
                    </div>
                    <div class="mb-8">
                        <h3 class="text-lg font-semibold mb-4">Фактичність</h3>
                        <div class="px-4">
                            <div class="flex justify-between text-sm text-gray-600 mb-2">
                                <span>Стаття базується майже повністю на припущеннях</span>
                                <span>Статя базується і посилається лише на реальні події</span>
                            </div>
                            <div id="factualitySlider" class="mb-4"></div>
                            <div class="flex justify-between text-xs">
                                <span>1</span>
                                <span>2</span>
                                <span>3</span>
                                <span>4</span>
                                <span>5</span>
                            </div>
                        </div>
                    </div>
                    <div class="mb-8">
                        <h3 class="text-lg font-semibold mb-4">"Клікбейти"</h3>
                        <div class="px-4">
                            <div class="flex justify-between text-sm text-gray-600 mb-2">
                                <span>Дуже сенсаційні заголовки</span>
                                <span>Нейтральні заголовки</span>
                            </div>
                            <div id="clickbaitnessSlider" class="mb-4"></div>
                            <div class="flex justify-between text-xs">
                                <span>1</span>
                                <span>2</span>
                                <span>3</span>
                            </div>
                        </div>
                    </div>
                    <div class="flex gap-4 pt-6">
                        <button type="button" id="resetSettings" class="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
                            Скасувати налаштування
                        </button>
                        <button type="button" id="saveSettings" class="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600">
                            Зберегти налаштування
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <style>
        .checkbox-visual.checked {
            background-color: #3b82f6;
            border-color: #3b82f6;
        }

        .checkbox-visual.checked::after {
            content: '✓';
            color: white;
            font-weight: bold;
        }

        .dual-range-container {
            position: relative;
            height: 2rem;
            margin: 1rem 0;
        }

        .slider-track {
            position: absolute;
            top: 50%;
            left: 0;
            right: 0;
            height: 8px;
            background-color: #e5e7eb;
            border-radius: 4px;
            transform: translateY(-50%);
        }

        .slider-range {
            position: absolute;
            top: 50%;
            height: 8px;
            background-color: #3b82f6;
            border-radius: 4px;
            transform: translateY(-50%);
        }

        .slider-handle {
            position: absolute;
            top: 50%;
            width: 1.5rem;
            height: 1.5rem;
            background-color: #3b82f6;
            border: 2px solid white;
            border-radius: 50%;
            cursor: pointer;
            transform: translate(-50%, -50%);
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
    </style>
    <script src="resources/js/filter-modal.js"></script>
@endsection
