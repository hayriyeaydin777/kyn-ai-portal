<script lang="ts">
	import { Popover } from 'melt/builders';
	import BotIcon from 'lucide-svelte/icons/bot';
	import XIcon from 'lucide-svelte/icons/x';
	import SendIcon from 'lucide-svelte/icons/send';
	import SparklesIcon from 'lucide-svelte/icons/sparkles';

	const popover = new Popover();
</script>

<button
	{...popover.trigger}
	type="button"
	aria-label={popover.open ? 'Close AI assistant' : 'Open AI assistant'}
	class="dsy-btn dsy-btn-circle fixed bottom-20 right-6 z-40 h-14 w-14 border-none bg-gradient-to-br from-teal to-emerald-500 text-white shadow-xl transition-transform hover:scale-105"
>
	<span class="absolute inset-0 -z-10 animate-ping rounded-full bg-teal/40"></span>
	{#if popover.open}
		<XIcon class="h-6 w-6" />
	{:else}
		<BotIcon class="h-6 w-6" />
	{/if}
</button>

<div
	{...popover.content}
	class="fixed bottom-[9.5rem] right-6 z-40 w-80 rounded-2xl border border-line bg-white p-4 shadow-2xl [&:not(:popover-open)]:hidden"
>
	<div class="flex items-center gap-2 border-b border-line pb-3">
		<span class="flex h-8 w-8 items-center justify-center rounded-lg bg-teal/10 text-teal">
			<SparklesIcon class="h-4 w-4" />
		</span>
		<div>
			<p class="text-sm font-bold text-ink">Workspace Assistant</p>
			<p class="text-xs text-slate-400">Sample data — not wired to a backend yet</p>
		</div>
	</div>
	<div class="my-3 rounded-xl bg-paper p-3 text-sm text-ink">
		Hi! I'm a preview of the workspace assistant. Ask me about applications,
		modernization runs, or ADRs once I'm connected to a real model.
	</div>
	<form class="flex items-center gap-2" on:submit|preventDefault>
		<input
			type="text"
			disabled
			placeholder="Ask a question… (coming soon)"
			class="w-full rounded-lg border border-line bg-paper px-3 py-2 text-sm text-ink placeholder:text-slate-400 disabled:cursor-not-allowed"
		/>
		<button
			type="submit"
			disabled
			class="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-teal text-white disabled:opacity-50"
		>
			<SendIcon class="h-4 w-4" />
		</button>
	</form>
</div>
