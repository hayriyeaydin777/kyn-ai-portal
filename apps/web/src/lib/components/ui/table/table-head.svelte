<script lang="ts">
	import { cn } from '$lib/utils';
	let className: string | undefined = undefined;
	export { className as class };
</script>

<th
	class={cn(
		'whitespace-nowrap px-2.5 py-1.5 text-left text-[0.62rem] font-bold uppercase tracking-wide text-slate-400',
		className
	)}
	{...$$restProps}
>
	<slot />
</th>
