<script lang="ts">
	import { enhance } from '$app/forms';
	import type { ActionData, PageData } from './$types';

	export let data: PageData;
	export let form: ActionData;
</script>

<h1>Modernization Advisor — {data.application.name}</h1>
<p><a href={`/applications/${data.application.id}`}>Back to application</a></p>

{#if form?.message}
	<p role="alert">{form.message}</p>
{/if}

<h2>Current-state input</h2>
<form method="POST" action="?/createCase" use:enhance>
	<label>Technology stack <input name="technology_stack" required /></label>
	<label>Hosting <input name="hosting" required /></label>
	<label>Release process <input name="release_process" required /></label>
	<label>Scale <input name="scale" required /></label>
	<label>Pain points <textarea name="pain_points"></textarea></label>
	<button type="submit">Save current-state input</button>
</form>

{#if data.cases.length === 0}
	<p>No current-state input recorded yet.</p>
{:else}
	<ul>
		{#each data.cases as c (c.id)}
			<li>
				{c.technology_stack} on {c.hosting}, {c.release_process}, scale: {c.scale}
				<form method="POST" action="?/generateRecommendation" use:enhance>
					<input type="hidden" name="caseId" value={c.id} />
					<button type="submit">Generate recommendation (AI_PROVIDER=fake, no tokens)</button>
				</form>
			</li>
		{/each}
	</ul>
{/if}

<h2>Recommendations</h2>
{#if data.recommendations.length === 0}
	<p>No recommendations yet.</p>
{:else}
	<ul>
		{#each data.recommendations as rec (rec.id)}
			<li>
				<p>
					<em>provider: {rec.provider} — complexity score: {rec.complexity_score} — status: {rec.status}</em>
				</p>
				<h3>Risk signals</h3>
				<ul>
					{#each rec.risk_signals as signal}
						<li><strong>{signal.severity}</strong> [{signal.rule_id}] {signal.message}</li>
					{/each}
				</ul>
				<h3>Matched options</h3>
				<p>{rec.matched_option_ids.join(', ') || 'None'}</p>
				<h3>Narrative (draft — assumptions labeled, not fact)</h3>
				<pre>{rec.narrative}</pre>
				<p>Citations: {rec.citations.join(', ')}</p>
				<a href={`/applications/${data.application.id}/modernization/export/${rec.id}`} download>
					Export as JSON
				</a>
			</li>
		{/each}
	</ul>
{/if}
