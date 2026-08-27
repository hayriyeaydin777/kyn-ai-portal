<script lang="ts">
	import { cn } from '$lib/utils';
	let className: string | undefined = undefined;
	export { className as class };
</script>

<div class={cn('flex items-center gap-2.5 border-t border-line px-4 py-2.5', className)} {...$$restProps}>
	<slot />
</div>
