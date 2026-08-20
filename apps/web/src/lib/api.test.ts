import { describe, expect, it, vi } from 'vitest';
import { getApplication, listApplications, listFindings, triggerAssessment } from './api';

describe('api client', () => {
	it('listApplications returns parsed JSON on success', async () => {
		const mockFetch = vi.fn().mockResolvedValue({
			ok: true,
			json: async () => [{ id: '1', name: 'Northstar Claims Service' }]
		});

		const result = await listApplications(mockFetch as unknown as typeof fetch);

		expect(result).toEqual([{ id: '1', name: 'Northstar Claims Service' }]);
		expect(mockFetch).toHaveBeenCalledWith(expect.stringContaining('/v1/applications'));
	});

	it('throws when the response is not ok', async () => {
		const mockFetch = vi.fn().mockResolvedValue({ ok: false, status: 500 });

		await expect(listApplications(mockFetch as unknown as typeof fetch)).rejects.toThrow(
			/failed with status 500/
		);
	});

	it('getApplication requests the correct path', async () => {
		const mockFetch = vi.fn().mockResolvedValue({
			ok: true,
			json: async () => ({ id: 'abc', name: 'Aurora Customer Portal' })
		});

		await getApplication('abc', mockFetch as unknown as typeof fetch);

		expect(mockFetch).toHaveBeenCalledWith(expect.stringContaining('/v1/applications/abc'));
	});

	it('listFindings requests the assessments path', async () => {
		const mockFetch = vi.fn().mockResolvedValue({ ok: true, json: async () => [] });

		await listFindings('abc', mockFetch as unknown as typeof fetch);

		expect(mockFetch).toHaveBeenCalledWith(expect.stringContaining('/v1/applications/abc/assessments'));
	});

	it('triggerAssessment posts to the assessments path', async () => {
		const mockFetch = vi.fn().mockResolvedValue({ ok: true, json: async () => [] });

		await triggerAssessment('abc', mockFetch as unknown as typeof fetch);

		expect(mockFetch).toHaveBeenCalledWith(
			expect.stringContaining('/v1/applications/abc/assessments'),
			{ method: 'POST' }
		);
	});
});
