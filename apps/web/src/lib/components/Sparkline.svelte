<script lang="ts">
	/** Lightweight inline-SVG sparkline (no chart library — layerchart requires Svelte 5). */
	export let points: number[] = [];
	export let width = 64;
	export let height = 24;
	export let stroke = '#174b4d';

	$: min = Math.min(...points);
	$: max = Math.max(...points);
	$: range = max - min || 1;
	$: path = points
		.map((value, index) => {
			const x = (index / (points.length - 1 || 1)) * width;
			const y = height - ((value - min) / range) * height;
			return `${index === 0 ? 'M' : 'L'}${x.toFixed(1)},${y.toFixed(1)}`;
		})
		.join(' ');
</script>

<svg {width} {height} viewBox="0 0 {width} {height}" class="overflow-visible" aria-hidden="true">
	<path d={path} fill="none" stroke={stroke} stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" />
</svg>
