/**
 * Load test for Supply Chain Platform
 * Run with: k6 run tests/load/load-test.js
 */
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');

export const options = {
  stages: [
    { duration: '2m', target: 100 }, // Ramp up to 100 users
    { duration: '5m', target: 100 }, // Stay at 100 users
    { duration: '2m', target: 200 }, // Ramp up to 200 users
    { duration: '5m', target: 200 }, // Stay at 200 users
    { duration: '2m', target: 0 },   // Ramp down to 0 users
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests should be below 500ms
    http_req_failed: ['rate<0.1'],    // Error rate should be below 10%
    errors: ['rate<0.1'],
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost:8000';

export default function() {
  // Test homepage
  let response = http.get(`${BASE_URL}/`);
  check(response, {
    'homepage status is 200': (r) => r.status === 200,
    'homepage loads quickly': (r) => r.timings.duration < 500,
  }) || errorRate.add(1);

  sleep(1);

  // Test health endpoint
  response = http.get(`${BASE_URL}/health`);
  check(response, {
    'health check status is 200': (r) => r.status === 200,
    'health response is valid': (r) => {
      try {
        const body = JSON.parse(r.body);
        return body.status === 'healthy';
      } catch (e){
        return false;
      }
    },
  }) || errorRate.add(1);

  sleep(1);

  // Test analytics endpoints
  const endpoints = [
    '/analytics/overview',
    '/analytics/performance',
    '/analytics/trends',
    '/suppliers',
    '/warehouses',
    '/shipments'
  ];

  for (let endpoint of endpoints) {
    response = http.get(`${BASE_URL}${endpoint}`);
    check(response, {
      [`${endpoint} status is 200`]: (r) => r.status === 200,
      [`${endpoint} response time < 1000ms`]: (r) => r.timings.duration < 1000,
    }) || errorRate.add(1);
    
    sleep(0.5);
  }

  // Test POST endpoints (with sample data)
  const postData = {
    supplier: {
      name: 'Test Supplier',
      country: 'US',
      lead_time_days: 7
    }
  };

  response = http.post(`${BASE_URL}/suppliers`, JSON.stringify(postData), {
    headers: { 'Content-Type': 'application/json' },
  });
  
  check(response, {
    'supplier creation status is 201': (r) => r.status === 201,
    'supplier creation response time < 1000ms': (r) => r.timings.duration < 1000,
  }) || errorRate.add(1);

  sleep(2);
}

// Summary function
export function handleSummary(data) {
  return {
    'tests/load/results.json': JSON.stringify(data),
    'tests/load/results.html': htmlReport(data),
  };
}

function htmlReport(data) {
  return `
  <!DOCTYPE html>
  <html>
  <head>
    <title>Load Test Results</title>
    <style>
      body { font-family: Arial, sans-serif; margin: 20px; }
      .metric { margin: 10px 0; padding: 10px; border: 1px solid #ccc; }
      .success { background-color: #d4edda; }
      .error { background-color: #f8d7da; }
    </style>
  </head>
  <body>
    <h1>Supply Chain Platform Load Test Results</h1>
    <div class="metric">
      <h3>Duration</h3>
      <p>Total: ${data.state.testRunDurationMs}ms</p>
    </div>
    <div class="metric">
      <h3>Requests</h3>
      <p>Total: ${data.metrics.http_reqs.count}</p>
      <p>Rate: ${data.metrics.http_reqs.rate} req/s</p>
    </div>
    <div class="metric">
      <h3>Response Times</h3>
      <p>Average: ${data.metrics.http_req_duration.avg}ms</p>
      <p>95th percentile: ${data.metrics.http_req_duration['p(95)']}ms</p>
      <p>99th percentile: ${data.metrics.http_req_duration['p(99)']}ms</p>
    </div>
    <div class="metric">
      <h3>Error Rate</h3>
      <p>${data.metrics.http_req_failed.rate * 100}%</p>
    </div>
  </body>
  </html>
  `;
}
