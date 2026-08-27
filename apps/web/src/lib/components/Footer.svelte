<script lang="ts">
	import ShieldCheckIcon from 'lucide-svelte/icons/shield-check';
</script>

<footer class="shrink-0 border-t border-line bg-white px-5 py-3 text-xs text-slate-500 md:px-8">
	<div class="mx-auto flex w-full flex-col items-start justify-between gap-2 sm:flex-row sm:items-center">
		<p class="flex items-center gap-1.5 text-left">
			<ShieldCheckIcon class="h-3.5 w-3.5 text-coral" />
			<span class="font-semibold text-ink">ROAIP v2.0.0</span>
			<span class="text-line">|</span>
			© 2026 Synthetic Systems Lab. All rights reserved.
		</p>
		<nav class="flex items-center gap-2">
			<button type="button" class="hover:text-teal">Security</button>
			<span class="text-line">|</span>
			<button type="button" class="hover:text-teal">Privacy</button>
			<span class="text-line">|</span>
			<button type="button" class="hover:text-teal">Contact</button>
			<span class="text-line">|</span>
			<button type="button" class="hover:text-teal">Documentation</button>
		</nav>
	</div>
</footer>
