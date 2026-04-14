import { authAxios } from './config';

export const startSession = async () => {
  const response = await authAxios.post('/api/v1/onboarding/start');
  return response.data;
};

export const getSession = async (sessionId) => {
  const response = await authAxios.get(`/api/v1/onboarding/${sessionId}`);
  return response.data;
}

export const sendMessage = async (sessionId, message) => {
  const response = await authAxios.post(`/api/v1/chat/${sessionId}/message`, {
    message
  });
  return response.data;
};

export const getChatHistory = async (sessionId) => {
  // If your backend doesn't support chat history fetch yet, this acts as a stub
  // that can be extended when the endpoint is created.
  try {
    const response = await authAxios.get(`/api/v1/chat/${sessionId}/history`);
    return response.data;
  } catch {
    return [];
  }
};
