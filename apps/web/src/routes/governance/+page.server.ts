import { fail } from '@sveltejs/kit';
import {
	acceptArchitectureDecision,
	createArchitectureDecision,
	listArchitectureDecisions,
	proposeArchitectureDecision,
	rejectArchitectureDecision
} from '$lib/api';
import type { Actions, PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ fetch }) => {
	const decisions = await listArchitectureDecisions(fetch);
	return { decisions };
};

export const actions: Actions = {
	createDecision: async ({ fetch, request }) => {
		const formData = await request.formData();
		const payload = {
			title: String(formData.get('title') ?? ''),
			context: String(formData.get('context') ?? ''),
			drivers: String(formData.get('drivers') ?? ''),
			decision: String(formData.get('decision') ?? ''),
			consequences: String(formData.get('consequences') ?? '')
		};
		try {
			await createArchitectureDecision(payload, fetch);
		} catch {
			return fail(502, { message: 'Could not create architecture decision.' });
		}
	},
	propose: async ({ fetch, request }) => {
		const formData = await request.formData();
		const decisionId = String(formData.get('decisionId') ?? '');
		try {
			await proposeArchitectureDecision(decisionId, fetch);
		} catch {
			return fail(502, { message: 'Could not propose decision.' });
		}
	},
	accept: async ({ fetch, request }) => {
		const formData = await request.formData();
		const decisionId = String(formData.get('decisionId') ?? '');
		try {
			await acceptArchitectureDecision(decisionId, fetch);
		} catch {
			return fail(502, { message: 'Could not accept decision.' });
		}
	},
	reject: async ({ fetch, request }) => {
		const formData = await request.formData();
		const decisionId = String(formData.get('decisionId') ?? '');
		try {
			await rejectArchitectureDecision(decisionId, fetch);
		} catch {
			return fail(502, { message: 'Could not reject decision.' });
		}
	}
};
