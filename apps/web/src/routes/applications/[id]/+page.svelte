<script lang="ts">
	import { enhance } from '$app/forms';
	import type { ActionData, PageData } from './$types';

	export let data: PageData;
	export let form: ActionData;
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

<h2>Assessment</h2>
<form method="POST" action="?/evaluate" use:enhance>
	<button type="submit">Run deterministic assessment</button>
</form>
{#if form?.message}
	<p role="alert">{form.message}</p>
{/if}
{#if data.findings.length === 0}
	<p>No findings yet. Run an assessment to generate findings.</p>
{:else}
	<ul>
		{#each data.findings as finding (finding.id)}
			<li>
				<strong>{finding.severity}</strong> [{finding.rule_id}] {finding.message}
				(evidence: {finding.evidence_fields.join(', ')})
			</li>
		{/each}
	</ul>
{/if}

<p><a href="/applications">Back to list</a></p>
