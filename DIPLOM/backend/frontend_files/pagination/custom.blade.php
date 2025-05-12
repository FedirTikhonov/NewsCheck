@if ($paginator->hasPages())
    <nav class="flex justify-center">
        <ul class="flex space-x-1">
            {{-- Previous Page Link --}}
            @if ($paginator->onFirstPage())
                <li class="px-3 py-1 border bg-gray-100 text-gray-400" aria-disabled="true">
                    &lsaquo;
                </li>
            @else
                <li>
                    <a href="{{ $paginator->previousPageUrl() }}" class="px-3 py-1 border bg-white hover:bg-gray-50" rel="prev">
                        &lsaquo;
                    </a>
                </li>
            @endif

            {{-- Pagination Elements --}}
            @foreach ($elements as $element)
                {{-- "Three Dots" Separator --}}
                @if (is_string($element))
                    <li class="px-3 py-1 border bg-white" aria-disabled="true">
                        {{ $element }}
                    </li>
                @endif

                {{-- Array Of Links --}}
                @if (is_array($element))
                    @foreach ($element as $page => $url)
                        @if ($page == $paginator->currentPage())
                            <li class="px-3 py-1 border bg-gray-200" aria-current="page">
                                {{ $page }}
                            </li>
                        @else
                            <li>
                                <a href="{{ $url }}" class="px-3 py-1 border bg-white hover:bg-gray-50">
                                    {{ $page }}
                                </a>
                            </li>
                        @endif
                    @endforeach
                @endif
            @endforeach

            {{-- Next Page Link --}}
            @if ($paginator->hasMorePages())
                <li>
                    <a href="{{ $paginator->nextPageUrl() }}" class="px-3 py-1 border bg-white hover:bg-gray-50" rel="next">
                        &rsaquo;
                    </a>
                </li>
            @else
                <li class="px-3 py-1 border bg-gray-100 text-gray-400" aria-disabled="true">
                    &rsaquo;
                </li>
            @endif
        </ul>
    </nav>
@endif
