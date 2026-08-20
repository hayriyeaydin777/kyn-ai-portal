<script lang="ts">
	import type { PageData } from './$types';

	export let data: PageData;
</script>

<h1>{data.application.name}</h1>
<p>{data.application.description ?? 'No description provided.'}</p>
<p>Business owner: {data.application.business_owner ?? 'Unassigned'}</p>
<p>Criticality: {data.application.criticality}</p>

<h2>Dependencies</h2>
{#if data.dependencies.length === 0}
	<p>No dependencies recorded.</p>
{:else}
	<ul>
		{#each data.dependencies as dep (dep.id)}
			<li>{dep.name} ({dep.dependency_type}) — {dep.criticality}</li>
		{/each}
	</ul>
{/if}

<h2>Evidence</h2>
{#if data.evidence.length === 0}
	<p>No evidence recorded.</p>
{:else}
	<ul>
		{#each data.evidence as ev (ev.id)}
			<li>{ev.title} — {ev.source}</li>
		{/each}
	</ul>
{/if}

<p><a href="/applications">Back to list</a></p>
