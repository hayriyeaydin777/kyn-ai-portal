<script lang="ts">
	import RocketIcon from 'lucide-svelte/icons/rocket';
	import CodeIcon from 'lucide-svelte/icons/code';
	import ListChecksIcon from 'lucide-svelte/icons/list-checks';
	import FilePenLineIcon from 'lucide-svelte/icons/file-pen-line';
	import ScaleIcon from 'lucide-svelte/icons/scale';
	import MessageSquareIcon from 'lucide-svelte/icons/message-square';
	import PlusIcon from 'lucide-svelte/icons/plus';
	import SettingsIcon from 'lucide-svelte/icons/settings';
	import TrendingUpIcon from 'lucide-svelte/icons/trending-up';
	import ShieldCheckIcon from 'lucide-svelte/icons/shield-check';
	import ArrowRightIcon from 'lucide-svelte/icons/arrow-up-right';

	import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '$lib/components/ui/card';
	import { Badge } from '$lib/components/ui/badge';
	import { Button } from '$lib/components/ui/button';
	import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '$lib/components/ui/table';
	import Sparkline from '$lib/components/Sparkline.svelte';

	// (sample data) — no backend exists yet for run history, approvals, provider metrics, or usage stats.
	const tools = [
		{
			name: 'Modernization Advisor',
			description: 'Assess current state, target architecture, risks, and migration roadmap.',
			icon: RocketIcon,
			accent: 'bg-teal/10 text-teal',
			href: '/applications'
		},
		{
			name: 'Code Review',
			description: 'AI-powered static analysis for security, performance, and best practices.',
			icon: CodeIcon,
			accent: 'bg-coral/10 text-coral',
			href: '/workspace/code-review'
		},
		{
			name: 'Test Generator',
			description: 'Generate unit, integration, and boundary tests from code or requirements.',
			icon: ListChecksIcon,
			accent: 'bg-blue-100 text-blue-600',
			href: '/workspace/test-generator'
		},
		{
			name: 'Documentation Generator',
			description: 'Create technical docs, API references, diagrams, and architecture notes.',
			icon: FilePenLineIcon,
			accent: 'bg-purple-100 text-purple-600',
			href: '/workspace/documentation'
		},
		{
			name: 'ADR Assistant',
			description: 'Generate Architecture Decision Records with alternatives and trade-offs.',
			icon: ScaleIcon,
			accent: 'bg-amber-100 text-amber-600',
			href: '/governance'
		},
		{
			name: 'Prompt Lab',
			description: 'Design, version, evaluate, and optimize prompts with test datasets.',
			icon: MessageSquareIcon,
			accent: 'bg-teal/10 text-teal',
			href: null
		}
	];

	const recentRuns = [
		{ id: 'RUN-2026-08-15-1024', tool: 'Modernization Advisor', target: 'Northstar Claims Service', status: 'Completed', score: '82%', duration: '2m 34s', time: '10:24 AM' },
		{ id: 'RUN-2026-08-15-0941', tool: 'Code Review', target: 'auth_service.py', status: 'Completed', score: '91%', duration: '1m 18s', time: '9:41 AM' },
		{ id: 'RUN-2026-08-15-0850', tool: 'Test Generator', target: 'PaymentController.cs', status: 'Completed', score: '77%', duration: '45s', time: '8:50 AM' },
		{ id: 'RUN-2026-08-14-1632', tool: 'ADR Assistant', target: 'Policy Evaluation Service', status: 'Completed', score: '88%', duration: '1m 55s', time: '4:32 PM' },
		{ id: 'RUN-2026-08-14-1512', tool: 'Prompt Lab', target: 'Brief Generation v3', status: 'Completed', score: '73%', duration: '30s', time: '3:12 PM' },
		{ id: 'RUN-2026-08-14-1345', tool: 'Documentation Generator', target: 'Claims API', status: 'Failed', score: '–', duration: '1m 05s', time: '1:45 PM' }
	];

	const approvalQueue = [
		{ request: 'AI Brief: Northstar Claims Service', type: 'Brief', by: 'Synthetic User A', risk: 'High', age: '15m' },
		{ request: 'Modernization Roadmap', type: 'Roadmap', by: 'Synthetic User B', risk: 'Medium', age: '42m' },
		{ request: 'ADR: Policy Evaluation Service', type: 'ADR', by: 'Synthetic User C', risk: 'Medium', age: '1h 20m' },
		{ request: 'Code Review Findings', type: 'Review', by: 'Synthetic User D', risk: 'Low', age: '2h 05m' },
		{ request: 'Test Generation Results', type: 'Tests', by: 'Synthetic User E', risk: 'Low', age: '3h 12m' }
	];

	const quickStats = [
		{ label: 'AI Runs', value: '124', delta: '+18% vs last 7 days', points: [70, 82, 78, 95, 88, 110, 124] },
		{ label: 'Success Rate', value: '94%', delta: '+6% vs last 7 days', points: [86, 88, 87, 90, 91, 93, 94] },
		{ label: 'Approvals', value: '47', delta: '+12% vs last 7 days', points: [30, 34, 33, 38, 40, 44, 47] },
		{ label: 'Applications', value: '12', delta: '+2 vs last 7 days', points: [8, 9, 9, 10, 10, 11, 12] },
		{ label: 'Assessments', value: '28', delta: '+6 vs last 7 days', points: [18, 20, 21, 23, 24, 26, 28] },
		{ label: 'Evidence Items', value: '312', delta: '+34 vs last 7 days', points: [240, 255, 262, 278, 290, 300, 312] }
	];

	function statusVariant(status: string) {
		return status === 'Failed' ? 'danger' : 'success';
	}

	function riskVariant(risk: string) {
		if (risk === 'High') return 'danger';
		if (risk === 'Medium') return 'warning';
		return 'muted';
	}
