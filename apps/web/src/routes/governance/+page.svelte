<script lang="ts">
	import { enhance } from '$app/forms';
	import type { ActionData, PageData } from './$types';

	export let data: PageData;
	export let form: ActionData;
</script>

<h1>Architecture Governance</h1>

{#if form?.message}
	<p role="alert">{form.message}</p>
{/if}

<h2>New architecture decision</h2>
<form method="POST" action="?/createDecision" use:enhance>
	<label>Title <input name="title" required /></label>
	<label>Context <textarea name="context" required></textarea></label>
	<label>Drivers <textarea name="drivers" required></textarea></label>
	<label>Decision <textarea name="decision" required></textarea></label>
	<label>Consequences <textarea name="consequences"></textarea></label>
	<button type="submit">Create draft</button>
</form>

<h2>Decisions</h2>
{#if data.decisions.length === 0}
	<p>No architecture decisions yet.</p>
{:else}
	<ul>
		{#each data.decisions as d (d.id)}
			<li>
				<h3>{d.title} (v{d.version})</h3>
				<p>
					<em>status: {d.status}</em>
					{#if d.status === 'accepted'}
						<strong>— immutable</strong>
					{/if}
				</p>
				<p>{d.decision}</p>
				<details>
					<summary>Alternatives (draft, reviewable)</summary>
					<pre>{d.alternatives}</pre>
				</details>

				{#if d.status === 'draft'}
					<form method="POST" action="?/propose" use:enhance>
						<input type="hidden" name="decisionId" value={d.id} />
						<button type="submit">Propose</button>
					</form>
				{/if}
				{#if d.status === 'proposed'}
					<form method="POST" action="?/accept" use:enhance>
						<input type="hidden" name="decisionId" value={d.id} />
						<button type="submit">Accept</button>
					</form>
					<form method="POST" action="?/reject" use:enhance>
						<input type="hidden" name="decisionId" value={d.id} />
						<button type="submit">Reject</button>
					</form>
				{/if}
			</li>
		{/each}
	</ul>
{/if}
