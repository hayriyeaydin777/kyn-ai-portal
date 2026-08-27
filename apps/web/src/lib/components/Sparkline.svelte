<script lang="ts">
	/** Lightweight inline-SVG sparkline — layerchart's Tailwind-v4-only CSS pipeline conflicts with this project's Tailwind v3 setup. */
	export let points: number[] = [];
	export let width = 72;
	export let height = 24;
	export let colorClass = 'text-teal';

	const uid = `spark-${Math.random().toString(36).slice(2, 9)}`;

	$: min = Math.min(...points);
	$: max = Math.max(...points);
	$: range = max - min || 1;
	$: coords = points.map((value, index) => ({
		x: (index / (points.length - 1 || 1)) * width,
		y: height - ((value - min) / range) * (height - 3) - 1.5
	}));
	$: linePath = coords
		.map((point, index) => `${index === 0 ? 'M' : 'L'}${point.x.toFixed(1)},${point.y.toFixed(1)}`)
		.join(' ');
	$: areaPath = coords.length ? `${linePath} L${width},${height} L0,${height} Z` : '';
</script>

<svg {width} {height} viewBox="0 0 {width} {height}" class="overflow-visible {colorClass}" aria-hidden="true">
	<defs>
		<linearGradient id={uid} x1="0" y1="0" x2="0" y2="1">
			<stop offset="0%" stop-color="currentColor" stop-opacity="0.35" />
			<stop offset="100%" stop-color="currentColor" stop-opacity="0" />
		</linearGradient>
	</defs>
	<path d={areaPath} fill="url(#{uid})" stroke="none" />
	<path d={linePath} fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" />
</svg>
