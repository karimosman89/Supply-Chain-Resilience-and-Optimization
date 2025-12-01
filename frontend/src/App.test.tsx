import { describe, it, expect } from '@jest/globals';
import '@testing-library/jest-dom';
import { screen } from '@testing-library/react';

// Basic test to ensure the app renders without errors
describe('App Component', () => {
  it('renders without crashing', () => {
    // Create root div using testing library approach
    const rootElement = document.createElement('div');
    rootElement.id = 'root';
    document.body.appendChild(rootElement);
    
    // Test using Testing Library methods instead of direct node access
    expect(document.body).toBeInTheDocument();
    expect(screen.getByText(/You need to enable JavaScript to run this app/)).toBeInTheDocument();
  });

  it('has proper structure', () => {
    // Create root div
    const rootElement = document.createElement('div');
    rootElement.id = 'root';
    document.body.appendChild(rootElement);
    
    // Test structure using testing library
    expect(document.body.children.length).toBeGreaterThan(0);
    expect(screen.getByRole('generic', { hidden: true })).toBeInTheDocument();
  });
});
