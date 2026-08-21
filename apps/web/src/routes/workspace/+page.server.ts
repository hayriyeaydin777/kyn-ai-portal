import { fail } from '@sveltejs/kit';
import { createCodeReview, createDocumentationDraft, createTestGeneration } from '$lib/api';
import type { Actions } from './$types';

export const actions: Actions = {
	reviewCode: async ({ fetch, request }) => {
		const formData = await request.formData();
		const source = String(formData.get('source') ?? '');
		try {
			const review = await createCodeReview(source, fetch);
			return { review };
		} catch {
			return fail(502, { message: 'Code review failed.' });
		}
	},
	generateTests: async ({ fetch, request }) => {
		const formData = await request.formData();
		const source = String(formData.get('source') ?? '');
		try {
			const suite = await createTestGeneration(source, fetch);
			return { suite };
		} catch {
			return fail(502, { message: 'Test generation failed.' });
		}
	},
	generateDocs: async ({ fetch, request }) => {
		const formData = await request.formData();
		const source = String(formData.get('source') ?? '');
		try {
			const draft = await createDocumentationDraft(source, fetch);
			return { draft };
		} catch {
			return fail(502, { message: 'Documentation generation failed.' });
		}
	}
};
