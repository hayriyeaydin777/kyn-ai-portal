import { error } from '@sveltejs/kit';
import { getApplication, listDependencies, listEvidence } from '$lib/api';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ fetch, params }) => {
	try {
		const [application, dependencies, evidence] = await Promise.all([
			getApplication(params.id, fetch),
			listDependencies(params.id, fetch),
			listEvidence(params.id, fetch)
		]);
		return { application, dependencies, evidence };
	} catch {
		throw error(404, 'Application not found');
	}
};
