import { listApplications } from '$lib/api';
import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async ({ fetch }) => {
	try {
		const applications = await listApplications(fetch);
		return { applications };
	} catch {
		return { applications: [] };
	}
};
