import { error } from '@sveltejs/kit';
import { listModernizationRecommendations } from '$lib/api';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async ({ fetch, params }) => {
	const recommendations = await listModernizationRecommendations(params.id, fetch);
	const recommendation = recommendations.find((r) => r.id === params.recId);
	if (!recommendation) {
		throw error(404, 'Recommendation not found');
	}

	return new Response(JSON.stringify(recommendation, null, 2), {
		headers: {
			'Content-Type': 'application/json',
			'Content-Disposition': `attachment; filename="modernization-recommendation-${recommendation.id}.json"`
		}
	});
};
