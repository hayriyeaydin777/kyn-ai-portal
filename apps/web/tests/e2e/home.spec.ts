import { expect, test } from '@playwright/test';

test('home page renders the portal title', async ({ page }) => {
	await page.goto('/');
	await expect(page.getByRole('heading', { name: /Resilience Operations/i })).toBeVisible();
});
