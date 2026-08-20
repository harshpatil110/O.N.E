const API_BASE_URL = 'http://localhost:8000/api/v1';

const getAuthHeaders = () => {
  const token = localStorage.getItem('token') || localStorage.getItem('access_token');
  return {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {})
  };
};

export const fetchDashboardStats = async () => {
  const res = await fetch(`${API_BASE_URL}/admin/dashboard-stats`, { credentials: 'omit', headers: getAuthHeaders() });
  if (!res.ok) throw new Error('Failed to fetch dashboard stats');
  return res.json();
};

export const fetchDevelopers = async () => {
  const res = await fetch(`${API_BASE_URL}/admin/developers`, { credentials: 'omit', headers: getAuthHeaders() });
  if (!res.ok) throw new Error('Failed to fetch developer list');
  return res.json();
};

export const fetchUserChatHistory = async (userId) => {
  console.log(`[API] Fetching chats for user: ${userId}`);
  const url = `${API_BASE_URL}/admin/developers/${userId}/chats`;
  
  const res = await fetch(url, { 
      credentials: 'omit', 
      headers: getAuthHeaders() 
  });
  
  if (!res.ok) {
      console.error(`[API] Failed to fetch. Status: ${res.status}`);
      throw new Error('Failed to fetch chat history');
  }
  
  const data = await res.json();
  console.log(`[API] Raw response data:`, data);
  return data;
};

export const fetchAnalyticsTopics = async () => {
  const res = await fetch(`${API_BASE_URL}/admin/analytics/topics`, { credentials: 'omit', headers: getAuthHeaders() });
  if (!res.ok) throw new Error('Failed to fetch analytics topics');
  return res.json();
};

export const fetchAIInsights = async () => {
  const res = await fetch(`${API_BASE_URL}/admin/analytics/insights`, { credentials: 'omit', headers: getAuthHeaders() });
  if (!res.ok) throw new Error('Failed to fetch AI insights');
  return res.json();
};

export const fetchAdvancedAnalytics = async () => {
  const res = await fetch(`${API_BASE_URL}/admin/analytics/advanced`, { credentials: 'omit', headers: getAuthHeaders() });
  if (!res.ok) throw new Error('Failed to fetch advanced analytics');
  return res.json();
};
