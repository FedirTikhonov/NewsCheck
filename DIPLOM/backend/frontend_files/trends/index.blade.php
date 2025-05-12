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
            <div class="flex flex-col lg:flex-row gap-6">
                <!-- Chart Section -->
                <div class="lg:w-1/2">
                    <div class="bg-white rounded shadow p-6">
                        <h2 class="text-2xl font-bold mb-2 border-l-4 border-blue-500 pl-2">
                            Найпопулярніші категорії дезінформації
                        </h2>

                        <div class="relative h-96 mt-6">
                            <canvas id="categoriesChart" class="w-full h-full"></canvas>
                        </div>
                    </div>
                </div>

                <!-- Digest Section -->
                <div class="lg:w-1/2">
                    <div class="bg-white rounded shadow p-6">
                        @if($latestReport)
                            <h2 class="text-2xl font-bold mb-4 border-l-4 border-blue-500 pl-2">
                                Дайджест фейків за тиждень {{ $reportStartDate->format('d.m.Y') }} - {{ $reportEndDate->format('d.m.Y') }}
                            </h2>

                            <div class="prose max-w-none">
                                {!! nl2br(e($latestReport->digest_text)) !!}
                            </div>
                        @else
                            <h2 class="text-2xl font-bold mb-4 border-l-4 border-blue-500 pl-2">
                                Дайджест фейків
                            </h2>

                            <div class="text-gray-500">
                                На даний момент дайджест недоступний.
                            </div>
                        @endif
                    </div>
                </div>
            </div>
        </main>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        const chartData = @json($chartData);

        // Process data for Chart.js
        const labels = chartData.map(week => week.week);
        const categories = {};

        // Get all unique categories
        chartData.forEach(week => {
            week.categories.forEach(category => {
                if (!categories[category.name]) {
                    categories[category.name] = [];
                }
            });
        });

        // Fill data for each category
        Object.keys(categories).forEach(categoryName => {
            chartData.forEach(week => {
                const categoryData = week.categories.find(cat => cat.name === categoryName);
                categories[categoryName].push(categoryData ? categoryData.count : 0);
            });
        });

        // Create datasets with different colors
        const colors = [
            { bg: 'rgba(52, 152, 219, 0.6)', border: 'rgba(52, 152, 219, 1)' },
            { bg: 'rgba(46, 204, 113, 0.6)', border: 'rgba(46, 204, 113, 1)' },
            { bg: 'rgba(155, 89, 182, 0.6)', border: 'rgba(155, 89, 182, 1)' },
            { bg: 'rgba(241, 196, 15, 0.6)', border: 'rgba(241, 196, 15, 1)' },
            { bg: 'rgba(231, 76, 60, 0.6)', border: 'rgba(231, 76, 60, 1)' }
        ];

        const datasets = Object.keys(categories).map((categoryName, index) => ({
            label: categoryName,
            data: categories[categoryName],
            backgroundColor: colors[index % colors.length].bg,
            borderColor: colors[index % colors.length].border,
            borderWidth: 1
        }));

        const ctx = document.getElementById('categoriesChart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: datasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 5
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Тиждень'
                        }
                    }
                },
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: false
                    }
                }
            }
        });
    </script>
@endsection
