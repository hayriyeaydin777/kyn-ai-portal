<script lang="ts">
	import '../app.css';
	import Sidebar from '$lib/Sidebar.svelte';
	import AppHeader from '$lib/components/AppHeader.svelte';
	import Footer from '$lib/components/Footer.svelte';
	import type { LayoutData } from './$types';

	export let data: LayoutData;
</script>

<div class="min-h-screen bg-paper">
	<Sidebar />
	<div class="flex min-h-screen flex-col md:pl-64">
		<AppHeader applications={data.applications} />
		<main class="mx-auto w-full max-w-7xl flex-1 px-5 py-6 md:px-8 md:py-8">
			<slot />
		</main>
		<Footer />
	</div>
</div>

