export interface ApplicationProfile {
	id: string;
	name: string;
	description: string | null;
	business_owner: string | null;
	criticality: string;
	created_at: string;
	updated_at: string;
}

export interface Dependency {
	id: string;
	application_id: string;
	name: string;
	dependency_type: string;
	criticality: string;
	notes: string | null;
	created_at: string;
}

export interface EvidenceArtifact {
	id: string;
	application_id: string;
	title: string;
	source: string;
	reference: string | null;
	created_at: string;
}

export interface Finding {
	id: string;
	application_id: string;
	rule_id: string;
	severity: string;
	message: string;
	evidence_fields: string[];
	created_at: string;
}

const API_BASE_URL = process.env.API_BASE_URL ?? 'http://127.0.0.1:8000';

async function getJson<T>(path: string, fetchFn: typeof fetch): Promise<T> {
	const response = await fetchFn(`${API_BASE_URL}${path}`);
	if (!response.ok) {
		throw new Error(`Request to ${path} failed with status ${response.status}`);
	}
	return response.json() as Promise<T>;
}

async function postJson<T>(path: string, fetchFn: typeof fetch): Promise<T> {
	const response = await fetchFn(`${API_BASE_URL}${path}`, { method: 'POST' });
	if (!response.ok) {
		throw new Error(`Request to ${path} failed with status ${response.status}`);
	}
	return response.json() as Promise<T>;
}

export function listApplications(fetchFn: typeof fetch): Promise<ApplicationProfile[]> {
	return getJson('/v1/applications', fetchFn);
}

export function getApplication(id: string, fetchFn: typeof fetch): Promise<ApplicationProfile> {
	return getJson(`/v1/applications/${id}`, fetchFn);
}

export function listDependencies(id: string, fetchFn: typeof fetch): Promise<Dependency[]> {
	return getJson(`/v1/applications/${id}/dependencies`, fetchFn);
}

export function listEvidence(id: string, fetchFn: typeof fetch): Promise<EvidenceArtifact[]> {
	return getJson(`/v1/applications/${id}/evidence`, fetchFn);
}

export function listFindings(id: string, fetchFn: typeof fetch): Promise<Finding[]> {
	return getJson(`/v1/applications/${id}/assessments`, fetchFn);
}

export function triggerAssessment(id: string, fetchFn: typeof fetch): Promise<Finding[]> {
	return postJson(`/v1/applications/${id}/assessments`, fetchFn);
}
