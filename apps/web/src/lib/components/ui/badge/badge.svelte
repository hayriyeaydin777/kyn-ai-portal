<script lang="ts" context="module">
	import { tv, type VariantProps } from 'tailwind-variants';

	export const badgeVariants = tv({
		base: 'inline-flex items-center rounded-full px-2.5 py-1 text-xs font-semibold leading-none',
		variants: {
			variant: {
				default: 'bg-teal/10 text-teal',
				success: 'bg-emerald-100 text-emerald-700',
				warning: 'bg-amber-100 text-amber-700',
				danger: 'bg-red-100 text-red-700',
				muted: 'bg-slate-100 text-slate-500'
			}
		},
		defaultVariants: { variant: 'default' }
	});

	export type BadgeVariant = VariantProps<typeof badgeVariants>['variant'];
</script>

<script lang="ts">
	import { cn } from '$lib/utils';

	export let variant: BadgeVariant = 'default';
	let className: string | undefined = undefined;
	export { className as class };
</script>

<span class={cn(badgeVariants({ variant }), className)} {...$$restProps}>
	<slot />
</span>
