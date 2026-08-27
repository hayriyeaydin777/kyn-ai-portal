import { fail } from '@sveltejs/kit';
import { decideBrief, generateBrief, listApplications, listBriefs } from '$lib/api';
import type { Actions, PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ fetch, url }) => {
	const applications = await listApplications(fetch);
	const applicationId = url.searchParams.get('app') ?? applications[0]?.id ?? null;
	const briefs = applicationId ? await listBriefs(applicationId, fetch) : [];
	return { applications, applicationId, briefs };
};

export const actions: Actions = {
	generateBrief: async ({ fetch, request }) => {
		const formData = await request.formData();
		const applicationId = String(formData.get('applicationId') ?? '');
		try {
			await generateBrief(applicationId, fetch);
		} catch {
			return fail(502, { message: 'Brief generation failed.' });
		}
	},
	approveBrief: async ({ fetch, request }) => {
		const formData = await request.formData();
		const applicationId = String(formData.get('applicationId') ?? '');
		const briefId = String(formData.get('briefId') ?? '');
		try {
			await decideBrief(applicationId, briefId, 'approve', fetch);
		} catch {
			return fail(502, { message: 'Approval failed.' });
		}
	},
	rejectBrief: async ({ fetch, request }) => {
		const formData = await request.formData();
		const applicationId = String(formData.get('applicationId') ?? '');
		const briefId = String(formData.get('briefId') ?? '');
		try {
			await decideBrief(applicationId, briefId, 'reject', fetch);
		} catch {
			return fail(502, { message: 'Rejection failed.' });
		}
	}
};
