<script lang="ts">
	import { DropdownMenu as DropdownMenuPrimitive } from 'bits-ui';
	import { cn } from '$lib/utils';

	let className: string | undefined = undefined;
	export { className as class };
</script>

<DropdownMenuPrimitive.Item
	class={cn(
		'flex cursor-pointer select-none items-center gap-2 rounded-lg px-2.5 py-2 text-sm font-medium text-ink outline-none data-[highlighted]:bg-paper data-[highlighted]:text-teal',
		className
	)}
	on:click
	{...$$restProps}
>
	<slot />
</DropdownMenuPrimitive.Item>
