import { describe, it, expect } from '@jest/globals';
import '@testing-library/jest-dom';
import { render, screen } from '@testing-library/react';
import App from './App';

describe('App Component', () => {
  it('renders without crashing', () => {
    render(<App />);
    
    // Test that the app renders properly
    expect(document.body).toBeInTheDocument();
    expect(screen.getByText('Supply Chain Resilience & Optimization Platform')).toBeInTheDocument();
  });

  it('displays welcome message', () => {
    render(<App />);
    
    // Test that welcome message is displayed
    expect(screen.getByText('Welcome to the Supply Chain Analytics Dashboard')).toBeInTheDocument();
  });

  it('shows platform description', () => {
    render(<App />);
    
    // Test that platform description is shown
    expect(screen.getByText(/This platform provides real-time analytics/)).toBeInTheDocument();
  });

  it('has proper structure', () => {
    render(<App />);
    
    // Test structure using testing library
    expect(document.body.children.length).toBeGreaterThan(0);
    expect(screen.getByRole('heading')).toBeInTheDocument();
    expect(screen.getByText('Supply Chain Resilience & Optimization Platform')).toBeInTheDocument();
  });
});
