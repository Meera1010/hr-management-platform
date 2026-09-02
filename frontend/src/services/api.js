const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001/api';


const getHeaders = () => {
  const headers = { 'Content-Type': 'application/json' };
  const token = localStorage.getItem('token');
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
};

async function handleResponse(response) {
  const data = await response.json();
  if (!response.ok) {
    return { success: false, message: data.message || 'Something went wrong' };
  }
  return { success: true, data: data.data || data };
}

async function fetchWithAuth(endpoint, options = {}) {
  const response = await fetch(`${BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      ...getHeaders(),
      ...options.headers,
    },
  });
  return handleResponse(response);
}

const api = {
  get: (endpoint) => fetchWithAuth(endpoint, { method: 'GET' }),
  post: (endpoint, body) => fetchWithAuth(endpoint, { method: 'POST', body: JSON.stringify(body) }),
  put: (endpoint, body) => fetchWithAuth(endpoint, { method: 'PUT', body: JSON.stringify(body) }),
  patch: (endpoint, body) => fetchWithAuth(endpoint, { method: 'PATCH', body: JSON.stringify(body) }),
  delete: (endpoint) => fetchWithAuth(endpoint, { method: 'DELETE' }),
};

export default api;

// Keep original exports but adapt to new api pattern
export const getUsers = async () => {
  const res = await api.get('/users/');
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const getUser = async (id) => {
  const res = await api.get(`/users/${id}`);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const createUser = async (data) => {
  const res = await api.post('/users/', data);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const updateUser = async (id, data) => {
  const res = await api.put(`/users/${id}`, data);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const deactivateUser = async (id) => {
  const res = await api.delete(`/users/${id}`);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const getRoles = async () => {
  const res = await api.get('/roles/');
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const getRole = async (id) => {
  const res = await api.get(`/roles/${id}`);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const getEmployees = async (params = {}) => {
  const query = new URLSearchParams(params).toString();
  const res = await api.get(`/employees/?${query}`);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

// Jobs API
export const getJobs = async (params = {}) => {
  const query = new URLSearchParams(params).toString();
  const res = await api.get(`/jobs/?${query}`);
  if (!res.success) throw new Error(res.message);
  return res;
};

export const searchJobs = async (q) => {
  const res = await api.get(`/jobs/search?q=${encodeURIComponent(q)}`);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const getJob = async (id) => {
  const res = await api.get(`/jobs/${id}`);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const createJob = async (data) => {
  const res = await api.post('/jobs/', data);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const updateJob = async (id, data) => {
  const res = await api.put(`/jobs/${id}`, data);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

// Candidate API
export const getCandidates = async (params) => {
  const query = new URLSearchParams(params).toString();
  const res = await api.get(`/candidates/?${query}`);
  if (!res.success) throw new Error(res.message);
  return res.data;
};
export const getCandidate = async (id) => {
  const res = await api.get(`/candidates/${id}`);
  if (!res.success) throw new Error(res.message);
  return res.data;
};
export const createCandidate = async (data) => {
  const res = await api.post('/candidates/', data);
  if (!res.success) throw new Error(res.message);
  return res.data;
};
export const updateCandidate = async (id, data) => {
  const res = await api.put(`/candidates/${id}`, data);
  if (!res.success) throw new Error(res.message);
  return res.data;
};
export const updateCandidateStatus = async (id, status) => {
  const res = await api.patch(`/candidates/${id}/status`, { status });
  if (!res.success) throw new Error(res.message);
  return res.data;
};

// Application API
export const getApplications = async (params) => {
  const query = new URLSearchParams(params).toString();
  const res = await api.get(`/applications/?${query}`);
  if (!res.success) throw new Error(res.message);
  return res.data;
};
export const getApplication = async (id) => {
  const res = await api.get(`/applications/${id}`);
  if (!res.success) throw new Error(res.message);
  return res.data;
};
export const createApplication = async (data) => {
  const res = await api.post('/applications/', data);
  if (!res.success) throw new Error(res.message);
  return res.data;
};
export const updateApplicationStatus = async (id, data) => {
  const res = await api.patch(`/applications/${id}/status`, data);
  if (!res.success) throw new Error(res.message);
  return res.data;
};
export const withdrawApplication = async (id) => {
  const res = await api.delete(`/applications/${id}`);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const changeJobStatus = async (id, status) => {
  const res = await fetchWithAuth(`/jobs/${id}/status`, {
    method: 'PATCH',
    body: JSON.stringify({ status })
  });
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const archiveJob = async (id) => {
  const res = await api.delete(`/jobs/${id}`);
  if (!res.success) throw new Error(res.message);
  return res;
};

// Resume API Services
export const uploadResume = async (formData) => {
  const token = localStorage.getItem('token');
  const response = await fetch(`${BASE_URL}/resumes/upload`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`
    },
    body: formData
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.message || 'Failed to upload resume');
  return data.data;
};

