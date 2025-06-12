import { useState } from 'react'
import { generateVideo } from '../api/videoService'

const VideoGeneration = () => {
  const [formData, setFormData] = useState({
    video_title: '',
    duration: 30
  })
  
  const [result, setResult] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  
  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: name === 'duration' ? parseInt(value) : value
    }))
  }
  
  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')
    
    try {
      // Extract the actual title if it contains the prefix
      let title = formData.video_title.trim();
      
      // Clean up title if it contains metadata
      if (title.includes("Video Title:")) {
        const titleMatch = title.match(/Video Title:\s*(.*?)(?:\s+Duration:|$)/);
        title = titleMatch ? titleMatch[1].trim() : title;
      }
      
      // Client-side validation
      if (title.length > 100) {
        setError('Video title must be 100 characters or less')
        setIsLoading(false)
        return
      }
      
      if (formData.duration < 10 || formData.duration > 300) {
        setError('Duration must be between 10 and 300 seconds')
        setIsLoading(false)
        return
      }
      
      const response = await generateVideo({
        ...formData,
        video_title: title
      })
      
      setResult(response)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate video. Please try again.')
      console.error(err)
    } finally {
      setIsLoading(false)
    }
  }
  
  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">AI Video Generation</h1>
      
      <div className="card mb-8 bg-yellow-50 border border-yellow-200">
        <div className="flex items-start">
          <div className="text-yellow-500 mr-3">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <h3 className="font-semibold text-yellow-800">Coming Soon</h3>
            <p className="text-yellow-700 text-sm">
              Full video generation with animations and voiceovers will be available soon. 
              Currently, this demo will generate a video concept and script.
            </p>
          </div>
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div>
          <div className="card">
            <h2 className="text-xl font-semibold mb-4">Create Your Video</h2>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="video_title" className="block text-sm font-medium text-gray-700 mb-1">
                  Video Title/Topic
                </label>
                <input
                  type="text"
                  id="video_title"
                  name="video_title"
                  value={formData.video_title}
                  onChange={handleChange}
                  className="input-field"
                  required
                  placeholder="e.g., Product Demo, Company Introduction, etc."
                />
              </div>
              
              <div>
                <label htmlFor="duration" className="block text-sm font-medium text-gray-700 mb-1">
                  Duration (seconds)
                </label>
                <input
                  type="range"
                  id="duration"
                  name="duration"
                  min="15"
                  max="120"
                  step="15"
                  value={formData.duration}
                  onChange={handleChange}
                  className="w-full"
                />
                <div className="flex justify-between text-xs text-gray-500">
                  <span>15s</span>
                  <span>{formData.duration}s</span>
                  <span>120s</span>
                </div>
              </div>
              
              {error && (
                <div className="text-red-600 text-sm">{error}</div>
              )}
              
              <button
                type="submit"
                className="btn btn-primary w-full"
                disabled={isLoading}
              >
                {isLoading ? 'Generating...' : 'Generate Video Concept'}
              </button>
            </form>
          </div>
          
          <div className="mt-6 card bg-gray-50">
            <h3 className="text-lg font-semibold mb-3">Video Creation Process</h3>
            <ol className="list-decimal pl-5 space-y-2 text-gray-700">
              <li>Generate a video concept and script</li>
              <li>Create storyboards and visual elements</li>
              <li>Add animations and transitions</li>
              <li>Generate AI voiceover narration</li>
              <li>Combine all elements into a final video</li>
            </ol>
          </div>
        </div>
        
        <div>
          <div className="card h-full">
            <h2 className="text-xl font-semibold mb-4">Generated Video Concept</h2>
            
            {isLoading ? (
              <div className="flex items-center justify-center h-64">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
              </div>
            ) : result ? (
              <div className="bg-gray-50 p-4 rounded-md border border-gray-200 min-h-[300px]">
                <div className="mb-3">
                  <span className="inline-block bg-primary-100 text-primary-800 text-xs px-2 py-1 rounded-full font-medium">
                    {formData.duration} seconds
                  </span>
                </div>
                
                <p className="whitespace-pre-line">{result.detailed_script}</p>
                
                <div className="mt-6 flex justify-end">
                  <button
                    onClick={() => navigator.clipboard.writeText(result.detailed_script)}
                    className="btn btn-secondary text-sm flex items-center"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" />
                    </svg>
                    Copy to Clipboard
                  </button>
                </div>
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center h-64 text-gray-500">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
                <p>Fill out the form and click "Generate Video Concept" to create your video idea</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default VideoGeneration
