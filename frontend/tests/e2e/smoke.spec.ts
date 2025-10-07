import { test, expect } from '@playwright/test';

test('homepage has call to action', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await expect(page.getByRole('link', { name: 'Vai al carrello' })).toBeVisible();
});
