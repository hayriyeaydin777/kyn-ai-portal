import { error } from '@sveltejs/kit';
import { getApplication, listDependencies } from '$lib/api';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ fetch, params }) => {
	try {
		const [application, dependencies] = await Promise.all([
			getApplication(params.id, fetch),
			listDependencies(params.id, fetch)
		]);
		return { application, dependencies };
	} catch {
		throw error(404, 'Application not found');
	}
};
