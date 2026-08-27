<script lang="ts">
	import { Avatar as AvatarPrimitive } from 'bits-ui';
	import { cn } from '$lib/utils';

	let className: string | undefined = undefined;
	export { className as class };
</script>

<AvatarPrimitive.Fallback
	class={cn(
		'flex h-full w-full items-center justify-center bg-teal text-xs font-bold text-white',
		className
	)}
	{...$$restProps}
>
	<slot />
</AvatarPrimitive.Fallback>
