<script lang="ts">
	import { Avatar as AvatarPrimitive } from 'bits-ui';
	import { cn } from '$lib/utils';

	let className: string | undefined = undefined;
	export { className as class };
</script>

<AvatarPrimitive.Root
	class={cn('flex h-9 w-9 shrink-0 overflow-hidden rounded-full', className)}
	{...$$restProps}
>
	<slot />
</AvatarPrimitive.Root>
