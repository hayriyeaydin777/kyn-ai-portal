<script lang="ts">
	import { page } from '$app/stores';

	let open = false;

	type NavItem = { href: string; label: string; icon: string; soon?: boolean };
	type NavGroup = { title: string; items: NavItem[] };

	const navGroups: NavGroup[] = [
		{
			title: 'Overview',
			items: [{ href: '/', label: 'Overview', icon: '⌂' }]
		},
		{
			title: 'Recovery readiness',
			items: [
				{ href: '/applications', label: 'Applications', icon: '▣' },
				{ href: '/applications', label: 'Dependencies', icon: '⛓', soon: true },
				{ href: '/applications', label: 'Evidence', icon: '📄', soon: true },
				{ href: '/applications', label: 'Findings', icon: '⚑', soon: true },
				{ href: '/applications', label: 'Runbooks', icon: '📘', soon: true }
			]
		},
		{
			title: 'AI workspace',
			items: [
				{ href: '/workspace', label: 'Brief generator', icon: '✦' },
				{ href: '/workspace', label: 'Code review', icon: '⌨', soon: true },
				{ href: '/workspace', label: 'Test generator', icon: '✓', soon: true },
				{ href: '/workspace', label: 'Documentation', icon: '✎', soon: true },
				{ href: '/workspace', label: 'Prompt lab', icon: '⚗', soon: true }
			]
		},
		{
			title: 'Architecture',
			items: [
				{ href: '/governance', label: 'ADR assistant', icon: '◇' },
				{ href: '/governance', label: 'Architecture review', icon: '⬡', soon: true },
				{ href: '/governance', label: 'Diagrams', icon: '▤', soon: true }
			]
		},
		{
			title: 'Agent platform',
			items: [{ href: '/agents', label: 'Agent catalog', icon: '◈', soon: true }]
		},
		{
			title: 'Evaluation',
			items: [
				{ href: '/evaluation', label: 'AI metrics', icon: '📊', soon: true },
				{ href: '/evaluation', label: 'Observability', icon: '◎', soon: true }
			]
		},
		{
			title: 'Operations',
			items: [
				{ href: '/operations', label: 'Approvals', icon: '✔', soon: true },
				{ href: '/operations', label: 'Audit log', icon: '☰', soon: true },
				{ href: '/operations', label: 'Policies', icon: '🛡', soon: true },
				{ href: '/operations', label: 'Settings', icon: '⚙', soon: true }
			]
		}
	];

	$: currentPath = $page.url.pathname;
</script>

<svelte:window on:keydown={(event) => event.key === 'Escape' && (open = false)} />

<button
	class="fixed left-4 top-4 z-40 inline-flex h-11 w-11 items-center justify-center rounded-lg border border-line bg-white text-ink shadow-sm md:hidden"
	type="button"
	aria-label="Open navigation"
	aria-expanded={open}
	on:click={() => (open = true)}
>
	<span class="text-xl leading-none">☰</span>
</button>

{#if open}
	<button
		class="fixed inset-0 z-40 bg-ink/40 md:hidden"
		aria-label="Close navigation"
		type="button"
		on:click={() => (open = false)}
	></button>
{/if}

<aside
	class:translate-x-0={open}
	class="fixed inset-y-0 left-0 z-50 flex w-72 -translate-x-full flex-col border-r border-line bg-white px-5 py-6 transition-transform duration-200 md:translate-x-0"
	aria-label="Primary navigation"
>
	<div class="flex items-center justify-between border-b border-line pb-6">
		<a href="/" class="flex items-center gap-3 no-underline" on:click={() => (open = false)}>
			<span class="flex h-10 w-10 items-center justify-center rounded-lg bg-coral text-xl font-black text-white">R</span>
			<span>
				<strong class="block text-sm font-extrabold tracking-tight text-ink">Resilience</strong>
				<span class="block text-xs font-medium uppercase tracking-[0.16em] text-slate-500">Operations portal</span>
			</span>
		</a>
		<button class="text-slate-500 md:hidden" type="button" aria-label="Close navigation" on:click={() => (open = false)}>×</button>
	</div>

	<nav class="mt-6 flex-1 space-y-5 overflow-y-auto pr-1">
		{#each navGroups as group}
			<div>
				<p class="mb-2 px-3 text-[0.68rem] font-bold uppercase tracking-[0.18em] text-slate-400">{group.title}</p>
				<div class="space-y-1">
					{#each group.items as item}
						{#if item.soon}
							<span
								class="flex cursor-not-allowed items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-semibold text-slate-300"
								title="Coming soon"
							>
								<span class="flex h-7 w-7 items-center justify-center rounded-md bg-paper text-base">{item.icon}</span>
								{item.label}
								<span class="ml-auto rounded-full bg-paper px-2 py-0.5 text-[0.62rem] font-bold uppercase tracking-wide text-slate-400">Soon</span>
							</span>
						{:else}
							<a
								href={item.href}
								class:active={item.href === '/' ? currentPath === '/' : currentPath.startsWith(item.href)}
								class="sidebar-link group flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-semibold text-slate-600 no-underline transition-colors hover:bg-paper hover:text-teal"
								on:click={() => (open = false)}
							>
								<span class="flex h-7 w-7 items-center justify-center rounded-md bg-paper text-base text-teal group-[.active]:bg-white/15 group-[.active]:text-white">{item.icon}</span>
								{item.label}
							</a>
						{/if}
					{/each}
				</div>
			</div>
		{/each}
	</nav>

	<div class="mt-4 rounded-xl bg-teal p-4 text-white">
		<p class="text-[0.68rem] font-bold uppercase tracking-[0.16em] text-white/60">System status</p>
		<div class="mt-3 flex items-center gap-2 text-sm font-semibold"><span class="h-2 w-2 rounded-full bg-emerald-300"></span> All services healthy</div>
	</div>
</aside>
