<script lang="ts">
	import { cn } from '$lib/utils';
	let className: string | undefined = undefined;
	export { className as class };
</script>

<h3 class={cn('text-[13px] font-semibold leading-tight text-ink', className)} {...$$restProps}>
	<slot />
</h3>
