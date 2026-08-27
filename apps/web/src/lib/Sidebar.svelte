<script lang="ts">
	import { page } from '$app/stores';
	import ShieldCheckIcon from 'lucide-svelte/icons/shield-check';
	import LayoutDashboardIcon from 'lucide-svelte/icons/layout-dashboard';
	import AppWindowIcon from 'lucide-svelte/icons/app-window';
	import GitBranchIcon from 'lucide-svelte/icons/git-branch';
	import FileTextIcon from 'lucide-svelte/icons/file-text';
	import ClipboardCheckIcon from 'lucide-svelte/icons/clipboard-check';
	import FlagIcon from 'lucide-svelte/icons/flag';
	import BookOpenIcon from 'lucide-svelte/icons/book-open';
	import RocketIcon from 'lucide-svelte/icons/rocket';
	import CodeIcon from 'lucide-svelte/icons/code';
	import ListChecksIcon from 'lucide-svelte/icons/list-checks';
	import FilePenLineIcon from 'lucide-svelte/icons/file-pen-line';
	import MessageSquareIcon from 'lucide-svelte/icons/message-square';
	import ScaleIcon from 'lucide-svelte/icons/scale';
	import ShapesIcon from 'lucide-svelte/icons/shapes';
	import WorkflowIcon from 'lucide-svelte/icons/workflow';
	import BotIcon from 'lucide-svelte/icons/bot';
	import UserIcon from 'lucide-svelte/icons/user';
	import BarChart3Icon from 'lucide-svelte/icons/bar-chart-3';
	import ActivityIcon from 'lucide-svelte/icons/activity';
	import CircleCheckBigIcon from 'lucide-svelte/icons/circle-check-big';
	import ScrollTextIcon from 'lucide-svelte/icons/scroll-text';
	import ShieldIcon from 'lucide-svelte/icons/shield';
	import SettingsIcon from 'lucide-svelte/icons/settings';
	import ChevronsLeftIcon from 'lucide-svelte/icons/chevrons-left';
	import MenuIcon from 'lucide-svelte/icons/menu';
	import XIcon from 'lucide-svelte/icons/x';
	import type { ComponentType } from 'svelte';

	let open = false;
	let collapsed = false;

	type NavItem = { href: string; label: string; icon: ComponentType; soon?: boolean };
	type NavGroup = { title: string; items: NavItem[] };

	const navGroups: NavGroup[] = [
		{
			title: 'Recovery readiness',
			items: [
				{ href: '/', label: 'Dashboard', icon: LayoutDashboardIcon, soon: true },
				{ href: '/applications', label: 'Applications', icon: AppWindowIcon },
				{ href: '/applications', label: 'Dependencies', icon: GitBranchIcon, soon: true },
				{ href: '/applications', label: 'Evidence', icon: FileTextIcon, soon: true },
				{ href: '/applications', label: 'Assessments', icon: ClipboardCheckIcon, soon: true },
				{ href: '/applications', label: 'Findings', icon: FlagIcon, soon: true },
				{ href: '/applications', label: 'Runbooks', icon: BookOpenIcon, soon: true }
			]
		},
		{
			title: 'AI workspace',
			items: [
				{ href: '/workspace', label: 'Workspace home', icon: LayoutDashboardIcon },
				{ href: '/applications', label: 'Modernization advisor', icon: RocketIcon },
				{ href: '/workspace/code-review', label: 'Code review', icon: CodeIcon },
				{ href: '/workspace/test-generator', label: 'Test generator', icon: ListChecksIcon },
				{ href: '/workspace/documentation', label: 'Documentation generator', icon: FilePenLineIcon },
				{ href: '/workspace', label: 'Prompt lab', icon: MessageSquareIcon, soon: true }
			]
		},
		{
			title: 'Architecture',
			items: [
				{ href: '/governance', label: 'ADR assistant', icon: ScaleIcon, soon: true },
				{ href: '/governance', label: 'Architecture review', icon: ShapesIcon, soon: true },
				{ href: '/governance', label: 'Diagram generator', icon: WorkflowIcon, soon: true },
				{ href: '/governance', label: 'Governance', icon: ShieldCheckIcon }
			]
		},
		{
			title: 'Agent platform',
			items: [
				{ href: '/agents', label: 'Agent catalog', icon: BotIcon, soon: true },
				{ href: '/agents', label: 'Agent details', icon: UserIcon, soon: true }
			]
		},
		{
			title: 'Evaluation',
			items: [
				{ href: '/evaluation', label: 'AI metrics', icon: BarChart3Icon, soon: true },
				{ href: '/evaluation', label: 'Observability', icon: ActivityIcon, soon: true }
			]
		},
		{
			title: 'Operations',
			items: [
				{ href: '/operations', label: 'Approvals', icon: CircleCheckBigIcon, soon: true },
				{ href: '/operations', label: 'Audit log', icon: ScrollTextIcon, soon: true },
				{ href: '/operations', label: 'Policies', icon: ShieldIcon, soon: true },
				{ href: '/operations', label: 'Settings', icon: SettingsIcon, soon: true }
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
	<MenuIcon class="h-5 w-5" />
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
	class:md:w-72={!collapsed}
	class:md:w-[4.5rem]={collapsed}
	class="fixed inset-y-0 left-0 z-50 flex w-72 -translate-x-full flex-col border-r border-line bg-white px-5 py-6 transition-[transform,width] duration-200 md:translate-x-0"
	aria-label="Primary navigation"
>
	<div class="flex items-center justify-between border-b border-line pb-6">
		<a href="/" class="flex min-w-0 items-center gap-3 no-underline" on:click={() => (open = false)}>
			<span class="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-coral text-white">
				<ShieldCheckIcon class="h-5 w-5" />
			</span>
			{#if !collapsed}
				<span class="min-w-0">
					<strong class="block truncate text-sm font-extrabold leading-tight tracking-tight text-ink">Resilience Operations &amp;</strong>
					<span class="block truncate text-xs font-medium uppercase tracking-[0.14em] text-slate-500">AI Engineering Portal</span>
				</span>
			{/if}
		</a>
		<button class="shrink-0 text-slate-500 md:hidden" type="button" aria-label="Close navigation" on:click={() => (open = false)}>
			<XIcon class="h-5 w-5" />
		</button>
	</div>

	<nav class="mt-6 flex-1 space-y-5 overflow-y-auto overflow-x-hidden pr-1">
		{#each navGroups as group}
			<div>
				{#if !collapsed}
					<p class="mb-2 px-3 text-[0.68rem] font-bold uppercase tracking-[0.18em] text-slate-400">{group.title}</p>
				{/if}
				<div class="space-y-1">
					{#each group.items as item}
						{#if item.soon}
							<span
								class="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-semibold text-slate-300"
								title="Coming soon"
							>
								<span class="flex h-7 w-7 shrink-0 items-center justify-center rounded-md bg-paper">
									<svelte:component this={item.icon} class="h-4 w-4" />
								</span>
								{#if !collapsed}
									<span class="truncate">{item.label}</span>
									<span class="ml-auto shrink-0 rounded-full bg-paper px-2 py-0.5 text-[0.62rem] font-bold uppercase tracking-wide text-slate-400">Soon</span>
								{/if}
							</span>
						{:else}
							<a
								href={item.href}
								class:active={item.href === '/' ? currentPath === '/' : currentPath.startsWith(item.href)}
								class="sidebar-link group flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-semibold text-slate-600 no-underline transition-colors hover:bg-paper hover:text-teal"
								on:click={() => (open = false)}
								title={collapsed ? item.label : undefined}
							>
								<span class="flex h-7 w-7 shrink-0 items-center justify-center rounded-md bg-paper text-teal group-[.active]:bg-white/15 group-[.active]:text-white">
									<svelte:component this={item.icon} class="h-4 w-4" />
								</span>
								{#if !collapsed}
									<span class="truncate">{item.label}</span>
								{/if}
							</a>
						{/if}
					{/each}
				</div>
			</div>
		{/each}
	</nav>

	{#if !collapsed}
		<div class="mt-4 rounded-xl bg-teal p-4 text-white">
			<p class="text-[0.68rem] font-bold uppercase tracking-[0.16em] text-white/60">System status</p>
			<div class="mt-3 flex items-center gap-2 text-sm font-semibold"><span class="h-2 w-2 rounded-full bg-emerald-300"></span> All services healthy</div>
		</div>
	{/if}

	<button
		type="button"
		class="mt-4 hidden items-center justify-center gap-2 rounded-lg border border-line px-3 py-2 text-xs font-semibold text-slate-500 hover:bg-paper md:flex"
		on:click={() => (collapsed = !collapsed)}
	>
		<ChevronsLeftIcon class={collapsed ? 'h-4 w-4 rotate-180 transition-transform' : 'h-4 w-4 transition-transform'} />
		{#if !collapsed}Collapse{/if}
	</button>
</aside>
