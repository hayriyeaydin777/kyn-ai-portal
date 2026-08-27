<script lang="ts">
	import RocketIcon from 'lucide-svelte/icons/rocket';
	import CodeIcon from 'lucide-svelte/icons/code';
	import ListChecksIcon from 'lucide-svelte/icons/list-checks';
	import FilePenLineIcon from 'lucide-svelte/icons/file-pen-line';
	import ScaleIcon from 'lucide-svelte/icons/scale';
	import MessageSquareIcon from 'lucide-svelte/icons/message-square';
	import PlusIcon from 'lucide-svelte/icons/plus';
	import ChevronDownIcon from 'lucide-svelte/icons/chevron-down';
	import SettingsIcon from 'lucide-svelte/icons/settings';
	import TrendingUpIcon from 'lucide-svelte/icons/trending-up';
	import ShieldCheckIcon from 'lucide-svelte/icons/shield-check';
	import ArrowRightIcon from 'lucide-svelte/icons/arrow-up-right';
	import CircleCheckBigIcon from 'lucide-svelte/icons/circle-check-big';
	import BotIcon from 'lucide-svelte/icons/bot';
	import BarChart3Icon from 'lucide-svelte/icons/bar-chart-3';
	import ClockIcon from 'lucide-svelte/icons/clock';

	import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '$lib/components/ui/card';
	import { Badge } from '$lib/components/ui/badge';
	import { Button } from '$lib/components/ui/button';
	import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '$lib/components/ui/table';
	import {
		DropdownMenu,
		DropdownMenuTrigger,
		Content as DropdownMenuContent,
		Item as DropdownMenuItem
	} from '$lib/components/ui/dropdown-menu';
	import Sparkline from '$lib/components/Sparkline.svelte';

	// (sample data) — no backend exists yet for run history, approvals, provider metrics, or usage stats.
	const tools = [
		{
			name: 'Modernization Advisor',
			description: 'Assess current state, target architecture, risks, and migration roadmap.',
			icon: RocketIcon,
			tile: 'bg-gradient-to-br from-teal to-emerald-600',
			pill: 'border-teal/20 bg-teal/10 text-teal hover:bg-teal/15',
			href: '/applications'
		},
		{
			name: 'Code Review',
			description: 'AI-powered static analysis for security, performance, and best practices.',
			icon: CodeIcon,
			tile: 'bg-gradient-to-br from-coral to-red-600',
			pill: 'border-coral/20 bg-coral/10 text-coral hover:bg-coral/15',
			href: '/workspace/code-review'
		},
		{
			name: 'Test Generator',
			description: 'Generate unit, integration, and boundary tests from code or requirements.',
			icon: ListChecksIcon,
			tile: 'bg-gradient-to-br from-blue-500 to-blue-700',
			pill: 'border-blue-200 bg-blue-50 text-blue-700 hover:bg-blue-100',
			href: '/workspace/test-generator'
		},
		{
			name: 'Documentation Generator',
			description: 'Create technical docs, API references, diagrams, and architecture notes.',
			icon: FilePenLineIcon,
			tile: 'bg-gradient-to-br from-purple-500 to-purple-700',
			pill: 'border-purple-200 bg-purple-50 text-purple-700 hover:bg-purple-100',
			href: '/workspace/documentation'
		},
		{
			name: 'ADR Assistant',
			description: 'Generate Architecture Decision Records with alternatives and trade-offs.',
			icon: ScaleIcon,
			tile: 'bg-gradient-to-br from-amber-400 to-amber-600',
			pill: 'border-amber-200 bg-amber-50 text-amber-700 hover:bg-amber-100',
			href: '/governance'
		},
		{
			name: 'Prompt Lab',
			description: 'Design, version, evaluate, and optimize prompts with test datasets.',
			icon: MessageSquareIcon,
			tile: 'bg-gradient-to-br from-teal to-emerald-600',
			pill: 'border-teal/20 bg-teal/10 text-teal hover:bg-teal/15',
			href: '/workspace'
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
		<h1 class="text-xl font-semibold text-ink">AI Workspace</h1>
		<p class="mt-0.5 text-xs text-slate-500">AI-powered tools to build, modernize, test, and improve applications with confidence.</p>
	</div>
	<div class="flex shrink-0 gap-2">
		<div class="flex">
			<Button variant="outline" class="rounded-r-none border-teal/30 text-teal hover:bg-teal/5"><PlusIcon class="h-3.5 w-3.5" />New AI Run</Button>
			<DropdownMenu>
				<DropdownMenuTrigger class="inline-flex h-8 w-8 items-center justify-center rounded-r-md border border-l-0 border-teal/30 text-teal hover:bg-teal/5" aria-label="Choose AI run type"><ChevronDownIcon class="h-3.5 w-3.5" /></DropdownMenuTrigger>
				<DropdownMenuContent align="end">
					<DropdownMenuItem>Modernization assessment</DropdownMenuItem>
					<DropdownMenuItem>Code review</DropdownMenuItem>
					<DropdownMenuItem>Test generation</DropdownMenuItem>
				</DropdownMenuContent>
			</DropdownMenu>
		</div>
		<Button variant="outline"><SettingsIcon class="h-3.5 w-3.5" />Workspace settings</Button>
	</div>
</div>
<div class="mb-6 grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6">
	{#each tools as tool}
		<Card class="flex flex-col">
			<CardHeader>
				<span class={`flex h-12 w-12 items-center justify-center rounded-2xl text-white shadow-sm ${tool.tile}`}>
					<svelte:component this={tool.icon} class="h-6 w-6" />
				</span>
				<CardTitle class="mt-2 font-semibold">{tool.name}</CardTitle>
				<CardDescription>{tool.description}</CardDescription>
			</CardHeader>
			<CardFooter class="mt-auto border-t-0 pt-0">
				{#if tool.href}
					<Button
						href={tool.href}
						variant="ghost"
						class={`w-full justify-center rounded-lg border font-semibold ${tool.pill}`}
					>
						Launch
						<ArrowRightIcon class="h-3.5 w-3.5" />
					</Button>
				{:else}
					<Button disabled class="w-full justify-center rounded-lg border border-line bg-paper text-slate-400">Coming soon</Button>
				{/if}
			</CardFooter>
		</Card>
	{/each}
</div>

<div class="mb-6 grid grid-cols-1 gap-5 xl:grid-cols-2">
	<Card>
		<CardHeader class="flex-col items-start justify-between gap-2 sm:flex-row sm:items-center">
			<div class="flex items-center gap-2">
				<ClockIcon class="h-4 w-4 text-teal" />
				<div>
					<CardTitle class="font-semibold">Recent AI Runs</CardTitle>
				</div>
			</div>
			<Button variant="ghost" size="sm" disabled class="shrink-0 gap-1 font-semibold text-teal disabled:opacity-100 hover:bg-transparent">
				View all runs
				<ArrowRightIcon class="h-3.5 w-3.5" />
			</Button>
		</CardHeader>
		<CardContent class="px-0">
			<Table class="workspace-table recent-runs-table">
				<TableHeader>
					<TableRow>
						<TableHead class="w-[20%]">Run ID</TableHead>
						<TableHead class="w-[22%]">Tool</TableHead>
						<TableHead class="w-[25%]">Target</TableHead>
						<TableHead class="w-[15%]">Status</TableHead>
						<TableHead class="w-[7%]">Score</TableHead>
						<TableHead class="w-[11%]">Duration</TableHead>
					</TableRow>
				</TableHeader>
				<TableBody>
					{#each recentRuns as run (run.id)}
						<TableRow>
							<TableCell class="truncate font-mono text-slate-500" title={run.id}>{run.id}</TableCell>
							<TableCell class="truncate" title={run.tool}>{run.tool}</TableCell>
							<TableCell class="truncate" title={run.target}>{run.target}</TableCell>
							<TableCell><Badge class="workspace-pill" variant={statusVariant(run.status)}>{run.status}</Badge></TableCell>
							<TableCell>{run.score}</TableCell>
							<TableCell>{run.duration}</TableCell>
						</TableRow>
					{/each}
				</TableBody>
			</Table>
		</CardContent>
		<CardFooter>
			<Button variant="ghost" size="sm" disabled class="w-full justify-center gap-1 font-semibold text-teal disabled:opacity-100 hover:bg-transparent">
				View full run history
				<ArrowRightIcon class="h-3.5 w-3.5" />
			</Button>
		</CardFooter>
	</Card>

	<Card>
		<CardHeader class="flex-row items-center justify-between gap-2 py-4">
			<div class="flex items-center gap-2">
				<CircleCheckBigIcon class="h-4 w-4 text-teal" />
				<div>
					<CardTitle class="flex items-center gap-2 font-semibold">
						Approval Queue
						<Badge variant="danger">{approvalQueue.length}</Badge>
					</CardTitle>
				</div>
			</div>
			<Button variant="ghost" size="sm" disabled class="shrink-0 gap-1 font-semibold text-teal disabled:opacity-100 hover:bg-transparent">
				View all approvals
				<ArrowRightIcon class="h-3.5 w-3.5" />
			</Button>
		</CardHeader>
		<CardContent class="px-0">
			<Table class="workspace-table approval-queue-table">
				<TableHeader>
					<TableRow>
						<TableHead class="w-[36%]">Request</TableHead>
						<TableHead class="w-[16%]">Type</TableHead>
						<TableHead class="w-[24%]">Requested by</TableHead>
						<TableHead class="w-[14%]">Risk</TableHead>
						<TableHead class="w-[10%]">Age</TableHead>
					</TableRow>
				</TableHeader>
				<TableBody>
					{#each approvalQueue as item (item.request)}
						<TableRow>
							<TableCell class="whitespace-nowrap font-semibold">{item.request}</TableCell>
							<TableCell class="text-slate-500">{item.type}</TableCell>
							<TableCell class="whitespace-nowrap text-slate-500">{item.by}</TableCell>
							<TableCell><Badge class="workspace-pill" variant={riskVariant(item.risk)}>{item.risk}</Badge></TableCell>
							<TableCell class="text-slate-500">{item.age}</TableCell>
						</TableRow>
					{/each}
				</TableBody>
			</Table>
		</CardContent>
		<CardFooter>
			<Button variant="ghost" size="sm" disabled class="w-full justify-center gap-1 font-semibold text-teal disabled:opacity-100 hover:bg-transparent">
				Go to approvals
				<ArrowRightIcon class="h-3.5 w-3.5" />
			</Button>
		</CardFooter>
	</Card>
</div>

<style>
	:global(.workspace-table) {
		table-layout: fixed;
	}

	:global(.workspace-table th) {
		padding: 0.5rem 0.375rem;
		font-size: 0.625rem;
		line-height: 0.875rem;
	}

	:global(.workspace-table td) {
		padding: 0.5rem 0.375rem;
		font-size: 0.6875rem;
		line-height: 0.875rem;
	}

	:global(.workspace-table th:first-child),
	:global(.workspace-table td:first-child) {
		padding-left: 1rem;
	}

	:global(.workspace-table .workspace-pill) {
		border: 1px solid currentColor;
		background-color: color-mix(in srgb, currentColor 10%, white);
		padding: 0.1875rem 0.4375rem;
		font-size: 0.625rem;
	}
</style>

<div class="grid grid-cols-1 items-stretch gap-5 lg:grid-cols-3">
	<Card class="h-full">
		<CardHeader>
			<CardTitle class="flex items-center gap-2 font-semibold">
				<BotIcon class="h-4 w-4 text-teal" />
				Provider Status
			</CardTitle>
		</CardHeader>
		<CardContent class="grid gap-3 sm:grid-cols-[minmax(0,1fr)_11rem]">
			<div class="rounded-lg border border-line p-3">
				<div class="flex min-w-0 items-start gap-2.5">
					<span class="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-teal/20 text-teal">
						<BotIcon class="h-5 w-5" />
					</span>
					<div class="min-w-0">
						<div class="flex flex-wrap items-center gap-2">
							<p class="text-sm font-semibold text-ink">Fake Provider (v1)</p>
							<Badge class="border border-emerald-600/30 bg-emerald-50 text-emerald-700" variant="success">Active</Badge>
						</div>
						<p class="mt-1 text-xs text-slate-500">Model: Fake LLM v1.0 · Deterministic</p>
						<p class="text-xs text-slate-500">Environment: Development</p>
					</div>
				</div>
				<p class="mt-4 flex items-center gap-1.5 border-t border-line pt-2.5 text-[0.68rem] text-slate-400">
					<span>Last health check: 10:25:33 AM ·</span>
					<span class="h-1.5 w-1.5 rounded-full bg-emerald-500"></span>
					<span class="text-emerald-600">Healthy</span>
				</p>
			</div>
			<div>
				<div class="rounded-md border border-line bg-white p-3">
					<p class="mb-2 text-[0.62rem] font-semibold uppercase tracking-wide text-slate-500">Usage Today</p>
					<div class="space-y-2 text-xs">
						<div class="flex items-center justify-between gap-3"><p class="text-slate-500">Requests</p><p class="font-semibold text-ink">128</p></div>
						<div class="flex items-center justify-between gap-3"><p class="text-slate-500">Tokens</p><p class="font-semibold text-ink">25,642</p></div>
						<div class="flex items-center justify-between gap-3"><p class="text-slate-500">Avg latency</p><p class="font-semibold text-ink">1.42s</p></div>
						<div class="flex items-center justify-between gap-3"><p class="text-slate-500">Error rate</p><p class="font-semibold text-ink">0%</p></div>
					</div>
				</div>
				<Button variant="ghost" size="sm" disabled class="mt-2 w-full justify-center gap-1 px-0 font-semibold text-teal disabled:opacity-100 hover:bg-transparent">
					View metrics
					<ArrowRightIcon class="h-3.5 w-3.5" />
				</Button>
			</div>
		</CardContent>
	</Card>

	<Card class="h-full">
		<CardHeader>
			<CardTitle class="flex items-center gap-2 font-semibold">
				<BarChart3Icon class="h-4 w-4 text-teal" />
				Quick Stats
			</CardTitle>
		</CardHeader>
		<CardContent class="grid grid-cols-2 gap-2 xl:grid-cols-3">
			{#each quickStats as stat}
				<div class="min-w-0 rounded-md border border-slate-200 bg-white p-2.5">
					<p class="text-[0.68rem] text-slate-500">{stat.label}</p>
					<p class="mt-0.5 text-base font-semibold text-ink">{stat.value}</p>
					<div class="mt-1 flex items-end justify-between gap-1">
						<span class="min-w-0 truncate text-[0.62rem] font-medium text-emerald-500">
							<TrendingUpIcon class="h-3 w-3" />
							{stat.delta}
						</span>
						<Sparkline points={stat.points} width={48} height={20} colorClass="text-cyan-500" />
					</div>
				</div>
			{/each}
		</CardContent>
	</Card>

	<Card class="h-full">
		<CardHeader>
			<CardTitle class="flex items-center gap-1.5 font-semibold">
				<ShieldCheckIcon class="h-3.5 w-3.5 text-teal" />
				System Notice
			</CardTitle>
		</CardHeader>
		<CardContent class="pt-0">
			<div class="rounded-md border border-cyan-100 bg-cyan-50/50 p-4">
				<p class="text-sm font-semibold text-teal">Synthetic Data Only</p>
				<p class="mt-2 text-xs leading-relaxed text-slate-600">
					All data in this environment is 100% synthetic and created for demonstration and portfolio
					purposes only. No real customer, company, or personal data is used.
				</p>
				<Button variant="ghost" size="sm" class="mt-4 gap-1 px-0 font-semibold text-teal hover:bg-transparent" href="/">
					Learn more
					<ArrowRightIcon class="h-3.5 w-3.5" />
				</Button>
			</div>
		</CardContent>
	</Card>
</div>

