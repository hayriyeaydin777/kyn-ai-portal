<script lang="ts">
	import { enhance } from '$app/forms';
	import type { ActionData, PageData } from './$types';

	export let data: PageData;
	export let form: ActionData;
</script>

<div class="mb-6">
	<h1 class="text-2xl font-extrabold text-ink">Brief Generator</h1>
	<p class="mt-1 text-sm text-slate-500">Generate an AI briefing for an application (fake provider, no tokens used).</p>
</div>

<form method="GET" class="mb-6 flex items-center gap-3 rounded-xl border border-line bg-white p-4">
	<label for="app" class="text-sm font-semibold text-slate-600">Application</label>
	<select
		id="app"
		name="app"
		class="rounded-lg border border-line px-3 py-2 text-sm"
		on:change={(e) => e.currentTarget.form?.requestSubmit()}
	>
		{#each data.applications as app (app.id)}
			<option value={app.id} selected={app.id === data.applicationId}>{app.name}</option>
		{/each}
	</select>
</form>

{#if form?.message}
	<p role="alert" class="mb-4 rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">{form.message}</p>
{/if}

{#if data.applicationId}
	<form method="POST" action="?/generateBrief" use:enhance class="mb-6">
		<input type="hidden" name="applicationId" value={data.applicationId} />
		<button type="submit" class="rounded-lg bg-teal px-4 py-2 text-sm font-semibold text-white">
			Generate brief (AI_PROVIDER=fake, no tokens used)
		</button>
	</form>

	{#if data.briefs.length === 0}
		<p class="rounded-xl border border-line bg-white p-6 text-sm text-slate-500">No briefs yet. Generate one above.</p>
	{:else}
		<ul class="space-y-4">
			{#each data.briefs as brief (brief.id)}
				<li class="rounded-xl border border-line bg-white p-4">
					<p class="text-xs font-semibold uppercase tracking-wide text-slate-400">
						provider: {brief.provider} — status: {brief.status}
					</p>
					<pre class="mt-2 whitespace-pre-wrap text-sm text-ink">{brief.text}</pre>
					<p class="mt-2 text-xs text-slate-500">Citations: {brief.citations.join(', ')}</p>
					{#if brief.status === 'draft'}
						<div class="mt-3 flex gap-2">
							<form method="POST" action="?/approveBrief" use:enhance>
								<input type="hidden" name="applicationId" value={data.applicationId} />
								<input type="hidden" name="briefId" value={brief.id} />
								<button type="submit" class="rounded-lg bg-teal px-3 py-1.5 text-xs font-semibold text-white">Approve</button>
							</form>
							<form method="POST" action="?/rejectBrief" use:enhance>
								<input type="hidden" name="applicationId" value={data.applicationId} />
								<input type="hidden" name="briefId" value={brief.id} />
								<button type="submit" class="rounded-lg border border-line px-3 py-1.5 text-xs font-semibold text-slate-600">Reject</button>
							</form>
						</div>
					{/if}
				</li>
			{/each}
		</ul>
	{/if}
{:else}
	<p class="rounded-xl border border-line bg-white p-6 text-sm text-slate-500">No applications available yet.</p>
{/if}
