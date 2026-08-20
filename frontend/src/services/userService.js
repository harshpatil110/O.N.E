const API_BASE_URL = 'http://localhost:8000/api/v1';

const getAuthHeaders = () => {
  const token = localStorage.getItem('token') || localStorage.getItem('access_token');
  return {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {})
  };
};

export const fetchTaskStates = async (userId) => {
  const res = await fetch(`${API_BASE_URL}/tasks/states/${userId}`, { 
    credentials: 'omit', 
    headers: getAuthHeaders() 
  });
  if (!res.ok) throw new Error('Failed to fetch task states');
  return res.json();
};

export const submitTaskForVerification = async (taskId) => {
  const res = await fetch(`${API_BASE_URL}/tasks/submit`, {
    method: 'POST',
    credentials: 'omit',
    headers: getAuthHeaders(),
    body: JSON.stringify({ task_id: taskId })
  });
  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    throw new Error(errData.detail || 'Failed to submit task');
  }
  return res.json();
};