</script>

<div class="mb-5 flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
	<div>
		<h1 class="text-xl font-extrabold text-ink">AI Workspace</h1>
		<p class="mt-0.5 text-xs text-slate-500">
			AI-powered tools to build, modernize, test, and improve applications with confidence.
		</p>
	</div>
	<div class="flex shrink-0 gap-2">
		<Button variant="outline">
			<SettingsIcon class="h-3.5 w-3.5" />
			Workspace settings
		</Button>
		<Button>
			<PlusIcon class="h-3.5 w-3.5" />
			New AI Run
		</Button>
	</div>
</div>

<div class="mb-6 grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6">
	{#each tools as tool}
		<Card class="flex flex-col">
			<CardHeader>
				<span class={`flex h-8 w-8 items-center justify-center rounded-lg ${tool.accent}`}>
					<svelte:component this={tool.icon} class="h-4 w-4" />
				</span>
				<CardTitle class="mt-1.5">{tool.name}</CardTitle>
				<CardDescription>{tool.description}</CardDescription>
			</CardHeader>
			<CardFooter class="mt-auto border-t-0 pt-0">
				{#if tool.href}
					<Button href={tool.href} variant="secondary" class="w-full justify-center">
						Launch
						<ArrowRightIcon class="h-3.5 w-3.5" />
					</Button>
				{:else}
					<Button disabled variant="secondary" class="w-full justify-center">Coming soon</Button>
				{/if}
			</CardFooter>
		</Card>
	{/each}
</div>

<div class="mb-6 grid grid-cols-1 gap-5 lg:grid-cols-3">
	<Card class="lg:col-span-2">
		<CardHeader class="flex-row items-center justify-between">
			<div>
				<CardTitle>Recent AI Runs</CardTitle>
				<CardDescription>Sample data — run history isn't wired to a backend yet.</CardDescription>
			</div>
			<Button variant="ghost" size="sm" disabled>View all runs</Button>
		</CardHeader>
		<CardContent class="px-0">
			<Table>
				<TableHeader>
					<TableRow>
						<TableHead>Run ID</TableHead>
						<TableHead>Tool</TableHead>
						<TableHead>Target</TableHead>
						<TableHead>Status</TableHead>
						<TableHead>Score</TableHead>
						<TableHead>Duration</TableHead>
						<TableHead>Time</TableHead>
					</TableRow>
				</TableHeader>
				<TableBody>
					{#each recentRuns as run (run.id)}
						<TableRow>
							<TableCell class="font-mono text-xs text-slate-500">{run.id}</TableCell>
							<TableCell>{run.tool}</TableCell>
							<TableCell>{run.target}</TableCell>
							<TableCell><Badge variant={statusVariant(run.status)}>{run.status}</Badge></TableCell>
							<TableCell>{run.score}</TableCell>
							<TableCell>{run.duration}</TableCell>
							<TableCell class="text-slate-500">{run.time}</TableCell>
						</TableRow>
					{/each}
				</TableBody>
			</Table>
		</CardContent>
	</Card>

	<Card>
		<CardHeader class="flex-row items-center justify-between">
			<div>
				<CardTitle class="flex items-center gap-2">
					Approval Queue
					<Badge variant="danger">{approvalQueue.length}</Badge>
				</CardTitle>
				<CardDescription>Sample data — approvals aren't wired to a backend yet.</CardDescription>
			</div>
		</CardHeader>
		<CardContent class="space-y-2">
			{#each approvalQueue as item}
				<div class="flex items-center justify-between gap-3 rounded-lg border border-line px-2.5 py-1.5">
					<div class="min-w-0">
						<p class="truncate text-xs font-semibold text-ink">{item.request}</p>
						<p class="text-[0.68rem] text-slate-400">{item.type} · {item.by} · {item.age}</p>
					</div>
					<Badge variant={riskVariant(item.risk)}>{item.risk}</Badge>
				</div>
			{/each}
		</CardContent>
		<CardFooter>
			<Button variant="ghost" size="sm" disabled class="w-full justify-center">View all approvals</Button>
		</CardFooter>
	</Card>
</div>

<div class="grid grid-cols-1 gap-5 lg:grid-cols-3">
	<Card>
		<CardHeader>
			<CardTitle>Provider Status</CardTitle>
		</CardHeader>
		<CardContent class="space-y-2.5">
			<div class="flex items-center justify-between">
				<p class="text-xs font-semibold text-ink">Fake Provider (v1)</p>
				<Badge variant="success">Active</Badge>
			</div>
			<p class="text-[0.68rem] text-slate-500">Model: Fake LLM v1.0 · Deterministic</p>
			<p class="text-[0.68rem] text-slate-500">Environment: Development</p>
			<div class="grid grid-cols-2 gap-2.5 border-t border-line pt-2.5 text-[0.68rem]">
				<div><p class="text-slate-400">Requests today</p><p class="font-semibold text-ink">128</p></div>
				<div><p class="text-slate-400">Tokens</p><p class="font-semibold text-ink">25,642</p></div>
				<div><p class="text-slate-400">Avg latency</p><p class="font-semibold text-ink">1.42s</p></div>
				<div><p class="text-slate-400">Error rate</p><p class="font-semibold text-ink">0%</p></div>
			</div>
			<p class="text-[0.68rem] text-slate-400">Last health check: 10:25:33 AM · Healthy</p>
		</CardContent>
		<CardFooter>
			<Button variant="ghost" size="sm" disabled class="w-full justify-center">View metrics</Button>
		</CardFooter>
	</Card>

	<Card>
		<CardHeader>
			<CardTitle>Quick Stats</CardTitle>
		</CardHeader>
		<CardContent class="grid grid-cols-2 gap-2.5">
			{#each quickStats as stat}
				<div class="rounded-lg border border-line p-2.5">
					<p class="text-[0.68rem] text-slate-400">{stat.label}</p>
					<p class="mt-0.5 text-base font-extrabold text-ink">{stat.value}</p>
					<div class="mt-1 flex items-center justify-between gap-2">
						<span class="flex items-center gap-1 text-[0.62rem] font-semibold text-emerald-600">
							<TrendingUpIcon class="h-3 w-3" />
							{stat.delta}
						</span>
						<Sparkline points={stat.points} width={36} height={14} />
					</div>
				</div>
			{/each}
		</CardContent>
	</Card>

	<Card class="border-teal/20 bg-teal/5">
		<CardHeader>
			<CardTitle class="flex items-center gap-1.5 text-teal">
				<ShieldCheckIcon class="h-3.5 w-3.5" />
				System Notice
			</CardTitle>
		</CardHeader>
		<CardContent>
			<p class="text-xs font-semibold text-ink">Synthetic Data Only</p>
			<p class="mt-1.5 text-[0.68rem] leading-snug text-slate-600">
				All data in this environment is 100% synthetic and created for demonstration and portfolio
				purposes only. No real customer, company, or personal data is used.
			</p>
		</CardContent>
		<CardFooter class="border-t-0">
			<Button variant="ghost" size="sm" class="px-0 text-teal" href="/">Learn more</Button>
		</CardFooter>
	</Card>
</div>

