<script lang="ts">
	import { Tooltip as TooltipPrimitive } from 'bits-ui';
	import { cn } from '$lib/utils';

	export let sideOffset: number = 6;
	let className: string | undefined = undefined;
	export { className as class };
</script>

<TooltipPrimitive.Content
	{sideOffset}
	class={cn(
		'z-50 rounded-md bg-ink px-2.5 py-1.5 text-xs font-medium text-white shadow-md',
		className
	)}
	{...$$restProps}
>
	<slot />
</TooltipPrimitive.Content>
