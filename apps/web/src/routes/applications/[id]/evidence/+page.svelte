<script lang="ts">
	import type { PageData } from './$types';

	export let data: PageData;
</script>

<div class="mb-6">
	<a href={`/applications/${data.application.id}`} class="text-sm font-semibold text-teal no-underline hover:underline">
		← {data.application.name}
	</a>
	<h1 class="mt-2 text-2xl font-extrabold text-ink">Evidence</h1>
	<p class="mt-1 text-sm text-slate-500">Supporting evidence artifacts recorded for this application.</p>
</div>

{#if data.evidence.length === 0}
	<p class="rounded-xl border border-line bg-white p-6 text-sm text-slate-500">No evidence recorded.</p>
{:else}
	<div class="overflow-hidden rounded-xl border border-line bg-white">
		<table class="w-full text-left text-sm">
			<thead class="bg-paper text-[0.68rem] font-bold uppercase tracking-wide text-slate-500">
				<tr>
					<th class="px-4 py-3">Title</th>
					<th class="px-4 py-3">Source</th>
					<th class="px-4 py-3">Reference</th>
				</tr>
			</thead>
			<tbody>
				{#each data.evidence as ev (ev.id)}
					<tr class="border-t border-line">
						<td class="px-4 py-3 font-semibold text-ink">{ev.title}</td>
						<td class="px-4 py-3 text-slate-600">{ev.source}</td>
						<td class="px-4 py-3 text-slate-500">{ev.reference ?? '—'}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
{/if}
