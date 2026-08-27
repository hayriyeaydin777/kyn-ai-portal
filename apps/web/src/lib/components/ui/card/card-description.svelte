<script lang="ts">
	import { cn } from '$lib/utils';
	let className: string | undefined = undefined;
	export { className as class };
</script>

<p class={cn('text-xs leading-snug text-slate-500', className)} {...$$restProps}>
	<slot />
</p>
