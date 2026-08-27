<script lang="ts">
	import type { PageData } from './$types';

	export let data: PageData;
</script>

<div class="mb-6">
	<a href={`/applications/${data.application.id}`} class="text-sm font-semibold text-teal no-underline hover:underline">
		← {data.application.name}
	</a>
	<h1 class="mt-2 text-2xl font-extrabold text-ink">Dependencies</h1>
	<p class="mt-1 text-sm text-slate-500">External and internal dependencies recorded for this application.</p>
</div>

{#if data.dependencies.length === 0}
	<p class="rounded-xl border border-line bg-white p-6 text-sm text-slate-500">No dependencies recorded.</p>
{:else}
	<div class="overflow-hidden rounded-xl border border-line bg-white">
		<table class="w-full text-left text-sm">
			<thead class="bg-paper text-[0.68rem] font-bold uppercase tracking-wide text-slate-500">
				<tr>
					<th class="px-4 py-3">Name</th>
					<th class="px-4 py-3">Type</th>
					<th class="px-4 py-3">Criticality</th>
					<th class="px-4 py-3">Notes</th>
				</tr>
			</thead>
			<tbody>
				{#each data.dependencies as dep (dep.id)}
					<tr class="border-t border-line">
						<td class="px-4 py-3 font-semibold text-ink">{dep.name}</td>
						<td class="px-4 py-3 text-slate-600">{dep.dependency_type}</td>
						<td class="px-4 py-3 text-slate-600">{dep.criticality}</td>
						<td class="px-4 py-3 text-slate-500">{dep.notes ?? '—'}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
{/if}
