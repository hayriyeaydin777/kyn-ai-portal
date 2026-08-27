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
<p><a href={`/applications/${data.application.id}/modernization`}>Modernization Advisor</a></p>

<h2>Dependencies</h2>
<p><a href={`/applications/${data.application.id}/dependencies`}>View full dependencies page</a></p>
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
<p><a href={`/applications/${data.application.id}/evidence`}>View full evidence page</a></p>
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

<h2>AI Briefing</h2>
<form method="POST" action="?/generateBrief" use:enhance>
	<button type="submit">Generate brief (AI_PROVIDER=fake, no tokens used)</button>
</form>
{#if data.briefs.length === 0}
	<p>No briefs yet. Generate one above.</p>
{:else}
	<ul>
		{#each data.briefs as brief (brief.id)}
			<li>
				<p><em>provider: {brief.provider} — status: {brief.status}</em></p>
				<pre>{brief.text}</pre>
				<p>Citations: {brief.citations.join(', ')}</p>
				{#if brief.status === 'draft'}
					<form method="POST" action="?/approveBrief" use:enhance>
						<input type="hidden" name="briefId" value={brief.id} />
						<button type="submit">Approve</button>
					</form>
					<form method="POST" action="?/rejectBrief" use:enhance>
						<input type="hidden" name="briefId" value={brief.id} />
						<button type="submit">Reject</button>
					</form>
				{/if}
			</li>
		{/each}
	</ul>
{/if}

<p><a href="/applications">Back to list</a></p>
