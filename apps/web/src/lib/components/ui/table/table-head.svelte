<script lang="ts">
	import { cn } from '$lib/utils';
	let className: string | undefined = undefined;
	export { className as class };
</script>

<th
	class={cn(
		'whitespace-nowrap px-3 py-2 text-left text-[0.68rem] font-bold uppercase tracking-wide text-slate-400',
		className
	)}
	{...$$restProps}
>
	<slot />
</th>
