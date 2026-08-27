<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import ArrowUpIcon from 'lucide-svelte/icons/arrow-up';
	import ArrowDownIcon from 'lucide-svelte/icons/arrow-down';

	let scrollEl: HTMLElement | null = null;
	let visible = false;
	let atBottom = false;

	function handleScroll() {
		if (!scrollEl) return;
		const { scrollTop, scrollHeight, clientHeight } = scrollEl;
		visible = scrollHeight - clientHeight > 80;
		atBottom = scrollTop + clientHeight >= scrollHeight - 24;
	}

	function scrollToggle() {
		scrollEl?.scrollTo({ top: atBottom ? 0 : scrollEl.scrollHeight, behavior: 'smooth' });
	}

	onMount(() => {
		scrollEl = document.querySelector('main');
		scrollEl?.addEventListener('scroll', handleScroll);
		handleScroll();
		const resizeObserver = new ResizeObserver(handleScroll);
		if (scrollEl) resizeObserver.observe(scrollEl);
		return () => resizeObserver.disconnect();
	});

	onDestroy(() => scrollEl?.removeEventListener('scroll', handleScroll));
</script>

{#if visible}
	<button
		type="button"
		on:click={scrollToggle}
		aria-label={atBottom ? 'Scroll to top' : 'Scroll to bottom'}
		class="dsy-btn dsy-btn-circle fixed bottom-6 right-6 z-40 h-11 w-11 border-none bg-ink text-white shadow-lg transition-transform hover:scale-105 hover:bg-teal"
	>
		{#if atBottom}
			<ArrowUpIcon class="h-5 w-5" />
		{:else}
			<ArrowDownIcon class="h-5 w-5" />
		{/if}
	</button>
{/if}
