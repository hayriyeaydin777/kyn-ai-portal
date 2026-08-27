<script lang="ts">
	import { DropdownMenu as DropdownMenuPrimitive } from 'bits-ui';
	import { cn } from '$lib/utils';
	import { fly } from 'svelte/transition';

	export let sideOffset: number = 6;
	export let align: 'start' | 'center' | 'end' = 'end';
	let className: string | undefined = undefined;
	export { className as class };
</script>

<DropdownMenuPrimitive.Content
	{sideOffset}
	{align}
	transition={fly}
	transitionConfig={{ y: -4, duration: 120 }}
	class={cn(
		'z-50 min-w-[12rem] rounded-xl border border-line bg-white p-1.5 shadow-lg',
		className
	)}
	{...$$restProps}
>
	<slot />
</DropdownMenuPrimitive.Content>
