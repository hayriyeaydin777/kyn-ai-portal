<script lang="ts">
	import { Separator as SeparatorPrimitive } from 'bits-ui';
	import { cn } from '$lib/utils';

	export let orientation: 'horizontal' | 'vertical' = 'horizontal';
	let className: string | undefined = undefined;
	export { className as class };
</script>

<SeparatorPrimitive.Root
	{orientation}
	class={cn(
		'shrink-0 bg-line',
		orientation === 'horizontal' ? 'h-px w-full' : 'h-full w-px',
		className
	)}
	{...$$restProps}
/>
