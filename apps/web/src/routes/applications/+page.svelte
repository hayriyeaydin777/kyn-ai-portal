<script lang="ts">
	import type { PageData } from './$types';

	export let data: PageData;
</script>

<h1>Application Profiles</h1>

{#if data.applications.length === 0}
	<p>No application profiles yet.</p>
{:else}
	<ul>
		{#each data.applications as app (app.id)}
			<li>
				<a href={`/applications/${app.id}`}>{app.name}</a>
				— criticality: {app.criticality}
			</li>
		{/each}
	</ul>
{/if}
