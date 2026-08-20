import type { Handle } from '@sveltejs/kit';
import { randomUUID } from 'node:crypto';

const CORRELATION_ID_HEADER = 'x-correlation-id';

export const handle: Handle = async ({ event, resolve }) => {
	const correlationId = event.request.headers.get(CORRELATION_ID_HEADER) ?? randomUUID();
	event.locals.correlationId = correlationId;

	const response = await resolve(event);
	response.headers.set(CORRELATION_ID_HEADER, correlationId);
	return response;
};
