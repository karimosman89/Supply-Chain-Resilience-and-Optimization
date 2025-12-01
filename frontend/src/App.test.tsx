import { describe, it, expect } from '@jest/globals';
import '@testing-library/jest-dom';
import { render, screen } from '@testing-library/react';
import App from './App';

describe('App Component', () => {
  it('renders without crashing', () => {
    render(<App />);
    
    // Test that the app renders properly using basic assertions
    const body = document.body;
    expect(body).toBeTruthy();
    expect(body.children.length).toBeGreaterThan(0);
    
    // Test text content using screen queries
    const title = screen.getByText('Supply Chain Resilience & Optimization Platform');
    expect(title).toBeTruthy();
  });

  it('displays welcome message', () => {
    render(<App />);
    
    // Test that welcome message is displayed
    const welcomeText = screen.getByText('Welcome to the Supply Chain Analytics Dashboard');
    expect(welcomeText).toBeTruthy();
  });

  it('shows platform description', () => {
    render(<App />);
    
    // Test that platform description is shown
    const description = screen.getByText(/This platform provides real-time analytics/);
    expect(description).toBeTruthy();
  });

  it('has proper structure', () => {
    render(<App />);
    
    // Test structure using testing library
    expect(document.body.children.length).toBeGreaterThan(0);
    const heading = screen.getByRole('heading');
    expect(heading).toBeTruthy();
    expect(heading.textContent).toContain('Supply Chain Resilience & Optimization Platform');
  });
});
