<script lang="ts">
	import { cn } from '$lib/utils';
	let className: string | undefined = undefined;
	export { className as class };
</script>

<td class={cn('whitespace-nowrap px-3 py-3 text-[0.8rem] text-ink', className)} {...$$restProps}>
	<slot />
</td>
