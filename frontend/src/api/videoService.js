import api from './config';

export const generateVideo = async (videoData) => {
  try {
    const response = await api.get('/videos', { params: videoData });
    return response.data;
  } catch (error) {
    console.error('Error generating video:', error);
    throw error;
  }
};
