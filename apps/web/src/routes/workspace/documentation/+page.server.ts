import { fail } from '@sveltejs/kit';
import { createDocumentationDraft } from '$lib/api';
import type { Actions } from './$types';

export const actions: Actions = {
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
