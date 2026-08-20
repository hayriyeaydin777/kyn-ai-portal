import { error, fail } from '@sveltejs/kit';
import {
	decideBrief,
	generateBrief,
	getApplication,
	listBriefs,
	listDependencies,
	listEvidence,
	listFindings,
	triggerAssessment
} from '$lib/api';
import type { Actions, PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ fetch, params }) => {
	try {
		const [application, dependencies, evidence, findings, briefs] = await Promise.all([
			getApplication(params.id, fetch),
			listDependencies(params.id, fetch),
			listEvidence(params.id, fetch),
			listFindings(params.id, fetch),
			listBriefs(params.id, fetch)
		]);
		return { application, dependencies, evidence, findings, briefs };
	} catch {
		throw error(404, 'Application not found');
	}
};

export const actions: Actions = {
	evaluate: async ({ fetch, params }) => {
		try {
			await triggerAssessment(params.id, fetch);
		} catch {
			return fail(502, { message: 'Assessment failed. Is the policy service running?' });
		}
	},
	generateBrief: async ({ fetch, params }) => {
		try {
			await generateBrief(params.id, fetch);
		} catch {
			return fail(502, { message: 'Brief generation failed.' });
		}
	},
	approveBrief: async ({ fetch, params, request }) => {
		const formData = await request.formData();
		const briefId = formData.get('briefId');
		if (typeof briefId !== 'string') {
			return fail(400, { message: 'Missing briefId.' });
		}
		try {
			await decideBrief(params.id, briefId, 'approve', fetch);
		} catch {
			return fail(502, { message: 'Approval failed.' });
		}
	},
	rejectBrief: async ({ fetch, params, request }) => {
		const formData = await request.formData();
		const briefId = formData.get('briefId');
		if (typeof briefId !== 'string') {
			return fail(400, { message: 'Missing briefId.' });
		}
		try {
			await decideBrief(params.id, briefId, 'reject', fetch);
		} catch {
			return fail(502, { message: 'Rejection failed.' });
		}
	}
};
