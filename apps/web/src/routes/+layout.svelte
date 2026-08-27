<script lang="ts">
	import '../app.css';
	import Sidebar from '$lib/Sidebar.svelte';
	import AppHeader from '$lib/components/AppHeader.svelte';
	import Footer from '$lib/components/Footer.svelte';
	import { sidebarCollapsed } from '$lib/stores/sidebar';
	import type { LayoutData } from './$types';

	export let data: LayoutData;
</script>

<div class="h-screen overflow-hidden bg-paper">
	<Sidebar />
	<div
		class:md:pl-64={!$sidebarCollapsed}
		class:md:pl-[4.25rem]={$sidebarCollapsed}
		class="flex h-screen flex-col transition-[padding] duration-200"
	>
		<AppHeader applications={data.applications} />
		<main class="mx-auto w-full max-w-7xl flex-1 overflow-y-auto px-5 py-6 md:px-8 md:py-8">
			<slot />
		</main>
		<Footer />
	</div>
</div>