export const getResumes = async (params = {}) => {
  const query = new URLSearchParams(params).toString();
  const res = await api.get(`/resumes?${query}`);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const getResume = async (id) => {
  const res = await api.get(`/resumes/${id}`);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const deleteResume = async (id) => {
  const res = await api.delete(`/resumes/${id}`);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const downloadResume = async (id) => {
  const token = localStorage.getItem('token');
  const response = await fetch(`${BASE_URL}/resumes/${id}/download`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  if (!response.ok) throw new Error('Download failed');
  const blob = await response.blob();
  return blob;
};

export const extractSkills = async (id) => {
  const token = localStorage.getItem('token');
  const response = await fetch(`${BASE_URL}/resumes/${id}/extract-skills`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.message || 'Failed to extract skills');
  return data.data;
};

// Job Matching API Services
export const getCandidateMatches = async (candidateId) => {
  const res = await api.get(`/candidates/${candidateId}/matches`);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const getJobCandidateMatches = async (jobId, candidateId) => {
  const res = await api.get(`/jobs/${jobId}/match/${candidateId}`);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const getJobCandidateMatchesList = async (jobId) => {
  const res = await api.get(`/jobs/${jobId}/matches`);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

// ============================================================
// STEP 9: Candidate Ranking, Interviews, Feedback, Offers
// ============================================================

// Candidate Ranking
export const getCandidateRankings = async (jobId) => {
  const res = await api.get(`/jobs/${jobId}/rank-candidates`);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

// Shortlist Application
export const shortlistApplication = async (appId) => {
  const res = await fetch(`${BASE_URL}/applications/${appId}/shortlist`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${localStorage.getItem('token')}` }
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.message || 'Failed to shortlist');
  return data;
};

// Interviews
export const getInterviews = async (params = '') => {
  const res = await api.get(`/interviews${params}`);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const getInterview = async (id) => {
  const res = await api.get(`/interviews/${id}`);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const createInterview = async (payload) => {
  const res = await api.post('/interviews', payload);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const updateInterview = async (id, payload) => {
  const res = await api.put(`/interviews/${id}`, payload);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const updateInterviewStatus = async (id, status) => {
  const res = await fetch(`${BASE_URL}/interviews/${id}/status`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${localStorage.getItem('token')}` },
    body: JSON.stringify({ status })
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.message || 'Failed to update status');
  return data;
};

export const deleteInterview = async (id) => {
  const res = await api.delete(`/interviews/${id}`);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

// Interview Feedback
export const submitInterviewFeedback = async (interviewId, payload) => {
  const res = await api.post(`/interviews/${interviewId}/feedback`, payload);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const getInterviewFeedback = async (interviewId) => {
  const res = await api.get(`/interviews/${interviewId}/feedback`);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const updateInterviewFeedback = async (interviewId, payload) => {
  const res = await api.put(`/interviews/${interviewId}/feedback`, payload);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

// Offers
export const getOffers = async () => {
  const res = await api.get('/offers');
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const getOffer = async (id) => {
  const res = await api.get(`/offers/${id}`);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const createOffer = async (payload) => {
  const res = await api.post('/offers', payload);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const updateOffer = async (id, payload) => {
  const res = await api.put(`/offers/${id}`, payload);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const updateOfferStatus = async (id, status) => {
  const res = await fetch(`${BASE_URL}/offers/${id}/status`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${localStorage.getItem('token')}` },
    body: JSON.stringify({ status })
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.message || 'Failed to update offer status');
  return data;
};

export const deleteOffer = async (id) => {
  const res = await api.delete(`/offers/${id}`);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const acceptOffer = async (id) => {
  const res = await api.post(`/offers/${id}/accept`, {});
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const declineOffer = async (id) => {
  const res = await api.post(`/offers/${id}/decline`, {});
  if (!res.success) throw new Error(res.message);
  return res.data;
};

// ============================================================
// Attendance Management
// ============================================================
export const getAttendance = async (params = {}) => {
  const query = new URLSearchParams(params).toString();
  const res = await api.get(`/attendance?${query}`);
  if (!res.success) throw new Error(res.message || 'Failed to fetch attendance');
  return res;
};

export const createAttendance = async (data) => {
  const res = await api.post('/attendance', data);
  if (!res.success) throw new Error(res.message || 'Failed to record attendance');
  return res.data;
};

export const updateAttendance = async (id, data) => {
  const res = await api.put(`/attendance/${id}`, data);
  if (!res.success) throw new Error(res.message || 'Failed to update attendance');
  return res.data;
};

export const checkIn = async (data = {}) => {
  const res = await api.post('/attendance/check-in', data);
  if (!res.success) throw new Error(res.message || 'Failed to check in');
  return res.data;
};

export const checkOut = async (data = {}) => {
  const res = await api.post('/attendance/check-out', data);
  if (!res.success) throw new Error(res.message || 'Failed to check out');
  return res.data;
};

export const getAttendanceSummary = async (params = {}) => {
  const query = new URLSearchParams(params).toString();
  const res = await api.get(`/attendance/summary?${query}`);
  if (!res.success) throw new Error(res.message || 'Failed to fetch attendance summary');
  return res.data;
};

// ============================================================
// Leave Management
// ============================================================
export const getLeaves = async (params = {}) => {
  const query = new URLSearchParams(params).toString();
  const res = await api.get(`/leaves?${query}`);
  if (!res.success) throw new Error(res.message || 'Failed to fetch leaves');
  return res;
};

export const createLeave = async (data) => {
  const res = await api.post('/leaves', data);
  if (!res.success) throw new Error(res.message || 'Failed to submit leave request');
  return res.data;
};

export const approveLeave = async (id, comments = '') => {
  const res = await api.post(`/leaves/${id}/approve`, { comments });
  if (!res.success) throw new Error(res.message || 'Failed to approve leave');
  return res.data;
};

export const rejectLeave = async (id, comments = '') => {
  const res = await api.post(`/leaves/${id}/reject`, { comments });
  if (!res.success) throw new Error(res.message || 'Failed to reject leave');
  return res.data;
};

export const cancelLeave = async (id) => {
  const res = await api.post(`/leaves/${id}/cancel`, {});
  if (!res.success) throw new Error(res.message || 'Failed to cancel leave');
  return res.data;
};

// ============================================================
// Performance Management
// ============================================================
export const getPerformanceReviews = async (params = {}) => {
  const query = new URLSearchParams(params).toString();
  const res = await api.get(`/performance?${query}`);
  if (!res.success) throw new Error(res.message || 'Failed to fetch performance reviews');
  return res;
};

export const createPerformanceReview = async (data) => {
  const res = await api.post('/performance', data);
  if (!res.success) throw new Error(res.message || 'Failed to create performance review');
  return res.data;
};

export const updatePerformanceReview = async (id, data) => {
  const res = await api.put(`/performance/${id}`, data);
  if (!res.success) throw new Error(res.message || 'Failed to update performance review');
  return res.data;
};

export const deletePerformanceReview = async (id) => {
  const res = await api.delete(`/performance/${id}`);
  if (!res.success) throw new Error(res.message || 'Failed to delete performance review');
  return res.data;
};

// ============================================================
// Training & Notifications
// ============================================================
export const getTrainingCourses = async (params = {}) => {
  const query = new URLSearchParams(params).toString();
  const res = await api.get(`/training/courses?${query}`);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const createTrainingCourse = async (data) => {
  const res = await api.post('/training/courses', data);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const assignTraining = async (data) => {
  const res = await api.post('/training/assignments', data);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const getMyTrainings = async () => {
  const res = await api.get('/training/my-trainings');
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const updateTrainingAssignment = async (id, data) => {
  const res = await api.put(`/training/assignments/${id}`, data);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const getAllTrainingAssignments = async () => {
  const res = await api.get('/training/assignments');
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const getNotifications = async () => {
  const res = await api.get('/notifications');
  if (!res.success) throw new Error(res.message);
  return res;
};

export const markNotificationRead = async (id) => {
  const res = await api.put(`/notifications/${id}/read`, {});
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const markAllNotificationsRead = async () => {
  const res = await api.put('/notifications/read-all', {});
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const deleteNotification = async (id) => {
  const res = await api.delete(`/notifications/${id}`);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

// ============================================================
// Dashboards, Analytics, Reports, Search, Recommendations
// ============================================================
export const getDashboardStats = async () => {
  const res = await api.get('/dashboards/stats');
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const getAnalyticsOverview = async () => {
  const res = await api.get('/analytics/overview');
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const getHeadcountReport = async () => {
  const res = await api.get('/reports/headcount');
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const getAttendanceReport = async () => {
  const res = await api.get('/reports/attendance');
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const getRecruitmentReport = async () => {
  const res = await api.get('/reports/recruitment');
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const getPerformanceReport = async () => {
  const res = await api.get('/reports/performance');
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const getReportCsvUrl = (reportType) => {
  const token = localStorage.getItem('token');
  return `${BASE_URL}/reports/${reportType}?export=csv`;
};

export const globalSearch = async (query) => {
  const res = await api.get(`/search?q=${encodeURIComponent(query)}`);
  if (!res.success) throw new Error(res.message);
  return res;
};

export const getMyCareerRecommendations = async () => {
  const res = await api.get('/recommendations/my-recommendations');
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const getJobCandidateMatchesAI = async (jobId) => {
  const res = await api.get(`/recommendations/job-matches/${jobId}`);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

<<<<<<< HEAD
// ============================================================
// Leaves API
// ============================================================
export const getLeaves = async (params = {}) => {
  const query = new URLSearchParams(params).toString();
  const res = await api.get(`/leaves/?${query}`);
=======
// Candidate Profile helper
export const getMyCandidateProfile = async () => {
  const res = await api.get('/candidates/me');
>>>>>>> 8ff31b8c099d5cec38965a82ac8c6e030c590ab3
  if (!res.success) throw new Error(res.message);
  return res.data;
};

<<<<<<< HEAD
export const createLeave = async (data) => {
  const res = await api.post('/leaves/', data);
=======
export const updateMyCandidateProfile = async (data) => {
  const res = await api.put('/candidates/me', data);
>>>>>>> 8ff31b8c099d5cec38965a82ac8c6e030c590ab3
  if (!res.success) throw new Error(res.message);
  return res.data;
};

<<<<<<< HEAD
export const approveLeave = async (id) => {
  const res = await api.patch(`/leaves/${id}/approve`, {});
=======
export const deactivateCandidate = async (id) => {
  const res = await api.patch(`/candidates/${id}/status`, { status: 'Inactive' });
>>>>>>> 8ff31b8c099d5cec38965a82ac8c6e030c590ab3
  if (!res.success) throw new Error(res.message);
  return res.data;
};

<<<<<<< HEAD
export const rejectLeave = async (id, reason = '') => {
  const res = await api.patch(`/leaves/${id}/reject`, { rejection_reason: reason });
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const cancelLeave = async (id) => {
  const res = await api.patch(`/leaves/${id}/cancel`, {});
  if (!res.success) throw new Error(res.message);
  return res.data;
};

// ============================================================
// Attendance API
// ============================================================
export const getAttendance = async (params = {}) => {
  const query = new URLSearchParams(params).toString();
  const res = await api.get(`/attendance/?${query}`);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const createAttendance = async (data) => {
  const res = await api.post('/attendance/', data);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const updateAttendance = async (id, data) => {
  const res = await api.put(`/attendance/${id}`, data);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const checkIn = async () => {
  const res = await api.post('/attendance/check-in', {});
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const checkOut = async () => {
  const res = await api.post('/attendance/check-out', {});
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const getAttendanceSummary = async (employeeId) => {
  const res = await api.get(`/attendance/summary/${employeeId}`);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

// ============================================================
// Performance Reviews API
// ============================================================
export const getPerformanceReviews = async (params = {}) => {
  const query = new URLSearchParams(params).toString();
  const res = await api.get(`/performance/?${query}`);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const createPerformanceReview = async (data) => {
  const res = await api.post('/performance/', data);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const updatePerformanceReview = async (id, data) => {
  const res = await api.put(`/performance/${id}`, data);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const deletePerformanceReview = async (id) => {
  const res = await api.delete(`/performance/${id}`);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const getDepartments = async () => {
  const res = await api.get('/departments/');
  if (!res.success) throw new Error(res.message);
  return res.data;
};
=======
// Bind all named helpers onto api object for universal compatibility
Object.assign(api, {
  getUsers,
  getUser,
  createUser,
  updateUser,
  deactivateUser,
  getRoles,
  getRole,
  getEmployees,
  getJobs,
  searchJobs,
  getJob,
  createJob,
  updateJob,
  changeJobStatus,
  archiveJob,
  getCandidates,
  getCandidate,
  createCandidate,
  updateCandidate,
  updateCandidateStatus,
  deactivateCandidate,
  getMyCandidateProfile,
  updateMyCandidateProfile,
  getApplications,
  getApplication,
  createApplication,
  updateApplicationStatus,
  withdrawApplication,
  shortlistApplication,
  uploadResume,
  getResumes,
  getResume,
  deleteResume,
  downloadResume,
  extractSkills,
  getCandidateMatches,
  getJobCandidateMatches,
  getJobCandidateMatchesList,
  getCandidateRankings,
  getInterviews,
  getInterview,
  createInterview,
  updateInterview,
  updateInterviewStatus,
  deleteInterview,
  submitInterviewFeedback,
  getInterviewFeedback,
  updateInterviewFeedback,
  getOffers,
  getOffer,
  createOffer,
  updateOffer,
  updateOfferStatus,
  deleteOffer,
  acceptOffer,
  declineOffer,
  getAttendance,
  createAttendance,
  updateAttendance,
  checkIn,
  checkOut,
  getAttendanceSummary,
  getLeaves,
  createLeave,
  approveLeave,
  rejectLeave,
  cancelLeave,
  getPerformanceReviews,
  createPerformanceReview,
  updatePerformanceReview,
  deletePerformanceReview,
  getTrainingCourses,
  createTrainingCourse,
  assignTraining,
  getMyTrainings,
  updateTrainingAssignment,
  getAllTrainingAssignments,
  getNotifications,
  markNotificationRead,
  markAllNotificationsRead,
  deleteNotification,
  getDashboardStats,
  getAnalyticsOverview,
  getHeadcountReport,
  getAttendanceReport,
  getRecruitmentReport,
  getPerformanceReport,
  getReportCsvUrl,
  globalSearch,
  getMyCareerRecommendations,
  getJobCandidateMatchesAI
});
>>>>>>> 8ff31b8c099d5cec38965a82ac8c6e030c590ab3
