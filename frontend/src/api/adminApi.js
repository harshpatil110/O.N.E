import { authAxios } from './config';

export const getAdminMetrics = async () => {
  const response = await authAxios.get('/api/v1/admin/metrics');
  return response.data;
};

export const getAdminSessions = async (page = 1, pageSize = 20, role = '', status = '') => {
  const params = new URLSearchParams();
  params.append('page', page);
  params.append('page_size', pageSize);
  if (role) params.append('role', role);
  if (status) params.append('status', status);

  const response = await authAxios.get(`/api/v1/admin/sessions?${params.toString()}`);
  return response.data;
};

export const resendHrNotification = async (sessionId) => {
  const response = await authAxios.post(`/api/v1/admin/notify-hr/${sessionId}`);
  return response.data;
};

export const getSessionChatHistory = async (sessionId) => {
  const response = await authAxios.get(`/api/v1/admin/sessions/${sessionId}/chat-history`);
  return response.data;
};
