<script lang="ts">
	import { cn } from '$lib/utils';
	let className: string | undefined = undefined;
	export { className as class };
</script>

<div class={cn('rounded-xl border border-line bg-white shadow-sm', className)} {...$$restProps}>
	<slot />
</div>
