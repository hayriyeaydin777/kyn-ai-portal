import { fail } from '@sveltejs/kit';
import { createTestGeneration } from '$lib/api';
import type { Actions } from './$types';

export const actions: Actions = {
	generateTests: async ({ fetch, request }) => {
		const formData = await request.formData();
		const source = String(formData.get('source') ?? '');
		try {
			const suite = await createTestGeneration(source, fetch);
			return { suite };
		} catch {
			return fail(502, { message: 'Test generation failed.' });
		}
	}
};
