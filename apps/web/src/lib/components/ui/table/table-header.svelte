<script lang="ts">
	import { cn } from '$lib/utils';
	let className: string | undefined = undefined;
	export { className as class };
</script>

<thead class={cn('border-b border-line', className)} {...$$restProps}>
	<slot />
</thead>
