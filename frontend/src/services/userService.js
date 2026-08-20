const API_BASE_URL = 'http://localhost:8000/api/v1';

const getAuthHeaders = () => {
  const token = localStorage.getItem('token') || localStorage.getItem('access_token');
  return {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {})
  };
};

export const fetchMyTaskStatuses = async (userId) => {
  const res = await fetch(`${API_BASE_URL}/tasks/my-task-statuses/${userId}`, { 
    credentials: 'omit', 
    headers: getAuthHeaders() 
  });
  if (!res.ok) throw new Error('Failed to fetch task statuses');
  return res.json();
};
