import { fail } from '@sveltejs/kit';
import { createCodeReview } from '$lib/api';
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
	}
};
