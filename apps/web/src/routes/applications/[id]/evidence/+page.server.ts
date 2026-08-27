import { error } from '@sveltejs/kit';
import { getApplication, listEvidence } from '$lib/api';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ fetch, params }) => {
	try {
		const [application, evidence] = await Promise.all([
			getApplication(params.id, fetch),
			listEvidence(params.id, fetch)
		]);
		return { application, evidence };
	} catch {
		throw error(404, 'Application not found');
	}
};
