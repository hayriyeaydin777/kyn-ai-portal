<script lang="ts">
	import '../app.css';
	import Sidebar from '$lib/Sidebar.svelte';
</script>

<div class="min-h-screen bg-paper">
	<Sidebar />
	<div class="md:pl-72">
		<header class="flex h-20 items-center justify-between gap-4 border-b border-line bg-white px-6 pl-20 md:px-10 md:pl-10">
			<div class="shrink-0">
				<p class="text-[0.68rem] font-bold uppercase tracking-[0.2em] text-coral">Resilience operations</p>
				<p class="mt-1 text-sm font-medium text-slate-500">AI engineering control center</p>
			</div>
			<div class="hidden max-w-md flex-1 items-center gap-2 rounded-lg border border-line bg-paper px-3 py-2 text-sm text-slate-400 md:flex">
				<span aria-hidden="true">🔍</span>
				<input
					type="search"
					placeholder="Search applications, agents, ADRs… (coming soon)"
					disabled
					class="w-full cursor-not-allowed bg-transparent text-sm text-slate-400 placeholder:text-slate-400 focus:outline-none"
				/>
			</div>
			<div class="flex items-center gap-3 text-slate-400">
				<span class="hidden items-center gap-2 text-sm text-slate-500 sm:flex">
					<span class="h-2 w-2 rounded-full bg-emerald-500"></span>
					Connected
				</span>
				<button type="button" class="hidden h-9 w-9 items-center justify-center rounded-lg border border-line hover:bg-paper sm:flex" title="Notifications (coming soon)" disabled>🔔</button>
				<button type="button" class="hidden h-9 w-9 items-center justify-center rounded-lg border border-line hover:bg-paper sm:flex" title="Help (coming soon)" disabled>❓</button>
				<button type="button" class="hidden h-9 w-9 items-center justify-center rounded-lg border border-line hover:bg-paper sm:flex" title="Settings (coming soon)" disabled>⚙</button>
				<span class="flex h-9 w-9 items-center justify-center rounded-full bg-teal text-sm font-bold text-white" title="Demo user">DU</span>
			</div>
		</header>
		<main class="mx-auto max-w-7xl px-6 py-8 md:px-10 md:py-12">
			<slot />
		</main>
	</div>
</div>

