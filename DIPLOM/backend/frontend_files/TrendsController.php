<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\WeeklyReport;
use App\Models\WeeklyStats;
use App\Models\Category;
use Carbon\Carbon;
use Illuminate\Support\Facades\DB;

class TrendsController extends Controller
{
    public function index()
    {
        $latestReport = WeeklyReport::orderBy('digest_date', 'desc')->first();

        $reportEndDate = $latestReport ? Carbon::parse($latestReport->digest_date) : Carbon::now();
        $reportStartDate = $reportEndDate->clone()->subDays(6);

        $weeklyStats = WeeklyStats::with('category')
            ->where('date', '>=', Carbon::now()->subWeeks(4)->startOfWeek())
            ->orderBy('date', 'asc')
            ->get();

        $chartData = $this->processChartData($weeklyStats);

        return view('trends.index', compact('latestReport', 'reportStartDate', 'reportEndDate', 'chartData'));
    }

    private function processChartData($weeklyStats)
    {
        $weeklyData = $weeklyStats->groupBy(function($item) {
            return Carbon::parse($item->date)->startOfWeek()->format('Y-m-d');
        });

        $chartData = [];

        foreach ($weeklyData as $week => $stats) {
            $topCategories = $stats->sortByDesc('category_num')->take(3);

            $weekData = [
                'week' => Carbon::parse($week)->subDays(6)->format('d.m-') . Carbon::parse($week)->format('d.m'),
                'categories' => []
            ];

            foreach ($topCategories as $stat) {
                $weekData['categories'][] = [
                    'id' => $stat->category_id,
                    'name' => $stat->category->name,
                    'count' => $stat->category_num];}

            $chartData[] = $weekData;
        }

        return array_slice($chartData, -5);
    }
}
