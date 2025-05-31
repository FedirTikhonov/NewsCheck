document.addEventListener('DOMContentLoaded', function() {
            console.log('DOM Content Loaded - Filter Modal Script Starting');

            const filterButton = document.getElementById('filterButton');
            const filterModal = document.getElementById('filterModal');
            const closeModal = document.getElementById('closeModal');
            const resetSettings = document.getElementById('resetSettings');
            const saveSettings = document.getElementById('saveSettings');

            let sliders = {};

            function showModal() {
                if (filterModal) {
                    filterModal.style.display = 'flex';
                    filterModal.classList.remove('hidden');
                    filterModal.classList.add('flex');
                }
            }

            function hideModal() {
                if (filterModal) {
                    filterModal.style.display = 'none';
                    filterModal.classList.add('hidden');
                    filterModal.classList.remove('flex');
                }
            }

            function initFilterModal() {
                const containers = document.querySelectorAll('.checkbox-container');

                containers.forEach((container, index) => {
                    if (container.hasAttribute('data-listener-attached')) {
                        console.log(`Container ${index} already has listener, skipping...`);
                        return;
                    }

                    const checkbox = container.querySelector('input[type="checkbox"]');
                    const visual = container.querySelector('.checkbox-visual');

                    console.log(`Setting up container ${index}:`, {
                        checkbox: checkbox,
                        visual: visual,
                        checkboxValue: checkbox?.value || 'NO VALUE'
                    });

                    container.addEventListener('click', function(e) {
                        e.preventDefault();
                        e.stopPropagation();

                        console.log(`Container ${index} clicked! Timestamp: ${Date.now()}`, {
                            target: e.target,
                            currentTarget: e.currentTarget,
                            checkboxBefore: checkbox.checked
                        });

                        checkbox.checked = !checkbox.checked;

                        console.log(`Checkbox ${index} toggled to:`, checkbox.checked);

                        updateCheckboxVisual(checkbox, visual);
                    });

                    container.setAttribute('data-listener-attached', 'true');

                    checkbox.addEventListener('change', function(e) {
                        console.log(`Checkbox ${index} changed directly:`, checkbox.checked);
                        updateCheckboxVisual(checkbox, visual);
                    });

                    updateCheckboxVisual(checkbox, visual);
                });

                initializeSliders();
            }

            function updateCheckboxVisual(checkbox, visual) {
                console.log('Updating checkbox visual:', {
                    checked: checkbox.checked,
                    visualElement: visual,
                    currentClasses: visual.className
                });

                if (checkbox.checked) {
                    visual.classList.add('checked');
                    console.log('Added "checked" class');
                } else {
                    visual.classList.remove('checked');
                    console.log('Removed "checked" class');
                }

                console.log('Visual classes after update:', visual.className);
            }

            function initializeSliders() {
                console.log('Initializing sliders...');

                const credibilityContainer = document.getElementById('credibilitySlider');
                if (credibilityContainer && !credibilityContainer.hasAttribute('data-slider-initialized')) {
                    sliders.credibility = new DualRangeSlider(credibilityContainer, {
                        name: 'credibility',
                        min: 1,
                        max: 5,
                        minValue: 1,
                        maxValue: 5
                    });
                    credibilityContainer.setAttribute('data-slider-initialized', 'true');
                }

                const factualityContainer = document.getElementById('factualitySlider');
                if (factualityContainer && !factualityContainer.hasAttribute('data-slider-initialized')) {
                    sliders.factuality = new DualRangeSlider(factualityContainer, {
                        name: 'factuality',
                        min: 1,
                        max: 5,
                        minValue: 1,
                        maxValue: 5
                    });
                    factualityContainer.setAttribute('data-slider-initialized', 'true');
                }

                const clickbaitnessContainer = document.getElementById('clickbaitnessSlider');
                if (clickbaitnessContainer && !clickbaitnessContainer.hasAttribute('data-slider-initialized')) {
                    sliders.clickbaitness = new DualRangeSlider(clickbaitnessContainer, {
                        name: 'clickbaitness',
                        min: 1,
                        max: 3,
                        minValue: 1,
                        maxValue: 3
                    });
                    clickbaitnessContainer.setAttribute('data-slider-initialized', 'true');
                }
            }

            if (filterButton && !filterButton.hasAttribute('data-listener-attached')) {
                filterButton.addEventListener('click', function(e) {
                    console.log('Filter button clicked!', e);
                    e.preventDefault();
                    e.stopPropagation();
                    showModal();
                    loadCurrentFilters();
                });
                filterButton.setAttribute('data-listener-attached', 'true');
                console.log('Filter button listener attached');
            } else {
                console.log('Filter button not found or already has listener');
            }

            if (closeModal && !closeModal.hasAttribute('data-listener-attached')) {
                closeModal.addEventListener('click', function(e) {
                    console.log('Close modal clicked');
                    e.preventDefault();
                    e.stopPropagation();
                    hideModal();
                });
                closeModal.setAttribute('data-listener-attached', 'true');
            }

            if (filterModal && !filterModal.hasAttribute('data-listener-attached')) {
                filterModal.addEventListener('click', function(e) {
                    if (e.target === filterModal) {
                        console.log('Modal background clicked');
                        hideModal();
                    }
                });
                filterModal.setAttribute('data-listener-attached', 'true');
            }

            if (resetSettings && !resetSettings.hasAttribute('data-listener-attached')) {
                resetSettings.addEventListener('click', function(e) {
                    console.log('Reset settings clicked');
                    e.preventDefault();

                    document.querySelectorAll('input[type="checkbox"]').forEach((checkbox, index) => {
                        console.log(`Resetting checkbox ${index}`);
                        checkbox.checked = false;
                        const visual = checkbox.closest('.checkbox-container')?.querySelector('.checkbox-visual');
                        if (visual) visual.classList.remove('checked');
                    });

                    Object.values(sliders).forEach(slider => slider.reset());
                });
                resetSettings.setAttribute('data-listener-attached', 'true');
            }

            if (saveSettings && !saveSettings.hasAttribute('data-listener-attached')) {
                saveSettings.addEventListener('click', function(e) {
                    console.log('Save settings clicked');
                    e.preventDefault();
                    applyFilters();
                    hideModal();
                });
                saveSettings.setAttribute('data-listener-attached', 'true');
            }

            function loadCurrentFilters() {
                console.log('Loading current filters...');
                const urlParams = new URLSearchParams(window.location.search);

                const outlets = urlParams.getAll('outlets[]') || [];
                console.log('Loading outlets:', outlets);
                outlets.forEach(outlet => {
                    const checkbox = document.querySelector(`input[name="outlets[]"][value="${outlet}"]`);
                    if (checkbox) {
                        checkbox.checked = true;
                        const visual = checkbox.closest('.checkbox-container').querySelector('.checkbox-visual');
                        visual.classList.add('checked');
                    }
                });

                const emotionality = urlParams.getAll('emotionality[]');
                console.log('Loading emotionality:', emotionality);
                emotionality.forEach(value => {
                    const checkbox = document.querySelector(`input[name="emotionality[]"][value="${value}"]`);
                    if (checkbox) {
                        checkbox.checked = true;
                        const visual = checkbox.closest('.checkbox-container').querySelector('.checkbox-visual');
                        visual.classList.add('checked');
                    }
                });

                ['credibility', 'factuality', 'clickbaitness'].forEach(metric => {
                    const minValue = urlParams.get(`${metric}_min`);
                    const maxValue = urlParams.get(`${metric}_max`);

                    if (sliders[metric] && (minValue || maxValue)) {
                        sliders[metric].setValues(
                            minValue ? parseInt(minValue) : sliders[metric].options.min,
                            maxValue ? parseInt(maxValue) : sliders[metric].options.max
                        );
                    }
                });
            }

            function applyFilters() {
                console.log('Applying filters...');
                const form = document.getElementById('filterForm');
                const formData = new FormData(form);
                const urlParams = new URLSearchParams();

                const outlets = formData.getAll('outlets[]');
                console.log('Selected outlets:', outlets);
                outlets.forEach(outlet => urlParams.append('outlets[]', outlet));

                const emotionality = formData.getAll('emotionality[]');
                console.log('Selected emotionality:', emotionality);
                emotionality.forEach(value => urlParams.append('emotionality[]', value));

                ['credibility', 'factuality', 'clickbaitness'].forEach(metric => {
                    const minValue = formData.get(`${metric}_min`);
                    const maxValue = formData.get(`${metric}_max`);

                    if (minValue && minValue !== sliders[metric].options.min.toString()) {
                        urlParams.set(`${metric}_min`, minValue);
                    }
                    if (maxValue && maxValue !== sliders[metric].options.max.toString()) {
                        urlParams.set(`${metric}_max`, maxValue);
                    }
                });

                console.log('Final URL params:', urlParams.toString());

                const currentPath = window.location.pathname;
                window.location.href = `${currentPath}?${urlParams.toString()}`;
            }

            console.log('Starting initialization...');
            initFilterModal();
            console.log('Initialization complete!');

            window.filterModalInitialized = true;
        });

        class DualRangeSlider {
            constructor(container, options = {}) {
                this.container = container;
                this.options = {
                    min: options.min || 1,
                    max: options.max || 5,
                    step: options.step || 1,
                    minValue: options.minValue || options.min || 1,
                    maxValue: options.maxValue || options.max || 5,
                    name: options.name || 'range',
                    ...options
                };

                this.initialMin = this.options.minValue;
                this.initialMax = this.options.maxValue;
                this.isDragging = false;
                this.activeHandle = null;

                this.init();
            }

            init() {
                this.createSlider();
                this.bindEvents();
                this.updateVisual();
            }

            createSlider() {
                this.container.classList.add('dual-range-container');
                this.container.innerHTML = `
            <div class="slider-track"></div>
            <div class="slider-range"></div>
            <div class="slider-handle" data-handle="min"></div>
            <div class="slider-handle" data-handle="max"></div>
            <input type="hidden" name="${this.options.name}_min" class="min-input" value="${this.options.minValue}">
            <input type="hidden" name="${this.options.name}_max" class="max-input" value="${this.options.maxValue}">
        `;

                this.track = this.container.querySelector('.slider-track');
                this.range = this.container.querySelector('.slider-range');
                this.minHandle = this.container.querySelector('[data-handle="min"]');
                this.maxHandle = this.container.querySelector('[data-handle="max"]');
                this.minInput = this.container.querySelector('.min-input');
                this.maxInput = this.container.querySelector('.max-input');
            }

            bindEvents() {
                this.minHandle.addEventListener('mousedown', this.startDrag.bind(this, 'min'));
                this.maxHandle.addEventListener('mousedown', this.startDrag.bind(this, 'max'));

                // Bind global events
                this.onDragBound = this.onDrag.bind(this);
                this.stopDragBound = this.stopDrag.bind(this);
            }

            startDrag(handle, e) {
                e.preventDefault();
                this.activeHandle = handle;
                this.isDragging = true;
                this.startX = e.clientX;
                this.trackRect = this.track.getBoundingClientRect();
                this.startValue = this.options[handle + 'Value'];

                document.addEventListener('mousemove', this.onDragBound);
                document.addEventListener('mouseup', this.stopDragBound);
            }

            onDrag(e) {
                if (!this.isDragging) return;

                const deltaX = e.clientX - this.startX;
                const trackWidth = this.trackRect.width;
                const deltaRatio = deltaX / trackWidth;
                const valueRange = this.options.max - this.options.min;
                const deltaValue = deltaRatio * valueRange;

                if (this.activeHandle === 'min') {
                    let newValue = this.startValue + deltaValue;
                    newValue = Math.round(newValue / this.options.step) * this.options.step;
                    newValue = Math.max(this.options.min, Math.min(newValue, this.options.maxValue));
                    this.options.minValue = newValue;
                } else {
                    let newValue = this.startValue + deltaValue;
                    newValue = Math.round(newValue / this.options.step) * this.options.step;
                    newValue = Math.max(this.options.minValue, Math.min(newValue, this.options.max));
                    this.options.maxValue = newValue;
                }

                this.updateVisual();
                this.updateInputs();
            }

            stopDrag() {
                this.isDragging = false;
                this.activeHandle = null;

                document.removeEventListener('mousemove', this.onDragBound);
                document.removeEventListener('mouseup', this.stopDragBound);
            }

            updateVisual() {
                const minPercent = ((this.options.minValue - this.options.min) / (this.options.max - this.options.min)) * 100;
                const maxPercent = ((this.options.maxValue - this.options.min) / (this.options.max - this.options.min)) * 100;

                this.minHandle.style.left = `${minPercent}%`;
                this.maxHandle.style.left = `${maxPercent}%`;
                this.range.style.left = `${minPercent}%`;
                this.range.style.width = `${maxPercent - minPercent}%`;
            }

            updateInputs() {
                this.minInput.value = this.options.minValue;
                this.maxInput.value = this.options.maxValue;
            }

            setValues(min, max) {
                this.options.minValue = Math.max(this.options.min, Math.min(min, this.options.max));
                this.options.maxValue = Math.max(this.options.min, Math.min(max, this.options.max));
                this.updateVisual();
                this.updateInputs();
            }

            reset() {
                this.options.minValue = this.initialMin;
                this.options.maxValue = this.initialMax;
                this.updateVisual();
                this.updateInputs();
            }
        }