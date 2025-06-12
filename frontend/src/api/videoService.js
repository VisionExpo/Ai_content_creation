import api from './config';

export const generateVideo = async (videoData) => {
  try {
    // Clean up the title and create query parameters
    const params = {
      video_title: videoData.video_title,
      duration: videoData.duration
    };

    // Use GET request with query parameters
    const response = await api.get('/videos', { params });
    
    // Add error handling for specific API responses
    if (response.data.error) {
      throw new Error(response.data.error);
    }
    
    return response.data;
  } catch (error) {
    console.error('Error generating video:', error);
    // Ensure we pass through any error messages from the backend
    if (error.response?.data?.detail) {
      throw new Error(error.response.data.detail);
    }
    throw error;
  }
};
