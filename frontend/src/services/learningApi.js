import api from './api';

export const learningApi = {
  getCourses: (params) => api.get('/learning/courses', { params }),
  createCourse: (data) => api.post('/learning/courses', data),
  getEnrollments: () => api.get('/learning/enrollments'),
  enrollCourse: (data) => api.post('/learning/enrollments', data),
  submitQuiz: (quizId, data) => api.post(`/learning/quizzes/${quizId}/submit`, data),
  getCertificates: () => api.get('/learning/certificates'),
};

export default learningApi;
