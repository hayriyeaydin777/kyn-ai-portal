<script lang="ts">
	import { cn } from '$lib/utils';
	let className: string | undefined = undefined;
	export { className as class };
</script>

<td class={cn('whitespace-nowrap px-2.5 py-2 text-xs text-ink', className)} {...$$restProps}>
	<slot />
</td>
