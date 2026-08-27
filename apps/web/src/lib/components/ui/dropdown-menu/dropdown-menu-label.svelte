<script lang="ts">
	import { cn } from '$lib/utils';

	let className: string | undefined = undefined;
	export { className as class };
</script>

<div class={cn('px-2.5 py-1.5 text-[0.68rem] font-bold uppercase tracking-wide text-slate-400', className)} {...$$restProps}>
	<slot />
</div>
