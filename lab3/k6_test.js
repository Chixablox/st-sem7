import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  scenarios: {
    stress_test: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '1m', target: 50 },
        { duration: '1m', target: 50 },
        { duration: '30s', target: 0 },
      ],
    },
  },
  thresholds: {
    'http_req_duration{name: "GET /posts"}': ['p(95)<500'],
    'http_req_duration{name: "POST /posts"}': ['p(95)<2000'],
    'checks': ['rate>=0.99'],
  },
};

export default function () {
  let r = Math.random();

  const BASE = "http://localhost:5000";

  if (r < 0.9) {
    let res = http.get(`${BASE}/posts`, {
      tags: { name: "GET /posts" },
    });

    check(res, {
      "Статус ответа 200": (r) => r.status === 200,
      'Ответ содержит данные': (r) => r.body.length > 0,
    });

  } else {
    let payload = JSON.stringify({
        author: "Егор",
        title: "Обезьяний побег",
        content: "14.11.2025 в 12:00 по Гринвичу из Новосибирского зоопарка сбежало три макаки. Их точное местоположение до сих пор неизвестно.",
    })

    let res = http.post(
      `${BASE}/posts`,
        payload,
      {
        headers: { "Content-Type": "application/json" },
        tags: { name: "POST /posts" },
      }
    );

    check(res, {
      "Статус ответа 201": (r) => r.status === 201,
      'Ответ содержит данные': (r) => r.body.length > 0,
    });
  }

  sleep(1);
}