import { error } from '@sveltejs/kit';
import { getApplication, listFindings } from '$lib/api';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ fetch, params }) => {
	try {
		const [application, findings] = await Promise.all([
			getApplication(params.id, fetch),
			listFindings(params.id, fetch)
		]);
		return { application, findings };
	} catch {
		throw error(404, 'Application not found');
	}
};
