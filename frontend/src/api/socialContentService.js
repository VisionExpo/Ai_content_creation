import api from './config';

export const generateSocialContent = async (contentData) => {
  try {
    const response = await api.get('/social_content', { params: contentData });
    return response.data;
  } catch (error) {
    console.error('Error generating social content:', error);
    throw error;
  }
};
