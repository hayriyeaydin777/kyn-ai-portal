<script lang="ts">
	import type { PageData } from './$types';

	export let data: PageData;

	const severityClasses: Record<string, string> = {
		high: 'bg-red-50 text-red-700',
		critical: 'bg-red-50 text-red-700',
		medium: 'bg-amber-50 text-amber-700',
		low: 'bg-slate-100 text-slate-600'
	};
</script>

<div class="mb-6">
	<a href={`/applications/${data.application.id}`} class="text-sm font-semibold text-teal no-underline hover:underline">
		← {data.application.name}
	</a>
	<h1 class="mt-2 text-2xl font-extrabold text-ink">Findings</h1>
	<p class="mt-1 text-sm text-slate-500">Deterministic assessment findings for this application.</p>
</div>

{#if data.findings.length === 0}
	<p class="rounded-xl border border-line bg-white p-6 text-sm text-slate-500">
		No findings yet. Run a deterministic assessment from the application page to generate findings.
	</p>
{:else}
	<ul class="space-y-3">
		{#each data.findings as finding (finding.id)}
			<li class="rounded-xl border border-line bg-white p-4">
				<div class="flex items-center gap-2">
					<span
						class="rounded-full px-2 py-0.5 text-[0.68rem] font-bold uppercase tracking-wide {severityClasses[
							finding.severity.toLowerCase()
						] ?? 'bg-slate-100 text-slate-600'}"
					>
						{finding.severity}
					</span>
					<span class="text-xs font-mono text-slate-400">{finding.rule_id}</span>
				</div>
				<p class="mt-2 text-sm text-ink">{finding.message}</p>
				<p class="mt-1 text-xs text-slate-500">Evidence: {finding.evidence_fields.join(', ')}</p>
			</li>
		{/each}
	</ul>
{/if}
