<script lang="ts">
	import '../app.css';
	import Sidebar from '$lib/Sidebar.svelte';
</script>

<div class="min-h-screen bg-paper">
	<Sidebar />
	<div class="md:pl-72">
		<header class="flex h-20 items-center justify-between border-b border-line bg-white px-6 pl-20 md:px-10 md:pl-10">
			<div>
				<p class="text-[0.68rem] font-bold uppercase tracking-[0.2em] text-coral">Resilience operations</p>
				<p class="mt-1 text-sm font-medium text-slate-500">AI engineering control center</p>
			</div>
			<div class="hidden items-center gap-3 text-sm text-slate-500 sm:flex">
				<span class="h-2 w-2 rounded-full bg-emerald-500"></span>
				Connected
			</div>
		</header>
		<main class="mx-auto max-w-7xl px-6 py-8 md:px-10 md:py-12">
			<slot />
		</main>
	</div>
</div>

