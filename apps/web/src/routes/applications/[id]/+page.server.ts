import { error, fail } from '@sveltejs/kit';
import { getApplication, listDependencies, listEvidence, listFindings, triggerAssessment } from '$lib/api';
import type { Actions, PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ fetch, params }) => {
	try {
		const [application, dependencies, evidence, findings] = await Promise.all([
			getApplication(params.id, fetch),
			listDependencies(params.id, fetch),
			listEvidence(params.id, fetch),
			listFindings(params.id, fetch)
		]);
		return { application, dependencies, evidence, findings };
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
	}
};
