<script lang="ts">
	import { cn } from '$lib/utils';
	let className: string | undefined = undefined;
	export { className as class };
</script>

<tr class={cn('transition-colors hover:bg-paper/60', className)} {...$$restProps}>
	<slot />
</tr>
