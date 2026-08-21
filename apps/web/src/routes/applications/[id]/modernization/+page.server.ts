import { error, fail } from '@sveltejs/kit';
import {
	createModernizationCase,
	createModernizationRecommendation,
	getApplication,
	listModernizationCases,
	listModernizationRecommendations
} from '$lib/api';
import type { Actions, PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ fetch, params }) => {
	try {
		const [application, cases, recommendations] = await Promise.all([
			getApplication(params.id, fetch),
			listModernizationCases(params.id, fetch),
			listModernizationRecommendations(params.id, fetch)
		]);
		return { application, cases, recommendations };
	} catch {
		throw error(404, 'Application not found');
	}
};

export const actions: Actions = {
	createCase: async ({ fetch, params, request }) => {
		const formData = await request.formData();
		const payload = {
			technology_stack: String(formData.get('technology_stack') ?? ''),
			hosting: String(formData.get('hosting') ?? ''),
			release_process: String(formData.get('release_process') ?? ''),
			scale: String(formData.get('scale') ?? ''),
			pain_points: String(formData.get('pain_points') ?? '')
		};
		try {
			await createModernizationCase(params.id, payload, fetch);
		} catch {
			return fail(502, { message: 'Could not save current-state input.' });
		}
	},
	generateRecommendation: async ({ fetch, params, request }) => {
		const formData = await request.formData();
		const caseId = formData.get('caseId');
		if (typeof caseId !== 'string') {
			return fail(400, { message: 'Missing caseId.' });
		}
		try {
			await createModernizationRecommendation(params.id, caseId, fetch);
		} catch {
			return fail(502, { message: 'Recommendation generation failed.' });
		}
	}
};
