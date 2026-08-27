<script lang="ts">
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import SearchIcon from 'lucide-svelte/icons/search';
	import BellIcon from 'lucide-svelte/icons/bell';
	import CircleHelpIcon from 'lucide-svelte/icons/circle-help';
	import MenuIcon from 'lucide-svelte/icons/menu';
	import type { ApplicationProfile } from '$lib/api';
	import { sidebarCollapsed } from '$lib/stores/sidebar';
	import {
		DropdownMenu,
		DropdownMenuTrigger,
		Content as DropdownMenuContent,
		Item as DropdownMenuItem,
		Label as DropdownMenuLabel,
		Separator as DropdownMenuSeparator
	} from '$lib/components/ui/dropdown-menu';
	import { Avatar, AvatarFallback } from '$lib/components/ui/avatar';

	export let applications: ApplicationProfile[] = [];

	let searchInput: HTMLInputElement | undefined;
	let query = '';
	let searchOpen = false;

	$: matches = query.trim()
		? applications.filter((app) => app.name.toLowerCase().includes(query.trim().toLowerCase())).slice(0, 6)
		: [];

	function isMac() {
		return typeof navigator !== 'undefined' && /Mac/.test(navigator.platform);
	}

	function handleWindowKeydown(event: KeyboardEvent) {
		const shortcutPressed = (isMac() ? event.metaKey : event.ctrlKey) && event.key.toLowerCase() === 'k';
		if (shortcutPressed) {
			event.preventDefault();
			searchInput?.focus();
			searchOpen = true;
		}
		if (event.key === 'Escape') {
			searchOpen = false;
			searchInput?.blur();
		}
	}

	function selectApplication(id: string) {
		searchOpen = false;
		query = '';
		goto(`/applications/${id}`);
	}

	let searchWrapper: HTMLDivElement | undefined;
	function handleDocumentClick(event: MouseEvent) {
		if (searchWrapper && !searchWrapper.contains(event.target as Node)) {
			searchOpen = false;
		}
	}

	onMount(() => {
		document.addEventListener('click', handleDocumentClick);
		return () => document.removeEventListener('click', handleDocumentClick);
	});

	const sampleNotifications = [
		{ title: 'Modernization Advisor run completed', time: '15m ago' },
		{ title: 'ADR: Policy Evaluation Service needs review', time: '1h 20m ago' },
		{ title: 'Test generation failed for Claims API', time: '1h 45m ago' }
	];
</script>

<svelte:window on:keydown={handleWindowKeydown} />

<header class="flex h-12 shrink-0 items-center gap-3 border-b border-line bg-white px-3 pl-16 md:px-4 md:pl-3">
	<button
		type="button"
		class="hidden h-8 w-8 shrink-0 items-center justify-center rounded-lg text-slate-500 hover:bg-paper hover:text-ink md:flex"
		aria-label={$sidebarCollapsed ? 'Expand navigation' : 'Collapse navigation'}
		on:click={() => sidebarCollapsed.update((value) => !value)}
	>
		<MenuIcon class="h-4 w-4" />
	</button>

	<div class="flex-1"></div>

	<div class="relative hidden w-64 md:block" bind:this={searchWrapper}>
		<div class="flex items-center gap-1.5 rounded-lg border border-line bg-paper px-2 py-1 text-xs text-slate-500 focus-within:border-teal">
			<SearchIcon class="h-3.5 w-3.5 shrink-0" />
			<input
				bind:this={searchInput}
				bind:value={query}
				on:focus={() => (searchOpen = true)}
				type="search"
				placeholder="Search…"
				class="w-full bg-transparent text-xs text-ink placeholder:text-slate-400 focus:outline-none"
			/>
			<kbd class="hidden shrink-0 rounded border border-line bg-white px-1 py-0.5 text-[0.58rem] font-semibold text-slate-400 sm:inline">
				{isMac() ? '⌘K' : 'Ctrl K'}
			</kbd>
		</div>
		{#if searchOpen && query.trim()}
			<div class="absolute left-0 right-0 top-full z-50 mt-2 rounded-lg border border-line bg-white p-1.5 shadow-lg">
				{#if matches.length > 0}
					{#each matches as app (app.id)}
						<button
							type="button"
							class="flex w-full items-center gap-2 rounded-md px-2 py-1.5 text-left text-xs font-medium text-ink hover:bg-paper hover:text-teal"
							on:click={() => selectApplication(app.id)}
						>
							{app.name}
						</button>
					{/each}
				{:else}
					<p class="px-2 py-1.5 text-xs text-slate-400">No matching applications.</p>
				{/if}
			</div>
		{/if}
	</div>

	<div class="flex items-center gap-2 text-slate-400">
		<span class="hidden items-center gap-1.5 text-xs text-slate-500 sm:flex">
			<span class="h-1.5 w-1.5 rounded-full bg-emerald-500"></span>
			Connected
		</span>

		<DropdownMenu>
			<DropdownMenuTrigger
				class="relative hidden h-8 w-8 items-center justify-center rounded-lg border border-line hover:bg-paper sm:flex"
				title="Notifications"
			>
				<BellIcon class="h-3.5 w-3.5" />
				<span class="absolute -right-1 -top-1 flex h-3.5 w-3.5 items-center justify-center rounded-full bg-coral text-[0.55rem] font-bold text-white">
					{sampleNotifications.length}
				</span>
			</DropdownMenuTrigger>
			<DropdownMenuContent class="w-72">
				<DropdownMenuLabel>Notifications (sample data)</DropdownMenuLabel>
				<DropdownMenuSeparator />
				{#each sampleNotifications as note}
					<DropdownMenuItem class="flex-col items-start gap-0.5">
						<span class="text-sm font-semibold text-ink">{note.title}</span>
						<span class="text-xs text-slate-400">{note.time}</span>
					</DropdownMenuItem>
				{/each}
			</DropdownMenuContent>
		</DropdownMenu>

		<DropdownMenu>
			<DropdownMenuTrigger class="hidden h-8 w-8 items-center justify-center rounded-lg border border-line hover:bg-paper sm:flex" title="Help">
				<CircleHelpIcon class="h-3.5 w-3.5" />
			</DropdownMenuTrigger>
			<DropdownMenuContent class="w-56">
				<DropdownMenuItem>Documentation</DropdownMenuItem>
				<DropdownMenuItem>Security</DropdownMenuItem>
				<DropdownMenuItem>Contact support</DropdownMenuItem>
			</DropdownMenuContent>
		</DropdownMenu>

		<DropdownMenu>
			<DropdownMenuTrigger title="Demo user">
				<Avatar class="h-8 w-8">
					<AvatarFallback>HA</AvatarFallback>
				</Avatar>
			</DropdownMenuTrigger>
			<DropdownMenuContent class="w-48">
				<DropdownMenuLabel>Demo user</DropdownMenuLabel>
				<DropdownMenuSeparator />
				<DropdownMenuItem>Profile</DropdownMenuItem>
				<DropdownMenuItem>Settings</DropdownMenuItem>
				<DropdownMenuSeparator />
				<DropdownMenuItem>Sign out</DropdownMenuItem>
			</DropdownMenuContent>
		</DropdownMenu>
	</div>
</header>
