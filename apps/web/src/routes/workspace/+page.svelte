<script lang="ts">
	import { enhance } from '$app/forms';
	import type { ActionData } from './$types';

	export let form: ActionData;
</script>

<h1>AI Engineering Workspace</h1>
<p>Paste a small Python snippet below. All checks are deterministic and read-only — no code is ever executed.</p>

<form method="POST" use:enhance>
	<textarea name="source" rows="10" cols="80" placeholder="def example(a, b):\n    return a + b"
	></textarea>
	<div>
		<button formaction="?/reviewCode" type="submit">Run code review (no tokens)</button>
		<button formaction="?/generateTests" type="submit">Generate test skeleton (no tokens)</button>
		<button formaction="?/generateDocs" type="submit">Generate documentation draft (no tokens)</button>
	</div>
</form>

{#if form?.message}
	<p role="alert">{form.message}</p>
{/if}

{#if form?.review}
	<h2>Code Review (provider: {form.review.provider}, status: {form.review.status})</h2>
	<ul>
		{#each form.review.findings as finding}
			<li><strong>{finding.severity}</strong> [{finding.rule_id}] {finding.message}</li>
		{/each}
	</ul>
	<pre>{form.review.summary}</pre>
{/if}

{#if form?.suite}
	<h2>Generated Test Skeleton (status: {form.suite.status})</h2>
	<pre>{form.suite.generated_tests}</pre>
{/if}

{#if form?.draft}
	<h2>Documentation Draft (version {form.draft.version}, status: {form.draft.status})</h2>
	<pre>{form.draft.draft_text}</pre>
{/if}
