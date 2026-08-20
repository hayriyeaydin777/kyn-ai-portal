import { listApplications } from '$lib/api';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ fetch }) => {
	const applications = await listApplications(fetch);
	return { applications };
};
