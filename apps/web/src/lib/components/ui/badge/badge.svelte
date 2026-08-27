<script lang="ts" context="module">
	import { tv, type VariantProps } from 'tailwind-variants';

	export const badgeVariants = tv({
		base: 'inline-flex items-center rounded-full px-2 py-0.5 text-[0.68rem] font-bold uppercase tracking-wide',
		variants: {
			variant: {
				default: 'bg-teal/10 text-teal',
				success: 'bg-emerald-100 text-emerald-700',
				warning: 'bg-amber-100 text-amber-700',
				danger: 'bg-red-100 text-red-700',
				muted: 'bg-paper text-slate-400'
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
