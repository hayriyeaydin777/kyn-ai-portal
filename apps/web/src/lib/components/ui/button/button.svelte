<script lang="ts" context="module">
	import { tv, type VariantProps } from 'tailwind-variants';

	export const buttonVariants = tv({
		base: 'inline-flex items-center justify-center gap-1.5 whitespace-nowrap rounded-md text-[0.8rem] font-semibold leading-none transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-teal/40 disabled:pointer-events-none disabled:opacity-50',
		variants: {
			variant: {
				default: 'bg-teal text-white hover:bg-teal/90',
				outline: 'border border-line bg-white text-ink hover:bg-paper',
				ghost: 'text-slate-500 hover:bg-paper hover:text-ink',
				secondary: 'bg-paper text-ink hover:bg-line/60'
			},
			size: {
				default: 'h-8 px-3.5 py-1.5',
				sm: 'h-7 rounded-md px-2.5 text-xs',
				icon: 'h-8 w-8'
			}
		},
		defaultVariants: { variant: 'default', size: 'default' }
	});

	export type ButtonVariant = VariantProps<typeof buttonVariants>['variant'];
	export type ButtonSize = VariantProps<typeof buttonVariants>['size'];
</script>

<script lang="ts">
	import { cn } from '$lib/utils';

	export let variant: ButtonVariant = 'default';
	export let size: ButtonSize = 'default';
	export let type: 'button' | 'submit' | 'reset' = 'button';
	export let disabled = false;
	export let href: string | undefined = undefined;
	let className: string | undefined = undefined;
	export { className as class };
</script>

{#if href && !disabled}
	<a href={href} class={cn(buttonVariants({ variant, size }), className)} on:click {...$$restProps}>
		<slot />
	</a>
{:else}
	<button
		{type}
		{disabled}
		class={cn(buttonVariants({ variant, size }), className)}
		on:click
		{...$$restProps}
	>
		<slot />
	</button>
{/if}

