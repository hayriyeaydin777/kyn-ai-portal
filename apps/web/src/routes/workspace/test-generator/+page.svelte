<script lang="ts">
	import { enhance } from '$app/forms';
	import type { ActionData } from './$types';

	export let form: ActionData;
</script>

<div class="mb-6">
	<h1 class="text-2xl font-extrabold text-ink">Test Generator</h1>
	<p class="mt-1 text-sm text-slate-500">
		Paste a small Python snippet below to generate a deterministic test skeleton — no code is ever executed.
	</p>
</div>

<form method="POST" action="?/generateTests" use:enhance class="rounded-xl border border-line bg-white p-4">
	<textarea
		name="source"
		rows="10"
		class="w-full max-w-none rounded-lg border border-line px-3 py-2 font-mono text-sm"
		placeholder={'def example(a, b):\n    return a + b'}
	></textarea>
	<button type="submit" class="mt-3 rounded-lg bg-teal px-4 py-2 text-sm font-semibold text-white">
		Generate test skeleton (no tokens)
	</button>
</form>

{#if form?.message}
	<p role="alert" class="mt-4 rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">{form.message}</p>
{/if}

{#if form?.suite}
	<div class="mt-6 rounded-xl border border-line bg-white p-4">
		<h2 class="text-sm font-bold text-ink">Generated Test Skeleton (status: {form.suite.status})</h2>
		<pre class="mt-3 whitespace-pre-wrap text-sm text-slate-600">{form.suite.generated_tests}</pre>
	</div>
{/if}
