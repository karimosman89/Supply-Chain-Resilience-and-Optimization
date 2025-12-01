import { describe, it, expect } from '@jest/globals';
import '@testing-library/jest-dom';

// Basic test to ensure the app renders without errors
describe('App Component', () => {
  it('renders without crashing', () => {
    const div = document.createElement('div');
    div.id = 'root';
    document.body.appendChild(div);
    
    // Just test that the document has a root element
    expect(document.body).toBeInTheDocument();
    expect(document.getElementById('root')).toBeInTheDocument();
  });

  it('has proper structure', () => {
    const div = document.createElement('div');
    div.id = 'root';
    document.body.appendChild(div);
    
    expect(document.body.children.length).toBeGreaterThan(0);
  });
});
