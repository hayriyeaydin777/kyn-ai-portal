<script lang="ts">
	import { cn } from '$lib/utils';

	export let value: string | number | undefined = undefined;
	let className: string | undefined = undefined;
	export { className as class };
</script>

<input
	bind:value
	class={cn(
		'flex h-9 w-full rounded-lg border border-line bg-white px-3 py-1 text-sm text-ink placeholder:text-slate-400 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-teal/40 disabled:cursor-not-allowed disabled:opacity-50',
		className
	)}
	on:blur
	on:change
	on:click
	on:focus
	on:keydown
	on:keyup
	on:input
	{...$$restProps}
/>
