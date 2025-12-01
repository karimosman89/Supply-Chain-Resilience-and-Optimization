"""
End-to-end tests for Supply Chain Platform frontend and backend integration.
"""
const puppeteer = require('puppeteer');

describe('Supply Chain Platform E2E Tests', () => {
  let browser;
  let page;

  beforeAll(async () => {
    browser = await puppeteer.launch();
    page = await browser.newPage();
  });

  afterAll(async () => {
    await browser.close();
  });

  test('should load homepage successfully', async () => {
    await page.goto('http://localhost:3000');
    const title = await page.title();
    expect(title).toBe('Supply Chain Analytics Dashboard');
  });

  test('should display navigation menu', async () => {
    await page.goto('http://localhost:3000');
    const navElement = await page.waitForSelector('nav');
    expect(navElement).toBeTruthy();
  });

  test('should show KPI cards on dashboard', async () => {
    await page.goto('http://localhost:3000');
    const kpiCards = await page.$$('.kpi-card');
    expect(kpiCards.length).toBeGreaterThan(0);
  });

  test('should navigate between pages', async () => {
    await page.goto('http://localhost:3000');
    
    // Test navigation to analytics page
    await page.click('[data-testid="analytics-link"]');
    await page.waitForSelector('.analytics-content');
    
    // Test navigation to suppliers page
    await page.click('[data-testid="suppliers-link"]');
    await page.waitForSelector('.suppliers-content');
    
    // Test navigation back to dashboard
    await page.click('[data-testid="dashboard-link"]');
    await page.waitForSelector('.dashboard-content');
  });

  test('should display charts on analytics page', async () => {
    await page.goto('http://localhost:3000/analytics');
    const charts = await page.$$('.chart-container');
    expect(charts.length).toBeGreaterThan(0);
  });

  test('should handle responsive design', async () => {
    // Test mobile view
    await page.setViewport({ width: 375, height: 667 });
    await page.goto('http://localhost:3000');
    
    const mobileMenu = await page.$('.mobile-menu');
    expect(mobileMenu).toBeTruthy();
    
    // Reset viewport
    await page.setViewport({ width: 1920, height: 1080 });
  });
});