import { test, expect } from '@playwright/test';

test.describe('Dashboard Flow', () => {
  test('should load the dashboard and display main sections', async ({ page }) => {
    // Navigate to dashboard
    await page.goto('/');

    // Check header
    await expect(page.getByRole('heading', { name: /Opportunity-Discovery Engine/i })).toBeVisible();

    // Check KPI Section
    await expect(page.getByText('Items Scraped')).toBeVisible();

    // Check Opportunities section
    await expect(page.getByRole('heading', { name: /Opportunities/i })).toBeVisible();
    await expect(page.getByText('High Volume of Affected Users')).toBeVisible();
  });

  test('should allow asking a research query in the chat', async ({ page }) => {
    await page.goto('/');
    
    // Find the chat input
    const chatInput = page.getByPlaceholder(/Ask a research question.../i);
    await expect(chatInput).toBeVisible();

    // Type a query and submit
    await chatInput.fill('What do people complain about size?');
    await chatInput.press('Enter');

    // Chat messages should appear (just checking the loading state or that the input cleared)
    // Wait for the input to be cleared (our new behavior)
    await expect(chatInput).toHaveValue('');
    
    // The user's query should be visible in the chat list
    await expect(page.getByText('What do people complain about size?')).toBeVisible();
  });
});
