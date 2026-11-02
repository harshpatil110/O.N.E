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

export const submitTaskForVerification = async (taskId, proofData = {}) => {
  const payload = {
    task_id: taskId,
    github_repo_url: proofData.githubRepoUrl || null,
    proof_notes: proofData.proofNotes || null,
    screenshots: proofData.screenshots || [],
    subtasks: proofData.subtasks || null,
  };
  const res = await fetch(`${API_BASE_URL}/tasks/submit`, {
    method: 'POST',
    credentials: 'omit',
    headers: getAuthHeaders(),
    body: JSON.stringify(payload)
  });
  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    throw new Error(errData.detail || 'Failed to submit task');
  }
  return res.json();
};

export const fetchTaskChecklistItems = async (taskId, userEmail = '') => {
  const url = `${API_BASE_URL}/tasks/${taskId}/checklist-items${userEmail ? `?user_email=${encodeURIComponent(userEmail)}` : ''}`;
  const res = await fetch(url, {
    credentials: 'omit',
    headers: getAuthHeaders()
  });
  if (!res.ok) throw new Error('Failed to fetch task checklist items');
  return res.json();
};

export const submitTaskProof = async (taskId, proofData = {}) => {
  const res = await fetch(`${API_BASE_URL}/tasks/${taskId}/proof`, {
    method: 'POST',
    credentials: 'omit',
    headers: getAuthHeaders(),
    body: JSON.stringify({
      github_repo_url: proofData.githubRepoUrl || null,
      proof_notes: proofData.proofNotes || null,
      screenshots: proofData.screenshots || [],
      subtasks: proofData.subtasks || null,
      user_email: proofData.userEmail || null,
    })
  });
  if (!res.ok) throw new Error('Failed to submit proof');
  return res.json();
};
