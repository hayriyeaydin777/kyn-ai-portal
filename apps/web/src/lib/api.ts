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

export interface Brief {
	id: string;
	application_id: string;
	provider: string;
	text: string;
	citations: string[];
	status: string;
	created_at: string;
}

export interface ModernizationCase {
	id: string;
	application_id: string;
	technology_stack: string;
	hosting: string;
	release_process: string;
	scale: string;
	pain_points: string;
	created_at: string;
}

export interface RiskSignal {
	rule_id: string;
	severity: string;
	message: string;
}

export interface ModernizationRecommendation {
	id: string;
	application_id: string;
	modernization_case_id: string;
	complexity_score: number;
	risk_signals: RiskSignal[];
	matched_option_ids: string[];
	provider: string;
	narrative: string;
	citations: string[];
	status: string;
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

async function postJson<T>(path: string, fetchFn: typeof fetch, body?: unknown): Promise<T> {
	const response = await fetchFn(`${API_BASE_URL}${path}`, {
		method: 'POST',
		...(body !== undefined && {
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify(body)
		})
	});
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

export function listBriefs(id: string, fetchFn: typeof fetch): Promise<Brief[]> {
	return getJson(`/v1/applications/${id}/briefs`, fetchFn);
}

export function generateBrief(id: string, fetchFn: typeof fetch): Promise<Brief> {
	return postJson(`/v1/applications/${id}/briefs`, fetchFn);
}

export function decideBrief(
	applicationId: string,
	briefId: string,
	decision: 'approve' | 'reject',
	fetchFn: typeof fetch
): Promise<Brief> {
	return postJson(`/v1/applications/${applicationId}/briefs/${briefId}/approvals`, fetchFn, { decision });
}

export function listModernizationCases(id: string, fetchFn: typeof fetch): Promise<ModernizationCase[]> {
	return getJson(`/v1/applications/${id}/modernization-cases`, fetchFn);
}

export function createModernizationCase(
	applicationId: string,
	payload: {
		technology_stack: string;
		hosting: string;
		release_process: string;
		scale: string;
		pain_points: string;
	},
	fetchFn: typeof fetch
): Promise<ModernizationCase> {
	return postJson(`/v1/applications/${applicationId}/modernization-cases`, fetchFn, payload);
}

export function listModernizationRecommendations(
	id: string,
	fetchFn: typeof fetch
): Promise<ModernizationRecommendation[]> {
	return getJson(`/v1/applications/${id}/modernization-recommendations`, fetchFn);
}

export function createModernizationRecommendation(
	applicationId: string,
	caseId: string,
	fetchFn: typeof fetch
): Promise<ModernizationRecommendation> {
	return postJson(
		`/v1/applications/${applicationId}/modernization-recommendations?case_id=${caseId}`,
		fetchFn
	);
}
