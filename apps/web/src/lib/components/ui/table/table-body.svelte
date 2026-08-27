<script lang="ts">
	import { cn } from '$lib/utils';
	let className: string | undefined = undefined;
	export { className as class };
</script>

<tbody class={cn('divide-y divide-line', className)} {...$$restProps}>
	<slot />
</tbody>
